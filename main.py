import flet as ft
import scr.toggle_user_sessions
import scr.BD.bd_users.local.update_bd
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.add_job(scr.BD.bd_users.local.update_bd.update_status_task, 'interval', hours=24)  # Запуск раз в 24 часа
scheduler.start()


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
