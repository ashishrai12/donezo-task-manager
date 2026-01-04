import pathlib
from .task_manager import TaskManager
from .visualizer import generate_task_stats_plot

def print_menu():
    print("\n" + "="*30)
    print("      DONEZO TASK MANAGER")
    print("="*30)
    print("1. Add Task")
    print("2. List Tasks")
    print("3. Complete Task")
    print("4. Delete Task")
    print("5. View Progress (Plot)")
    print("6. Exit")
    print("="*30)

def get_input(prompt: str) -> str:
    return input(prompt).strip()

def get_valid_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")

def handle_add_task(manager: TaskManager):
    title = get_input("Enter task title: ")
    try:
        task_id = manager.add_task(title)
        print(f"Task added successfully! ID: {task_id}")
    except ValueError as e:
        print(f"Error: {e}")

def handle_list_tasks(manager: TaskManager):
    tasks = manager.list_tasks()
    if not tasks:
        print("No tasks found.")
    else:
        print("\nList of Tasks:")
        for task in tasks:
            status = "[x]" if task.completed else "[ ]"
            print(f"{task.id}. {status} {task.title}")

def handle_complete_task(manager: TaskManager):
    task_id = get_valid_int("Enter ID of task to complete: ")
    try:
        manager.complete_task(task_id)
        print(f"Task {task_id} marked as complete.")
    except KeyError as e:
        print(f"Error: {e}")

def handle_delete_task(manager: TaskManager):
    task_id = get_valid_int("Enter ID of task to delete: ")
    try:
        manager.delete_task(task_id)
        print(f"Task {task_id} deleted.")
    except KeyError as e:
        print(f"Error: {e}")

def handle_view_progress(manager: TaskManager):
    stats = manager.get_stats()
    print(f"\nProgress Summary:")
    print(f"Total Tasks: {stats['total']}")
    print(f"Completed:   {stats['completed']}")
    print(f"Pending:     {stats['pending']}")
    print(f"Rate:        {stats['completion_rate']:.1f}%")

    output_path = pathlib.Path(__file__).parent / "progress.png"
    if generate_task_stats_plot(manager, output_path):
        print(f"Success: Progress plot saved to '{output_path}'")
    else:
        print("Note: Add some tasks first to generate a plot.")

def main():
    db_path = pathlib.Path(__file__).parent / "tasks.json"
    manager = TaskManager(db_path)

    actions = {
        "1": handle_add_task,
        "2": handle_list_tasks,
        "3": handle_complete_task,
        "4": handle_delete_task,
        "5": handle_view_progress,
    }

    while True:
        print_menu()
        choice = get_input("Choose an option: ")

        if choice == "6":
            print("Goodbye!")
            break
        
        action = actions.get(choice)
        if action:
            action(manager)
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
