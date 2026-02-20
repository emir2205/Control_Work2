import sqlite3
from datetime import datetime
import config
from db import queries


def create_tables():
    conn = sqlite3.connect(config.db_path)
    cursor = conn.cursor()

    cursor.execute(queries.tasks_table)

    conn.commit()
    conn.close()


def current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def add_task(name):
    conn = sqlite3.connect(config.db_path)
    cursor = conn.cursor()

    created_at = current_time()
    cursor.execute(queries.insert_tasks, (name, created_at))
    task_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return task_id, created_at


def edit_task(id, new_value):
    conn = sqlite3.connect(config.db_path)
    cursor = conn.cursor()

    cursor.execute(queries.update_tasks, (new_value, id))

    conn.commit()
    conn.close()

    return id


def set_task_completed(id, completed):
    conn = sqlite3.connect(config.db_path)
    cursor = conn.cursor()

    cursor.execute(queries.update_task_completed, (completed, id))

    conn.commit()
    conn.close()

    return id


def delete_task(id):
    conn = sqlite3.connect(config.db_path)
    cursor = conn.cursor()

    cursor.execute(queries.delete_tasks, (id,))

    conn.commit()
    conn.close()

    return id


def get_all_tasks():
    conn = sqlite3.connect(config.db_path)
    cursor = conn.cursor()

    cursor.execute(queries.read_tasks)

    results = cursor.fetchall()
    conn.close()
    return results


def get_tasks_by_filters(completed):
    conn = sqlite3.connect(config.db_path)
    cursor = conn.cursor()

    cursor.execute(queries.read_tasks_by_completed, (completed,))

    result = cursor.fetchall()
    conn.close()
    return result


def clear_completed_tasks():
    conn = sqlite3.connect(config.db_path)
    cursor = conn.cursor()

    cursor.execute(queries.clear_completed_tasks)

    conn.commit()
    conn.close()