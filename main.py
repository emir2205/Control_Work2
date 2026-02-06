from datetime import datetime
import flet as ft

def app(page: ft.Page):
    page.title = "Тест Практика"
    
    plain_text = ft.Text(value="Введите имя ниже")
    history = []
    favorites = []

    history_text = ft.Text()
    favorites_text = ft.Text()

    def clear_history(e):
        history.clear()
        history_text.value = ""
        page.update()

    delete_button = ft.IconButton(icon=ft.Icons.DELETE, on_click=clear_history)

    def change_theme(e):
        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode = ft.ThemeMode.LIGHT
        else:
            page.theme_mode = ft.ThemeMode.DARK

    icon_button = ft.IconButton(icon=ft.Icons.SMART_BUTTON, on_click=change_theme)

    def add_favorite(e):
        if history:
            favorites.append(history[-1])
            favorites_text.value = "Избранные имена: " + ", ".join(favorites)
            page.update()

    fav_button = ft.TextButton("Добавить в избранное", on_click=add_favorite)

    def change(e):
        txt = user_input.value.strip()
        user_input.value = ""

        date = datetime.now().strftime("%Y:%m:%d - %H:%M:%S")

        if txt:
            history.append(txt)
            history[:] = history[-5:]
            history_text.value = "История имён: \n" + ", \n".join(history)
            plain_text.color = None
            plain_text.value = f"{date} - Привет, {txt}!"
        else:
            plain_text.value = "Введите правильное имя!"
            plain_text.color = ft.Colors.RED

        page.update()

    btn = ft.TextButton("Отправить", on_click=change)
    user_input = ft.TextField(label="Enter name", on_submit=change)
    
    page.add(
        plain_text, 
        user_input, 
        btn, 
        history_text, 
        fav_button, 
        favorites_text, 
        icon_button, 
        delete_button
    )

ft.app(target=app)
