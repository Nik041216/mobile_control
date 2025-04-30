import datetime
import flet as ft
import scr.BD.bd_users.local.update_bd
import scr.BD.bd_users.local.delete_bd
import scr.BD.bd_users.local.insert_bd
import scr.BD.bd_users.local.select_bd
import scr.BD.bd_users.bd_server_user
import scr.func
import scr.navigation_apps.users.doing_work.chose_meters
import os
import base64
from scr.components.loading import LoadingManager


def sealing(page, id_task, meter_id, container1):
    screen_width = page.window_width
    results_meters_data_v2 = scr.BD.bd_users.local.select_bd.select_meters_data_new_for_one(id_task, meter_id)
    if results_meters_data_v2:
        for result in results_meters_data_v2:
            (meter_number, seal_number, instalation_date, type_service, marka_id, marka_name, date_of_death, location,
             status_filling, antimagnetic_protection, average_consumption, remark_meter) = result
            if date_of_death:
                date_of_death = scr.func.reverse_date(date_of_death)
    result_info_meters = f"Счетчик: {meter_number} \nДата ликвидации: {date_of_death} \nТип: {type_service}"

    if antimagnetic_protection is not None:
        if antimagnetic_protection is True:
            seal_type = "роторную"
        else:
            seal_type = "антимагнитную пломбу"
    else:
        seal_type = ""

    def close(e):
        page.close(seal_al)
        page.open(alert)

    def not_installed(e):
        page.close(seal_al)
        scr.navigation_apps.users.doing_work.chose_meters.show_meters_data(page, id_task, container1)

    seal_al = ft.AlertDialog(
        modal=True,
        title=ft.Text(f"Установите {seal_type} пломбу"),
        actions=[
            ft.Row(
                [
                    ft.ElevatedButton("Установлена", on_click=close, bgcolor=ft.colors.BLUE_200),
                    ft.ElevatedButton("Назад", on_click=not_installed, bgcolor=ft.colors.RED_200),
                ], alignment=ft.MainAxisAlignment.CENTER
            )
        ],
    )

    title = ft.Column(
        [
            ft.Text(result_info_meters, size=17),
        ]
    )

    seal_number_new = ft.TextField(label="Номер пломбы", )
    remark = ft.TextField(label="Примечание", value=remark_meter, multiline=True, min_lines=1,
                          max_lines=3)

    seal_type_radio = ft.RadioGroup(
        content=ft.Column([
            ft.Radio(value="антимагнитная", label="Антимагнитная пломба"),
            ft.Radio(value="роторная", label="Роторная пломба"),
        ])
    )

    # Добавление кнопок выбора типа защиты счетчика
    protection_type_radio = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(value="белеберда чисто для приведения в bool", label="Да"),
            ft.Radio(value="", label="Нет"),
        ])
    )
    meter_reading = ft.TextField(label="Показания счетчика")

    def save_image_to_db(file_path):
        with open(file_path, 'rb') as file:
            file_data = file.read()

        file_name = os.path.basename(file_path)
        photo_id = scr.BD.bd_users.local.insert_bd.insert_photo(file_name, file_data, id_task, meter_id)
        if scr.func.check_internet():
            scr.BD.bd_users.bd_server_user.unload_photo(photo_id if isinstance(photo_id, list) else [photo_id])

    def pick_files_result(e: ft.FilePickerResultEvent):
        if e.files:
            LoadingManager.show_("Добавление фотографии")
            for file in e.files:
                save_image_to_db(file.path)  # Сохраняем изображение в базу данных
                update_saving_data(meter_id, id_task)

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    page.overlay.append(pick_files_dialog)
    selected_images = {}
    save_photos = ft.Row(scroll=ft.ScrollMode.AUTO, expand=True, )

    def on_click_delete_photo(e, id_p, meter_id, id_task, server_id):
        if scr.func.check_internet():
            scr.BD.bd_users.bd_server_user.delete_photo([server_id])
        try:
            scr.BD.bd_users.local.insert_bd.insert_deleted_photo(server_id)
        except:
            pass
        scr.BD.bd_users.local.delete_bd.delete_photo_db(id_p)
        if id_p in selected_images:
            del selected_images[id_p]
        update_saving_data(meter_id, id_task)
        page.update()

    def update_saving_data(meter_id, id_task):
        images = scr.BD.bd_users.local.select_bd.select_photo_data(meter_id, id_task)
        if images:
            selected_images.clear()
            for result in images:
                id_photo, value_photo, file_name1, task_id, meter_id, server_id = result
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
                                on_click=lambda e, id_p=id_page: on_click_delete_photo(e, id_p, meter_id, id_task,
                                                                                       server_id),
                            ),
                            image=ft.DecorationImage(src_base64=image_base64),
                            width=100,
                            height=100,
                            alignment=ft.Alignment(1.0, -1.0)
                        ),
                    )
                )
        page.update()
        LoadingManager.hide_()

    update_saving_data(meter_id, id_task)

    def zagr(e):
        pick_files_dialog.pick_files(allow_multiple=True, allowed_extensions=["jpeg", "gif", "png", "webp"])

    # Добавление кнопки для выбора фотографии
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

    content = ft.Container(
        content=ft.Stack(
            controls=[
                ft.Column(
                    [
                        seal_number_new,
                        meter_reading,
                        ft.Column(
                            [
                                ft.Text("Есть ли антимагнитная защита у счетчика?", weight=ft.FontWeight.BOLD),
                                protection_type_radio
                            ]
                        ),
                        ft.Column(
                            [
                                ft.Text("Тип пломбы", weight=ft.FontWeight.BOLD),
                                seal_type_radio
                            ]
                        ),
                        remark,
                        save_photos,
                        ft.Row([
                            photo_picker_button
                        ], alignment=ft.MainAxisAlignment.CENTER),
                    ], scroll=ft.ScrollMode.AUTO, expand=True

                ),
                LoadingManager.overlay
            ]
        ), width=screen_width * 0.95
    )

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
        if (seal_number_new.value is None or seal_number_new.value == ""
                or meter_reading.value is None or meter_reading.value == ""
                or seal_type_radio.value is None):
            if seal_number_new.value is None or seal_number_new.value == "":
                seal_number_new.error_text = "Введите номер пломбы"
                seal_number_new.update()
            if meter_reading.value is None or meter_reading.value == "":
                meter_reading.error_text = "Введите показания"
                meter_reading.update()
            if seal_type_radio.value is None:
                create_bottom_sheet("Выберете тип установленной пломбы")
        else:
            scr.BD.bd_users.local.update_bd.update_seal(
                seal_number_new.value, meter_id, id_task, remark.value, meter_reading.value, seal_type_radio.value
            )
            scr.navigation_apps.users.doing_work.chose_meters.show_meters_data(page, id_task, container1)
            page.close(alert)

    def on_click_back(e):
        page.close(alert)
        scr.navigation_apps.users.doing_work.chose_meters.show_meters_data(page, id_task, container1)

    alert = ft.AlertDialog(
        modal=True,
        title=title,
        content=content,
        actions=[
            ft.Row(
                [
                    ft.ElevatedButton("Сохранить", on_click=on_click_save, bgcolor=ft.colors.BLUE_300,
                                      color=ft.Colors.BLACK87),
                    ft.ElevatedButton("Назад", on_click=on_click_back, bgcolor=ft.colors.RED_300,
                                      color=ft.Colors.BLACK87)
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
        ],
        inset_padding=screen_width * 0.05
    )
    page.open(alert)

    page.update()
