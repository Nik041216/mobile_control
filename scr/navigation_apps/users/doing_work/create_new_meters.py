import flet as ft
import scr.BD.bd_users.local.insert_bd as insert
import scr.BD.bd_users.local.update_bd as update
import scr.BD.bd_users.local.create_bd as create
import scr.BD.bd_users.local.delete_bd as delete
import scr.BD.bd_users.local.delete_bd
import scr.constants as const
import scr.navigation_apps.users.doing_work.chose_meters
import os
import base64


def create_meter(page, id_task, container1):
    screen_width = page.window_width
    create.create_temp_photo_table()

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
            scr.navigation_apps.users.doing_work.chose_meters.show_meters_data(page, id_task, container1)
            page.update()

    def on_click_back(e):
        page.close(create_meter_alert)
        scr.navigation_apps.users.doing_work.chose_meters.show_meters_data(page, id_task, container1)
        delete.delete_photo_temp()
        page.update()

    old_value = ""

    def on_change_meter_id(e):
        nonlocal old_value
        try:
            update.update_photo_meter(old_value, e.control.value)
        except Exception as ex:
            print(ex)
        old_value = e.control.value

    meter_id = ft.TextField(label="Серийный номер счетчика", value=None, on_change=on_change_meter_id)
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

    def get_options():
        options = []
        for type in const.type_water:
            options.append(ft.DropdownOption(type))
        return options

    meter_type = ft.Dropdown(label="Тип услуги счетчика", enable_filter=True, max_menu_height=200, editable=True,
                             width=1000, options=get_options())

    def save_image_to_db(file_path):
        with open(file_path, 'rb') as file:
            file_data = file.read()

        file_name = os.path.basename(file_path)
        scr.BD.bd_users.local.insert_bd.insert_photo_temp(file_name, file_data, id_task, meter_id.value)

    def pick_files_result(e: ft.FilePickerResultEvent):
        if e.files:
            for file in e.files:
                save_image_to_db(file.path)  # Сохраняем изображение в базу данных
                update_saving_data(meter_id.value, id_task)

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    page.overlay.append(pick_files_dialog)
    selected_images = {}
    save_photos = ft.Row(scroll=ft.ScrollMode.AUTO, expand=True, )

    def on_click_delete_photo(e, id_p, meter_id, id_task):
        scr.BD.bd_users.local.delete_bd.delete_photo_db(id_p)
        if id_p in selected_images:
            del selected_images[id_p]
        update_saving_data(meter_id, id_task)
        page.update()

    def update_saving_data(meter_id, id_task):
        images = scr.BD.bd_users.local.select_bd.select_photo_data_temp(meter_id, id_task)
        if images:
            selected_images.clear()
            for result in images:
                id_photo, value_photo, file_name1, task_id, meter_id = result
                selected_images[id_photo] = value_photo  # Добавляем фото в словарь
        save_photos.controls.clear()
        if selected_images:
            for id_page, file in selected_images.items():
                image_base64 = base64.b64encode(file).decode('utf-8')
                save_photos.controls.append(
                    ft.Container(
                        content=ft.Container(
                            content=ft.IconButton(
                                icon=ft.Icons.DELETE,
                                icon_color=ft.Colors.RED,
                                on_click=lambda e, id_p=id_page: on_click_delete_photo(e, id_p, meter_id, id_task),
                            ),
                            image=ft.DecorationImage(src_base64=image_base64),
                            width=100,
                            height=100,
                            alignment=ft.Alignment(1.0, -1.0)
                        ),
                    )
                )
        page.update()

    update_saving_data(meter_id.value, id_task)

    def zagr(e):
        if meter_id.value is None or meter_id.value == "":
            meter_id.error_text = "* Введите серийный номер"
            meter_id.update()
        else:
            pick_files_dialog.pick_files(allow_multiple=True, allowed_extensions=["jpeg", "gif", "png", "webp"])

    photo_picker_button = ft.ElevatedButton(
        content=ft.Row(
            controls=[
                ft.Icon(name=ft.icons.CAMERA_ALT, size=22),
                ft.Text("Выбрать фото"),
            ], width=120,
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
            padding=16,
            side=ft.BorderSide(1, "#b8d1ff"),
        ),
        color="#1a3d7a",
        on_click=zagr
    )

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
            save_photos,
            ft.Row([
                photo_picker_button
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Text(size=1)
        ],
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        width=screen_width * 0.95
    )
    create_meter_alert = ft.AlertDialog(
        modal=True,
        title=ft.Text("Добавление данных о новом счетчике"),
        content=content,
        actions=[
            ft.Row(
                [
                    ft.ElevatedButton("Сохранить", on_click=on_click_save, bgcolor=ft.colors.BLUE_300,
                                      color=ft.Colors.BLACK87),
                    ft.ElevatedButton("Назад", on_click=on_click_back, bgcolor=ft.colors.RED_300,
                                      color=ft.Colors.BLACK87)
                ], alignment=ft.MainAxisAlignment.CENTER
            )
        ],
        inset_padding=screen_width * 0.05
    )

    page.open(create_meter_alert)
    page.update()
