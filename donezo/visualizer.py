import matplotlib.pyplot as plt
from .task_manager import TaskManager
import pathlib

def generate_task_stats_plot(manager: TaskManager, output_path: pathlib.Path):
    """Generates a pie chart of task completion status."""
    tasks = manager.list_tasks()
    if not tasks:
        return False

    completed_count = sum(1 for t in tasks if t.completed)
    pending_count = len(tasks) - completed_count

    labels = ['Completed', 'Pending']
    sizes = [completed_count, pending_count]
    colors = ['#4CAF50', '#FFC107']
    explode = (0.1, 0)  # offset the completed slice

    plt.figure(figsize=(8, 6))
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=140)
    plt.title('Task Completion Status Overview')
    plt.axis('equal')
    
    plt.savefig(output_path, transparent=True)
    plt.close()
    return True
