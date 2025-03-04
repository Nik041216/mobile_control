import flet as ft
from scr.navigation_apps.users.pages import (
    main_users_screen,
    future_user_screen,
    ratyng_user_screen,
    user_setting_screen
)
from scr.navigation_apps.users.doing_work import chose_meters
from scr import verifications
import scr.toggle_user_sessions
import scr.BD.bd_users.local.update_bd
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.add_job(scr.BD.bd_users.local.update_bd.update_status_task, 'interval', hours=24)
scheduler.start()


def main(page: ft.Page):
    page.window_width = 362.4
    page.window_height = 800
    page.theme_mode = 'light'
    page.bgcolor = ft.Colors.BLUE_50
    page.title = "Мобильный контроллер"
    scr.toggle_user_sessions.handle_user_sessions(page)

    def route_change(e):
        page.views.clear()

        # Основные маршруты
        page.views.append(
            ft.View(
                route="/",
                controls=[main_users_screen.get_content(page)],
                appbar=main_users_screen.get_appbar(page),
                navigation_bar=get_navigation_bar(0),
                bgcolor=ft.Colors.BLUE_50
            )
        )

        if page.route == "/future":
            page.views.append(
                ft.View(
                    route="/future",
                    controls=[future_user_screen.get_content(page)],
                    appbar=future_user_screen.get_appbar(page),
                    navigation_bar=get_navigation_bar(1),
                    bgcolor=ft.Colors.BLUE_50
                )
            )

        if page.route == "/rating":
            page.views.append(
                ft.View(
                    route="/rating",
                    controls=[ratyng_user_screen.get_content(page)],
                    appbar=ratyng_user_screen.get_appbar(page),
                    navigation_bar=get_navigation_bar(2),
                    bgcolor=ft.Colors.BLUE_50
                )
            )

        if page.route == "/settings":
            page.views.append(
                ft.View(
                    route="/settings",
                    controls=[user_setting_screen.get_content(page)],
                    appbar=user_setting_screen.get_appbar(page),
                    navigation_bar=get_navigation_bar(3),
                    bgcolor=ft.Colors.BLUE_50
                )
            )
        if page.route.startswith("/choise_meters/"):
            parts = page.route.split("/")
            id_task = parts[2]
            where = parts[3]

            page.views.append(
                ft.View(
                    route=page.route,
                    controls=[chose_meters.get_content(page, id_task, where)],
                    appbar=chose_meters.get_appbar(page),
                    bgcolor=ft.Colors.BLUE_50
                )
            )

        if page.route == "/authentication":
            page.views.append(
                ft.View(
                    route="/authentication",
                    controls=[verifications.get_content(page)],
                    appbar=None,
                    navigation_bar=None,
                    bgcolor=ft.Colors.BLUE_50
                )
            )

        page.update()

    def view_pop(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    def get_navigation_bar(selected_index=0):
        return ft.NavigationBar(
            selected_index=selected_index,
            destinations=[
                ft.NavigationBarDestination(
                    icon=ft.Icons.ASSIGNMENT_OUTLINED,
                    selected_icon=ft.Icons.ASSIGNMENT_ROUNDED
                ),
                ft.NavigationBarDestination(
                    icon=ft.Icons.TIMER_OUTLINED,
                    selected_icon=ft.Icons.TIMER_ROUNDED
                ),
                ft.NavigationBarDestination(
                    icon=ft.Icons.ASSESSMENT_OUTLINED,
                    selected_icon=ft.Icons.ASSESSMENT_ROUNDED
                ),
                ft.NavigationBarDestination(
                    icon=ft.Icons.SETTINGS_OUTLINED,
                    selected_icon=ft.Icons.SETTINGS_ROUNDED
                )
            ],
            on_change=lambda e: page.go(
                ["/", "/future", "/rating", "/settings"][e.control.selected_index]
            ),
            label_behavior=ft.NavigationBarLabelBehavior.ONLY_SHOW_SELECTED,
            bgcolor=ft.Colors.BLUE_100,
            height=50
        )

    page.go("/")


ft.app(target=main)
