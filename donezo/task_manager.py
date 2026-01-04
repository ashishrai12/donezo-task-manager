import json
import pathlib
from typing import List, Optional, Iterator
from contextlib import contextmanager
from .models import Task

class TaskManager:
    """Manages the lifecycle and persistence of tasks."""
    
    def __init__(self, db_path: pathlib.Path):
        self.db_path = db_path
        self._tasks: List[Task] = []
        self._ensure_db_exists()
        self._load()

    def _ensure_db_exists(self) -> None:
        if not self.db_path.parent.exists():
            self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def _load(self) -> None:
        if self.db_path.is_file():
            try:
                data = json.loads(self.db_path.read_text(encoding='utf-8'))
                self._tasks = [Task.from_dict(t) for t in data]
            except (json.JSONDecodeError, TypeError, KeyError):
                self._tasks = []
        else:
            self._tasks = []

    def _save(self) -> None:
        data = [t.to_dict() for t in self._tasks]
        self.db_path.write_text(json.dumps(data, indent=2), encoding='utf-8')

    @property
    def _next_id(self) -> int:
        return max((t.id for t in self._tasks), default=0) + 1

    @contextmanager
    def _transaction(self) -> Iterator[None]:
        """A context manager to ensure state is saved after modifications."""
        try:
            yield
        finally:
            self._save()

    def add_task(self, title: str) -> int:
        title = title.strip()
        if not title:
            raise ValueError("Task title cannot be empty")
        
        with self._transaction():
            task = Task(id=self._next_id, title=title)
            self._tasks.append(task)
            return task.id

    def list_tasks(self) -> List[Task]:
        return list(self._tasks)

    def get_stats(self) -> dict:
        total = len(self._tasks)
        completed = sum(1 for t in self._tasks if t.completed)
        return {
            "total": total,
            "completed": completed,
            "pending": total - completed,
            "completion_rate": (completed / total * 100) if total > 0 else 0
        }

    def find_by_id(self, task_id: int) -> Task:
        task = next((t for t in self._tasks if t.id == task_id), None)
        if not task:
            raise KeyError(f"Task with ID {task_id} not found.")
        return task

    def complete_task(self, task_id: int) -> None:
        with self._transaction():
            self.find_by_id(task_id).completed = True

    def delete_task(self, task_id: int) -> None:
        with self._transaction():
            task = self.find_by_id(task_id)
            self._tasks.remove(task)
