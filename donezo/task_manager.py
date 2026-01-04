import json
import pathlib
from typing import List, Optional
from .models import Task

class TaskManager:
    def __init__(self, db_path: pathlib.Path):
        self.db_path = db_path
        self._tasks: List[Task] = []
        self._next_id = 1
        self._ensure_db_exists()
        self._load()

    def _ensure_db_exists(self) -> None:
        """Ensures the database directory exists."""
        if not self.db_path.parent.exists():
            self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def _load(self) -> None:
        """Loads tasks from the JSON database."""
        if self.db_path.is_file():
            try:
                content = self.db_path.read_text(encoding='utf-8')
                data = json.loads(content)
                self._tasks = [Task.from_dict(t) for t in data]
            except (json.JSONDecodeError, TypeError, KeyError):
                self._tasks = []
        else:
            self._tasks = []
        
        self._update_next_id()

    def _update_next_id(self) -> None:
        """Updates the next available ID based on current tasks."""
        if self._tasks:
            self._next_id = max(t.id for t in self._tasks) + 1
        else:
            self._next_id = 1

    def _save(self) -> None:
        """Saves current tasks to the JSON database."""
        data = [t.to_dict() for t in self._tasks]
        self.db_path.write_text(json.dumps(data, indent=2), encoding='utf-8')

    def add_task(self, title: str) -> int:
        """Adds a new task and returns its ID."""
        title = title.strip()
        if not title:
            raise ValueError("Task title cannot be empty")
        
        task = Task(id=self._next_id, title=title)
        self._tasks.append(task)
        self._next_id += 1
        self._save()
        return task.id

    def list_tasks(self) -> List[Task]:
        """
        Returns a copy of the current tasks in the manager.
        :return: List of Task objects
        """
        return list(self._tasks)

    def _get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Helper to find a task by its ID."""
        return next((t for t in self._tasks if t.id == task_id), None)

    def complete_task(self, task_id: int) -> None:
        """Marks a task as completed."""
        task = self._get_task_by_id(task_id)
        if not task:
            raise KeyError(f"Task with ID {task_id} not found.")
        task.completed = True
        self._save()

    def delete_task(self, task_id: int) -> None:
        """Deletes a task by its ID."""
        task = self._get_task_by_id(task_id)
        if not task:
            raise KeyError(f"Task with ID {task_id} not found.")
        self._tasks.remove(task)
        self._save()
