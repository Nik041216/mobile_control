import os
import socket
import datetime
import flet as ft


def show_snack_bar(page, message):
    snack_bar = ft.SnackBar(
        content=ft.Text(message),
        open=True,
        duration=800
    )
    page.overlay.append(snack_bar)
    page.update()


def show_alert_yn(page, message):
    def on_button_yes(e):
        page.close(bs)

    def on_button_no(e):
        page.close(bs)

    bs = ft.AlertDialog(
        modal=True,
        title=ft.Text("Предупреждение"),
        content=ft.Text(message),
        actions=[
            ft.ElevatedButton("Да", on_click=on_button_yes),
            ft.ElevatedButton("Назад", on_click=on_button_no)
        ],
    )
    page.open(bs)
    page.update()


def create_filter_button(icon, color, status, on_click):
    return ft.Container(
        content=ft.Row([icon], alignment=ft.MainAxisAlignment.CENTER),
        padding=ft.padding.only(top=5, bottom=5),
        margin=ft.margin.only(left=5, right=5),
        bgcolor=color,
        border_radius=ft.border_radius.all(35),
        shadow=ft.BoxShadow(
            offset=ft.Offset(5, 5),
            blur_radius=10,
            color=ft.colors.BLACK38
        ),
        ink=True,
        ink_color=ft.colors.RED_200,
        col=1,
        on_click=lambda e: on_click(e, icon.color, status)
    )


def check_internet():
    try:
        # Проверяем доступность DNS-сервера Google
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except OSError:
        return False


def reverse_date(date):
    if date:
        date_obj = datetime.datetime.strptime(date, "%Y-%m-%d")
        date = date_obj.strftime("%d-%m-%Y")
        return date


def create_checkbox_with_wrapped_text(
        default_text: str,
        bold_text: str,
        after_text:str,
        checkbox_ref: ft.Ref[ft.Checkbox],
        on_checkbox_change: callable,
        toggle_checkbox: callable,
        name: str = "serial_number",
) -> ft.Container:
    """
    Создает контейнер с чекбоксом и текстом, где текст переносится,
    но первая строка остается в одной линии с чекбоксом.

    Возвращает:
    - ft.Container с настроенными элементами
    """
    return ft.Container(
        content=ft.Column(
            [
                ft.Row([
                    ft.Checkbox(
                        on_change=lambda e: on_checkbox_change(e.control, name),
                        ref=checkbox_ref,
                        value=True
                    ),
                    ft.Column(
                        [
                            ft.Text(
                                spans=[
                                    ft.TextSpan(default_text),
                                    ft.TextSpan(bold_text, ft.TextStyle(weight=ft.FontWeight.BOLD)),
                                    ft.TextSpan(after_text)
                                ],
                                no_wrap=False
                            ),
                        ],
                        spacing=0,
                        expand=True
                    )
                ], expand=True)
            ]
        ),
        on_click=lambda e: toggle_checkbox(e, checkbox_ref.current, name)
    )
