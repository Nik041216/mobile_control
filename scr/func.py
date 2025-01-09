import os

import flet as ft
import psycopg2


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


def get_user_db_connection(login, password):
    try:
        conn = psycopg2.connect(
            dbname=os.environ.get("DBNAME", default="Vodocanal_new"),
            user=login,  # Логин пользователя
            password=password,  # Пароль пользователя
            host=os.environ.get("HOST", default="45.151.31.154"),
            port=os.environ.get("PORT", default="5432")
        )
        return conn
    except Exception as ex:
        return None  # Возвращаем None в случае ошибки подключения


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



