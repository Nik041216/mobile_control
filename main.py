import flet as ft
import scr.toggle_user_sessions
import scr.BD.bd_users.local.update_bd


async def main(page: ft.Page):
    page.window_width = 362.4
    page.window_height = 800
    page.window.width = 362.4
    page.window.height = 800
    page.theme_mode = 'light'
    page.bgcolor = ft.Colors.BLUE_50
    page.title = "Мобильный контроллер"
    page.locale_configuration = ft.LocaleConfiguration(
        supported_locales=[
            ft.Locale("es", "ES"),
            ft.Locale("ru", "RU"),
        ],
        current_locale=ft.Locale("ru", "RU")
    )
    await scr.toggle_user_sessions.handle_user_sessions(page)


ft.app(target=main)
