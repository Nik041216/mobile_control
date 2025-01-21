import datetime
import flet as ft
import scr.BD.bd_users.local.update_bd
import scr.BD.bd_users.local.delete_bd
import scr.BD.bd_users.local.insert_bd
import scr.BD.bd_users.local.select_bd
import scr.BD.bd_users.bd_server_user
import scr.func
import scr.navigation_apps.users.doing_work.chose_meters


def create_meter(page, id_task, where):
    def on_click_save(e):
        page.close(create_meter_alert)

    def on_click_back(e):
        scr.navigation_apps.users.doing_work.chose_meters.show_meters_data(page, id_task, where)

    meter_reading = ft.TextField()
    seal_number_new = ft.TextField(label="Номер пломбы", )
    remark = ft.TextField(label="Примечание", multiline=True, min_lines=1,
                          max_lines=3)
    seal_type_radio = ft.RadioGroup(
        content=ft.Column([
            ft.Radio(value="антимагнитная", label="Антимагнитная пломба"),
            ft.Radio(value="роторная", label="Роторная пломба"),
        ])
    )

    protection_type_radio = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(value="с антимагнитной защитой", label="Да"),
            ft.Radio(value="без антимагнитной защиты", label="Нет"),
        ])
    )
    photo_button = ft.ElevatedButton("Выбрать фотографию")

    create_meter_alert = ft.AlertDialog(
        modal=True,
        title=ft.Text("Добавление данных о новом счетчике"),
        actions=[
            ft.Row(
                [
                    ft.ElevatedButton("Сохранить", on_click=on_click_save, bgcolor=ft.colors.BLUE_200),
                    ft.ElevatedButton("Назад", on_click=on_click_back, bgcolor=ft.colors.RED_200)
                ], alignment=ft.MainAxisAlignment.CENTER
            )
        ],
    )

    page.open(create_meter_alert)
    page.update()
