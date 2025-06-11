import scr.func
import flet as ft
from scr.navigation_apps.users.pages.task_page import (page_content as task_content, page_appbar as task_app)
from scr.navigation_apps.users.pages.future_task_page import (
    page_content as future_task_content,
    page_appbar as future_task_app
)
from scr.navigation_apps.users.pages.setting_page import (page_content as setting_content, page_appbar as setting_appbar)
from scr.navigation_apps.users.doing_work.chose_page import (page_appbar as chose_appbar, page_content as chose_content,
                                                             page_floating_button as chose_floating_button)
from scr import verifications


# тут программа смотрит какая роль у человека
def role_definition(privileges, page):
    if privileges == 1:
        page.go("/")
    elif privileges == 2:
        page.go("/")
    else:
        debugging(page)


def create_verification_route(page):
    def route_change(e):
        page.views.clear()

        if page.route == "/authentication":
            page.views.append(
                ft.View(
                    route="/authentication",
                    controls=[verifications.get_content(page)],
                    bgcolor=ft.Colors.BLUE_50,
                    vertical_alignment=ft.MainAxisAlignment.CENTER
                )
            )

        page.update()

    def view_pop(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop


def create_route(page):
    def route_change(e):
        page.views.clear()

        # Основные маршруты
        page.views.append(
            ft.View(
                route="/",
                controls=[task_content.get_content(page)],
                appbar=task_app.get_appbar(page),
                navigation_bar=get_navigation_bar(0),
                bgcolor=ft.Colors.BLUE_50
            )
        )

        if page.route == "/future":
            page.views.append(
                ft.View(
                    route="/future",
                    controls=[future_task_content.get_content(page)],
                    appbar=future_task_app.get_appbar(page),
                    navigation_bar=get_navigation_bar(1),
                    bgcolor=ft.Colors.BLUE_50
                )
            )

        # if page.route == "/rating":
        #     page.views.append(
        #         ft.View(
        #             route="/rating",
        #             controls=[ratyng_user_screen.get_content(page)],
        #             appbar=ratyng_user_screen.get_appbar(page),
        #             navigation_bar=get_navigation_bar(2),
        #             bgcolor=ft.Colors.BLUE_50,
        #             vertical_alignment=ft.MainAxisAlignment.CENTER
        #         )
        #     )

        if page.route == "/settings":
            page.views.append(
                ft.View(
                    route="/settings",
                    controls=[setting_content.get_content(page)],
                    appbar=setting_appbar.get_appbar(page),
                    navigation_bar=get_navigation_bar(3),
                    bgcolor=ft.Colors.BLUE_50
                )
            )
        if page.route.startswith("/choise_meters/"):
            parts = page.route.split("/")
            id_task = parts[2]
            where = parts[3]
            if where == "task":
                navigation_bar = get_navigation_bar(0)
            else:
                navigation_bar = get_navigation_bar(1)
            content = chose_content.get_content(page, id_task)

            page.views.append(
                ft.View(
                    route=page.route,
                    controls=[content],
                    appbar=chose_appbar.get_appbar(page, id_task, content),
                    navigation_bar=navigation_bar,
                    bgcolor=ft.Colors.BLUE_50,
                    floating_action_button=chose_floating_button.get_floating_action_button(page, id_task, content)
                )
            )

        if page.route == "/authentication":
            page.views.append(
                ft.View(
                    route="/authentication",
                    controls=[verifications.get_content(page)],
                    bgcolor=ft.Colors.BLUE_50,
                    vertical_alignment=ft.MainAxisAlignment.CENTER
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
                # ft.NavigationBarDestination(
                #     icon=ft.Icons.ASSESSMENT_OUTLINED,
                #     selected_icon=ft.Icons.ASSESSMENT_ROUNDED
                # ),
                ft.NavigationBarDestination(
                    icon=ft.Icons.SETTINGS_OUTLINED,
                    selected_icon=ft.Icons.SETTINGS_ROUNDED
                )
            ],
            on_change=lambda e: page.go(
                # ["/", "/future", "/rating", "/settings"][e.control.selected_index]
                ["/", "/future", "/settings"][e.control.selected_index]
            ),
            label_behavior=ft.NavigationBarLabelBehavior.ONLY_SHOW_SELECTED,
            bgcolor=ft.Colors.BLUE_100,
            height=50
        )


def debugging(page):
    scr.func.show_snack_bar(page, "Незвестный тип пользователя")

