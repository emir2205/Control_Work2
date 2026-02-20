tasks_table = """
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        date TEXT,
        completed INTEGER DEFAULT 0
    )
"""

read_tasks_by_completed = """
    SELECT id, task, date, completed FROM tasks WHERE completed = ?
"""

read_tasks = """
    SELECT id, task, date, completed FROM tasks ORDER BY id DESC
"""

update_tasks = """
    UPDATE tasks SET task = ? WHERE id = ?
"""

update_task_completed = """
    UPDATE tasks SET completed = ? WHERE id = ?
"""

delete_tasks = """
    DELETE FROM tasks WHERE id = ?
"""

clear_completed_tasks = """
    DELETE FROM tasks WHERE completed = 1
"""

insert_tasks = """
    INSERT INTO tasks (task, date) VALUES (?, ?)
"""
