from dataclasses import dataclass, asdict
from typing import Dict, Any

@dataclass
class Task:
    """Represents a single task in the system."""
    id: int
    title: str
    completed: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Task":
        return cls(**data)
