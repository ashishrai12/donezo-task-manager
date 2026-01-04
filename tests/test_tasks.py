import pytest
import pathlib
from donezo import TaskManager

@pytest.fixture
def task_manager(tmp_path):
    """Fixture to initialize TaskManager with a temporary JSON file."""
    db_file = tmp_path / "test_tasks.json"
    return TaskManager(db_file)

def test_add_task(task_manager):
    """Test adding a task increases the list count."""
    initial_count = len(task_manager.list_tasks())
    task_manager.add_task("New Task")
    new_count = len(task_manager.list_tasks())
    assert new_count == initial_count + 1
    
    tasks = task_manager.list_tasks()
    assert tasks[-1].title == "New Task"
    assert tasks[-1].completed is False

def test_data_persistence(tmp_path):
    """Test that tasks are saved to and loaded from the file."""
    db_file = tmp_path / "persistence_tasks.json"
    
    # Create first manager and add a task
    manager1 = TaskManager(db_file)
    manager1.add_task("Persistent Task")
    
    # Create second manager pointing to the same file
    manager2 = TaskManager(db_file)
    tasks = manager2.list_tasks()
    
    assert len(tasks) == 1
    assert tasks[0].title == "Persistent Task"

def test_add_empty_task_error(task_manager):
    """Test that adding an empty task raises ValueError."""
    with pytest.raises(ValueError, match="Task title cannot be empty"):
        task_manager.add_task("")
    
    with pytest.raises(ValueError, match="Task title cannot be empty"):
        task_manager.add_task("   ")

def test_complete_task(task_manager):
    """Test completing a task."""
    task_id = task_manager.add_task("Task to complete")
    task_manager.complete_task(task_id)
    
    tasks = task_manager.list_tasks()
    task = next(t for t in tasks if t.id == task_id)
    assert task.completed is True

def test_delete_task(task_manager):
    """Test deleting a task."""
    task_id = task_manager.add_task("Task to delete")
    initial_count = len(task_manager.list_tasks())
    
    task_manager.delete_task(task_id)
    
    final_count = len(task_manager.list_tasks())
    assert final_count == initial_count - 1
    
    # Verify task is gone
    tasks = task_manager.list_tasks()
    assert not any(t.id == task_id for t in tasks)

def test_invalid_task_id(task_manager):
    """Test operations with invalid task IDs raise KeyError."""
    with pytest.raises(KeyError):
        task_manager.complete_task(999)
        
    with pytest.raises(KeyError):
        task_manager.delete_task(999)
