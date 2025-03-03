import flet as ft
import scr.BD.auth
import scr.func


def authentication(page):
    screen_width = page.width
    screen_height = page.height

    login = ft.TextField(label="Логин", width=screen_width * 0.90, value="control1", bgcolor=ft.colors.WHITE)
    password = ft.TextField(label="Пароль", password=True, can_reveal_password=True,
                            width=screen_width * 0.90, value="control1", bgcolor=ft.colors.WHITE)

    def validate(login, password) -> bool:
        return login != "" and password != ""

    def on_click(e):
        if validate(login.value, password.value):
            scr.BD.auth.check_user_credentials(login.value, password.value, page)
        else:
            scr.func.show_snack_bar(page, "Неправильный логин или пароль.")

    return ft.Column(
        [
            ft.Row(
                [
                    ft.Column(
                        [
                            login,
                            password,
                            ft.ElevatedButton(text="Вход", on_click=on_click, bgcolor=ft.colors.BLUE_400,
                                              color=ft.colors.BLACK54)
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    )
                ], alignment=ft.MainAxisAlignment.CENTER
            )
        ]
    )
