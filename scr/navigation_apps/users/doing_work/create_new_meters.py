import datetime
import flet as ft
import scr.BD.bd_users.local.update_bd
import scr.BD.bd_users.local.delete_bd
import scr.BD.bd_users.local.insert_bd as insert
import scr.BD.bd_users.bd_server_user
import scr.func
import scr.navigation_apps.users.doing_work.chose_meters


def create_meter(page, id_task, where):
    def create_bottom_sheet(text):
        def bottom_sheet_yes(e):
            page.close(bottom_sheet)

        bottom_sheet = ft.BottomSheet(
            content=ft.Container(
                padding=50,
                content=ft.Column(
                    tight=True,
                    controls=[
                        ft.Text(f"{text}"),
                        ft.Row(
                            [
                                ft.ElevatedButton("ОК", on_click=bottom_sheet_yes),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                    ],
                ),
            ),
        )
        page.open(bottom_sheet)

    def on_click_save(e):
        if (meter_id.value is None or meter_id.value == ""
                or meter_marka.value is None or meter_marka.value == ""
                or meter_reading.value is None or meter_reading.value == ""
                or seal_number.value is None or seal_number.value == ""
                or seal_type_radio.value is None
                or meter_type.value is None or meter_type.value == ""):
            if meter_id.value is None or meter_id.value == "":
                meter_id.error_text = "* Введите серийный номер"
                meter_id.update()
            if meter_marka.value is None or meter_marka.value == "":
                meter_marka.error_text = "* Введите марку счетчика"
                meter_marka.update()
            if meter_reading.value is None or meter_reading.value == "":
                meter_reading.error_text = "* Введите текущие показания"
                meter_reading.update()
            if seal_number.value is None or seal_number.value == "":
                seal_number.error_text = "* Введите номер установленной пломбы"
                seal_number.update()
            if seal_type_radio.value is None:
                create_bottom_sheet("Выберете тип установленной пломбы")
            if meter_type.value is None or meter_type.value == "":
                meter_type.error_text = "* Введите тип услуги"
                meter_type.update()
        else:
            insert.insert_new_meters(
                id_task, meter_id.value, meter_marka.value, meter_reading.value, bool(protection_type_radio.value),
                seal_number.value, remark.value, meter_type.value, seal_type_radio.value
            )
            page.close(create_meter_alert)
            page.go(f"/choise_meters/{id_task}/{where}")

    def on_click_back(e):
        page.close(create_meter_alert)
        page.go(f"/choise_meters/{id_task}/{where}")

    meter_id = ft.TextField(label="Серийный номер счетчика", value=None)
    meter_marka = ft.TextField(label="Марка счетчика", value=None)
    meter_reading = ft.TextField(label="Показания счетчика", value=None)
    seal_number = ft.TextField(label="Номер пломбы", value=None)
    remark = ft.TextField(label="Примечание", multiline=True, min_lines=1,
                          max_lines=3, value=None)

    seal_type_radio = ft.RadioGroup(
        content=ft.Column([
            ft.Radio(value="антимагнитная", label="Антимагнитная пломба"),
            ft.Radio(value="роторная", label="Роторная пломба"),
        ])
    )

    protection_type_radio = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(value="gkg", label="Да"),
            ft.Radio(value="", label="Нет"),
        ])
    )

    meter_type = ft.TextField(label="Тип услуги счетчика", value=None)
    photo_button = ft.ElevatedButton("Выбрать фотографию")

    content = ft.Column(
        [
            meter_id,
            meter_marka,
            meter_reading,
            ft.Text("Есть ли у счетчика антимагнитная защита?", weight=ft.FontWeight.BOLD),
            protection_type_radio,
            meter_type,
            seal_number,
            ft.Text("Тип пломбы", weight=ft.FontWeight.BOLD),
            seal_type_radio,
            remark,
            photo_button
        ],
        expand=True,
        scroll=ft.ScrollMode.AUTO
    )
    create_meter_alert = ft.AlertDialog(
        modal=True,
        title=ft.Text("Добавление данных о новом счетчике"),
        content=content,
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
