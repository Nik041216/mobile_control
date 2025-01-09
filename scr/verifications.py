import flet as ft

import scr.BD.auth
import scr.func
import scr.navigation_apps.navigations


def authentication(page):
    page.clean()
    page.navigation_bar = None
    page.appbar = None
    page.controls.clear()
    screen_width = page.width
    screen_height = page.height

    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    login = ft.TextField(label="Логин", width=screen_width * 0.90, value="control1")
    password = ft.TextField(label="Пароль", password=True, can_reveal_password=True, width=screen_width * 0.90, value="control1")

    def validate(login, password) -> bool:
        return login != "" and password != ""

    def on_click(e):
        if validate(login.value, password.value):
            scr.BD.auth.check_user_credentials(login.value, password.value, page)
        else:
            scr.func.show_snack_bar(page, "Неправильный логин или пароль.")

    page.add(
        ft.Row(
            [
                ft.Column(
                    [
                        login,
                        password,
                        ft.ElevatedButton(text="Вход", on_click=on_click,)
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            ], alignment=ft.MainAxisAlignment.CENTER
        )
    )
    page.update()
