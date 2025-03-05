import flet as ft


def get_appbar(page):
    return ft.AppBar(
        title=ft.Text("Акты"),
        center_title=True,
        toolbar_height=50,
        bgcolor=ft.colors.BLUE_100,
    )


def get_content(page):
    container = ft.Container(expand=True)
    rating(page, container)
    return container


def rating(page: ft.Page, container: ft.Container):
    page.window_width = 362.4
    page.window_height = 800
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.floating_action_button = None
    content = ft.Column(
        [
            ft.Row(
                [
                    ft.Column(
                        [
                            ft.ProgressRing(scale=2, color=ft.colors.BLACK45),
                            ft.Text("Здесь пока что ничего нет", size=20)
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=50
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
        ]
    )
    container.content = content
    return container
