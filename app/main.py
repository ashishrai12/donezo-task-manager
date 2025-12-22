import sys
import pathlib

# Ensure the package can be imported if running directly
# This allows running with `python donezo/app/main.py` as well as `python -m donezo.app.main`
if __name__ == "__main__" and __package__ is None:
    # Add the project root to sys.path
    file_path = pathlib.Path(__file__).resolve()
    project_root = file_path.parent.parent.parent
    sys.path.insert(0, str(project_root))
    __package__ = "donezo.app"

from .task_manager import TaskManager

def print_menu():
    print("\n--- Donezo Task Manager ---")
    print("1. Add Task")
    print("2. List Tasks")
    print("3. Complete Task")
    print("4. Delete Task")
    print("5. Exit")

def get_valid_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")

def main():
    # Database file is stored in the same directory as this script
    db_path = pathlib.Path(__file__).parent / "tasks.json"
    manager = TaskManager(db_path)

    while True:
        print_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            title = input("Enter task title: ")
            try:
                task_id = manager.add_task(title)
                print(f"Task added successfully! ID: {task_id}")
            except ValueError as e:
                print(f"Error: {e}")
        
        elif choice == "2":
            tasks = manager.list_tasks()
            if not tasks:
                print("No tasks found.")
            else:
                print("\nCurrent Tasks:")
                for task in tasks:
                    status = "[x]" if task["completed"] else "[ ]"
                    print(f"{task['id']}. {status} {task['title']}")
        
        elif choice == "3":
            task_id = get_valid_int("Enter ID of task to complete: ")
            try:
                manager.complete_task(task_id)
                print(f"Task {task_id} marked as complete.")
            except KeyError as e:
                print(f"Error: {e}")
        
        elif choice == "4":
            task_id = get_valid_int("Enter ID of task to delete: ")
            try:
                manager.delete_task(task_id)
                print(f"Task {task_id} deleted.")
            except KeyError as e:
                print(f"Error: {e}")
        
        elif choice == "5":
            print("Goodbye!")
            break
        
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
