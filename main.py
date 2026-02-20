import flet as ft

from db import main_db


def main(page: ft.Page):
    page.title = "ToDo List"

    tasks_column = ft.Column()

    def add_to_db(name):
        task_id, task_date = main_db.add_task(name)
        return task_id, task_date

    def edit_db(task_id, new_value):
        main_db.edit_task(task_id, new_value)

    def complete_db(task_id, completed):
        main_db.set_task_completed(task_id, completed)

    def delete_from_db(task_id):
        main_db.delete_task(task_id)

    def add_task_row(task_id, task, task_date, completed):
        def completed_style(is_completed):
            task_text.color = ft.Colors.GREEN if is_completed else None

        def edit(e):
            value = task_text.value
            edit_db(task_id, value)
            task_text.read_only = True
            page.update()

        def delete(e):
            delete_from_db(task_id)
            tasks_column.controls.remove(task_row)
            page.update()

        def to_edit(e):
            if task_text.read_only:
                task_text.read_only = False
            else:
                task_text.read_only = True
            page.update()

        def switch_completed(e):
            if checkbox.value:
                complete_db(task_id, 1)
                completed_style(True)
            else:
                complete_db(task_id, 0)
                completed_style(False)
            page.update()

        task_text = ft.TextField(value=task, expand=True, read_only=True, on_submit=edit)
        task_date_text = ft.Text(value=task_date, size=12)
        checkbox = ft.Checkbox(value=bool(completed), on_change=switch_completed)

        edit_button = ft.IconButton(icon=ft.Icons.EDIT, on_click=to_edit)
        save_button = ft.IconButton(icon=ft.Icons.SAVE, on_click=edit)
        delete_button = ft.IconButton(icon=ft.Icons.DELETE, on_click=delete)

        task_row = ft.Row(
            [checkbox, task_text, task_date_text, edit_button, save_button, delete_button],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        if completed == 1:
            completed_style(True)
        else:
            completed_style(False)
        return task_row

    def add_task(e):
        if user_input.value:
            task_value = user_input.value
            task_id, task_date = add_to_db(task_value)
            new_task = add_task_row(task_id, task_value, task_date, 0)
            user_input.value = ""
            tasks_column.controls.append(new_task)
            page.update()

    def load_from_db():
        tasks_column.controls.clear()
        results = main_db.get_all_tasks()
        if results:
            for task_id, task, task_date, completed in results:
                task_row = add_task_row(task_id, task, task_date, completed)
                tasks_column.controls.append(task_row)
        page.update()

    def filter_by(completed):
        tasks_column.controls.clear()
        results = main_db.get_tasks_by_filters(completed)
        if results:
            for task_id, task, task_date, task_completed in results:
                task_row = add_task_row(task_id, task, task_date, task_completed)
                tasks_column.controls.append(task_row)
        page.update()

    def clear_completed(e):
        main_db.clear_completed_tasks()
        load_from_db()

    user_input = ft.TextField(label="Новая задача", expand=True, on_submit=add_task)
    add_button = ft.IconButton(icon=ft.Icons.ADD, on_click=add_task)

    filter_buttons = ft.Row(
        [
            ft.ElevatedButton("Все", on_click=lambda e: load_from_db()),
            ft.ElevatedButton("Выполненные", on_click=lambda e: filter_by(1)),
            ft.ElevatedButton("Невыполненные", on_click=lambda e: filter_by(0)),
            ft.ElevatedButton("Очистить выполненные", on_click=clear_completed),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    page.add(
        ft.Row([user_input, add_button]),
        filter_buttons,
        tasks_column,
    )

    load_from_db()


if __name__ == "__main__":
    main_db.create_tables()
    ft.run(main, view=ft.AppView.WEB_BROWSER)
