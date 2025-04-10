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
    container = ft.Container(expand=True)
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

    bte = ft.Container(
        content=ft.Row([
            ft.Icon(ft.icons.TIME_TO_LEAVE, color=ft.colors.WHITE),
            ft.Text("Выход", style=ft.TextStyle(color=ft.colors.WHITE))
        ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        padding=ft.padding.only(top=20, left=50, right=50, bottom=20),
        bgcolor=const.tasks_completed_text_color,
        border_radius=ft.border_radius.all(25),
        shadow=ft.BoxShadow(
            offset=ft.Offset(5, 5),
            blur_radius=10,
            color=ft.colors.BLACK38
        ),
        ink=True,
        ink_color=ft.colors.RED_200,
        on_click=on_click_exit,
    )

    if result:
        for record in result:
            user_id, login_user, password_user, privileges, first_name, last_name = record

    content = ft.Column(
        [
            ft.Text(f"Сотрудник: {last_name} {first_name}"),
            ft.Text(f"Логин: {login_user}"),
            ft.Text(f"Пароль: {password_user}"),
            bte,
            ft.ElevatedButton("Я хочу получать индивидуальные уведомления", on_click=on_click)
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    conteiner.content = content
    return conteiner
