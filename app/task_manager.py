import json
import pathlib
from typing import List, Dict, Any

class TaskManager:
    def __init__(self, db_path: pathlib.Path):
        self.db_path = db_path
        # Ensure the directory exists
        if not self.db_path.parent.exists():
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._load()

    def _load(self) -> None:
        if self.db_path.is_file():
            try:
                content = self.db_path.read_text(encoding='utf-8')
                self._tasks: List[Dict[str, Any]] = json.loads(content)
            except json.JSONDecodeError:
                self._tasks = []
        else:
            self._tasks = []
        
        # Determine next ID based on existing tasks
        if self._tasks:
            self._next_id = max(t["id"] for t in self._tasks) + 1
        else:
            self._next_id = 1

    def _save(self) -> None:
        self.db_path.write_text(json.dumps(self._tasks, indent=2), encoding='utf-8')

    def add_task(self, title: str) -> int:
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty")
        
        task = {
            "id": self._next_id,
            "title": title.strip(),
            "completed": False
        }
        self._tasks.append(task)
        self._next_id += 1
        self._save()
        return task["id"]

    def list_tasks(self) -> List[Dict[str, Any]]:
        return list(self._tasks)

    def _find_index(self, task_id: int) -> int:
        for index, task in enumerate(self._tasks):
            if task["id"] == task_id:
                return index
        raise KeyError(f"Task with ID {task_id} not found.")

    def complete_task(self, task_id: int) -> None:
        index = self._find_index(task_id)
        self._tasks[index]["completed"] = True
        self._save()

    def delete_task(self, task_id: int) -> None:
        index = self._find_index(task_id)
        self._tasks.pop(index)
        self._save()
