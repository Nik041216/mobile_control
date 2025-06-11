import flet as ft


def get_appbar(page):
    return ft.AppBar(
        title=ft.Text("Профиль сотрудника"),
        center_title=True,
        toolbar_height=50,
        bgcolor=ft.colors.BLUE_100,
    )

