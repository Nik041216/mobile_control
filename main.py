import flet as ft
import scr.toggle_user_sessions


def main(page: ft.Page):
    page.theme_mode = 'light'
    page.bgcolor = ft.colors.BLUE_50
    page.title = "Мобильный контралер"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    scr.toggle_user_sessions.handle_user_sessions(page)
    page.locale_configuration = ft.LocaleConfiguration(
        supported_locales=[
            ft.Locale("es", "ES"),
            ft.Locale("ru", "RU"),
        ],
        current_locale=ft.Locale("ru", "RU")
    )


ft.app(target=main)
