import flet as ft
import scr.BD.auth as auth
import scr.func


def get_content(page):
    container = ft.Container()
    authentication(page, container)
    return container


def authentication(page, container):
    screen_width = page.window_width
    screen_height = page.window_height

    login = ft.TextField(label="Логин", width=screen_width * 0.90, bgcolor=ft.colors.WHITE)
    password = ft.TextField(label="Пароль", password=True, can_reveal_password=True,
                            width=screen_width * 0.90, bgcolor=ft.colors.WHITE)

    def validate(login, password) -> bool:
        return login != "" and password != ""

    async def on_click(e):
        if validate(login.value, password.value):
            await auth.check_user_credentials(login.value, password.value, page)
        else:
            scr.func.show_snack_bar(page, "Неправильный логин или пароль.")

    content = ft.Column(
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
    container.content = content
    return container
