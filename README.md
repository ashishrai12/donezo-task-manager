# Donezo Task Manager

![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green.svg?style=flat-square)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg?style=flat-square)

**Donezo** is a sleek, professional Command Line Interface (CLI) task manager designed for simplicity and reliability. Built with a modular Python architecture, it features full data persistence and a comprehensive test suite.

![Progress Visualization](donezo/progress.png)

---

## Features

- **Persistent Storage**: Tasks are automatically saved to a local JSON database.
- **Data Visualization**: Generate progress plots to visualize task completion rates.
- **Robust Architecture**: Uses a modern `dataclass` model for data integrity.
- **Fast CLI**: Efficient menu-driven interface for daily task management.
- **Tested**: High reliability with a comprehensive `pytest` suite.
- **Modular Design**: Clean package structure ready for expansion.

---

## Getting Started

### Prerequisites

- Python 3.7 or higher
- `matplotlib` (for progress visualization)

### Installation

1. Clone the repository:
   ```bash
   git clone http://github.com/ashishrai12/donezo-task-manager.git
   cd donezo-task-manager
   ```

2. (Optional) Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install pytest matplotlib
   ```

---

## Usage

Run the following command to start the application:

```bash
python -m donezo.main
```

### Menu Options
1. **Add Task**: Create a new task with a title.
2. **List Tasks**: View all your current tasks and their status.
3. **Complete Task**: Mark a task as finished by its ID.
4. **Delete Task**: Remove a task permanently from the list.
5. **View Progress**: Display task statistics and generate a `progress.png` pie chart.

---

## Testing

The project uses `pytest` for unit testing. To run the full suite:

```bash
# Set PYTHONPATH to include the root directory
$env:PYTHONPATH="."
pytest tests/test_tasks.py
```

---

## Project Structure

```text
donezo-task-manager/
├── donezo/             # Main package
│   ├── __init__.py     # Package initialization
│   ├── main.py         # CLI entry point and menu logic
│   ├── models.py       # Task data models (Dataclasses)
│   ├── task_manager.py # Business logic and persistence
│   ├── visualizer.py   # Plot generation logic
│   ├── tasks.json      # Local database (generated)
│   └── progress.png    # Progress visualization (generated)
├── tests/              # Test suite
│   └── test_tasks.py   # Unit tests for TaskManager
└── README.md           # Project documentation
```

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.
