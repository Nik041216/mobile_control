import flet as ft
from scr.components.onesignal import onesignal
import scr.toggle_user_sessions
import scr.func
import scr.BD.bd_users.local.delete_bd
import scr.BD.bd_users.local.select_bd
import scr.API.api_user
import scr.navigation_apps.navigations
import scr.constants as const
import flet_permission_handler as fph


def get_appbar(page):
    return ft.AppBar(
        title=ft.Text("Профиль сотрудника"),
        center_title=True,
        toolbar_height=50,
        bgcolor=ft.colors.BLUE_100,
    )


def get_content(page):
    container = ft.Container(expand=True, alignment=ft.alignment.center)
    setting(page, container)
    return container


def setting(page: ft.Page, conteiner: ft.Container):
    ph = fph.PermissionHandler()
    page.overlay.append(ph)
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.controls.clear()
    page.appbar = ft.AppBar(
        title=ft.Text("Профиль сотрудника"),
        center_title=True,
        toolbar_height=50,
        bgcolor=ft.colors.BLUE_100,
    )

    def on_dialog_result_yes(e):
        opened = ph.open_app_settings()
        page.close(dialog)

    async def on_click_exit(e):
        scr.BD.bd_users.local.delete_bd.delete_data_db()
        await scr.toggle_user_sessions.handle_user_sessions(page)
        await scr.API.api_user.stop_websocket(login_user, password_user)

    def on_click(e):
        permission_status = ph.check_permission(fph.PermissionType.NOTIFICATION)
        if permission_status == fph.PermissionStatus.GRANTED:
            result_ = onesignal.login(user_id)
            if result_:
                scr.func.show_alert_yn(page, "Успешно подключено")
        else:
            page.open(dialog)

    result = scr.BD.bd_users.local.select_bd.select_user_data()

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Разрешить уведомления"),
        content=ft.Text("Для работы уведомлений требуется разрешение. Хотите открыть настройки?"),
        actions=[
            ft.ElevatedButton("Да", on_click=on_dialog_result_yes),
            ft.TextButton("Нет", on_click=lambda e: page.close(dialog)),
        ],
    )

    exit_button = ft.Container(
        width=220,
        height=44,
        border_radius=8,
        gradient=ft.LinearGradient(
            begin=ft.alignment.center_left,
            end=ft.alignment.center_right,
            colors=["#ffebee", "#ffcdd2"],  # Мягкий красный градиент
        ),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=12,
            controls=[
                ft.Icon(
                    name=ft.icons.EXIT_TO_APP,  # Более подходящая иконка для выхода
                    color="#c62828",  # Приглушенный красный
                    size=20,
                ),
                ft.Text(
                    "Выход",
                    color="#8e0000",  # Темно-красный
                    size=14,
                    weight=ft.FontWeight.W_500,
                ),
            ],
        ),
        padding=ft.padding.symmetric(horizontal=16),
        border=ft.border.all(1, "#ef9a9a"),  # Светлая красная граница
        on_click=on_click_exit,
    )

    notification_button = ft.Container(
        width=220,
        height=44,
        border_radius=8,
        gradient=ft.LinearGradient(
            begin=ft.alignment.center_left,
            end=ft.alignment.center_right,
            colors=["#e6f0ff", "#d0e1ff"],  # Мягкий синий градиент
        ),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=12,
            controls=[
                ft.Icon(
                    name=ft.icons.NOTIFICATIONS_ACTIVE,
                    color="#2a5db0",  # Приглушенный синий
                    size=20,
                ),
                ft.Text(
                    "Включить уведомления",
                    color="#1a3d7a",  # Темно-синий
                    size=14,
                    weight=ft.FontWeight.W_500,
                ),
            ],
        ),
        padding=ft.padding.symmetric(horizontal=16),
        border=ft.border.all(1, "#b8d1ff"),  # Светлая синяя граница
        on_click=on_click
    )

    if result:
        for record in result:
            user_id, login_user, password_user, privileges, first_name, last_name = record

    content = ft.Column(
        [
            ft.Text(f"Сотрудник: {last_name} {first_name}"),
            ft.Text(f"Логин: {login_user}"),
            ft.Text(f"Пароль: {password_user}"),
            notification_button,
            exit_button,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True
    )
    conteiner.content = content
    return conteiner
