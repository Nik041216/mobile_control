import datetime
import os
import flet as ft
import scr.BD.bd_users.local.update_bd
import scr.BD.bd_users.local.delete_bd
import scr.BD.bd_users.local.insert_bd
import scr.BD.bd_users.local.select_bd
import scr.BD.bd_users.bd_server_user
import scr.toggle_user_sessions
import scr.func
import scr.navigation_apps.users.doing_work.chose_meters
import base64
from scr.components.loading import LoadingManager


def update_data(page, meter_id, id_task, where, container1):
    screen_width = page.window_width

    def bottom_sheet_yes(e):
        page.close(bottom_sheet)
        page.close(dlg_modal)

    def bottom_sheet_no(e):
        page.close(bottom_sheet)

    def close(e):
        page.close(photo_message)

    bottom_sheet = ft.BottomSheet(
        content=ft.Container(
            padding=50,
            content=ft.Column(
                tight=True,
                controls=[
                    ft.Text("Вы точно хотите выйти?"),
                    ft.Text("Не сохраненные данные удалятся!"),
                    ft.Row(
                        [
                            ft.ElevatedButton("Да", on_click=bottom_sheet_yes),
                            ft.ElevatedButton("Нет", on_click=bottom_sheet_no)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                ],
            ),
        ),
    )

    photo_message = ft.BottomSheet(
        content=ft.Container(
            padding=50,
            content=ft.Column(
                tight=True,
                controls=[
                    ft.Text("Прикрепите фото и видео показания"),
                    ft.Row(
                        [
                            ft.ElevatedButton("Да", on_click=close),
                            ft.ElevatedButton("Нет", on_click=close)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                ],
            ),
        ),
    )

    def peredacha():
        today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        scr.BD.bd_users.local.update_bd.update_local_tasks(
            str(today), id_task, reading_value.value, remark.value, meter_id)
        page.close(dlg_modal)
        scr.navigation_apps.users.doing_work.chose_meters.show_meters_data(page, id_task, where, container1)
        page.update()

    # Обработка нажатия кнопки сохранения
    def on_click_time_task(e):
        if reading_value.value:
            value = float(reading_value.value) - float(last_reading_value)
            if average_consumption is None:
                peredacha()
            else:
                procent = abs(average_consumption - abs(value)) / ((abs(value) + average_consumption) / 2) * 100
                if procent < 20 or value == 0:
                    peredacha()
                else:
                    if selected_images is None or selected_images == {}:
                        page.open(photo_message)
                    else:
                        peredacha()
        else:
            reading_value.error_text = "✱ Введите данные"
            page.update()

    # Обработка нажатия кнопки назад
    def on_click_back(e):
        if reading_value.value != new_reading_value or remark.value != remark_meter:
            page.open(bottom_sheet)
        else:
            page.close(dlg_modal)

    # Инициализация переменных на случай, если данные не будут получены
    marka_name = "Неизвестно"
    meter_number = "Неизвестно"
    date_of_death = "Неизвестно"
    date_of_death2 = "Неизвестно"
    type_service = "Неизвестно"
    seal_number = "Неизвестно"
    location = "Неизвестно"
    remark_meter = "Неизвестно"

    results_meters_data = scr.BD.bd_users.local.select_bd.select_meters_data_new_for_one(id_task, meter_id)
    if results_meters_data:
        for result in results_meters_data:
            (meter_number, seal_number, instalation_date, type_service, marka_id, marka_name, date_of_death,
             location, status_filling, antimagnetic_protection, average_consumption, remark_meter) = result
            date_of_death2 = scr.func.reverse_date(date_of_death)
    result_info_meters = f"Счетчик: {meter_number} \nДата ликвидации: {date_of_death2} \nТип: {type_service}"

    dict_checkboxes = {}

    def on_checkbox_change(checkbox, name):
        dict_checkboxes[name] = checkbox.value

    def toggle_checkbox(e, checkbox, name):
        checkbox.value = not checkbox.value
        checkbox.update()
        on_checkbox_change(checkbox, name)

    marka_checkbox = ft.Ref[ft.Checkbox]()
    serial_number_checkbox = ft.Ref[ft.Checkbox]()
    seal_number_checkbox = ft.Ref[ft.Checkbox]()

    dict_checkboxes["marka"] = True
    dict_checkboxes["serial_number"] = True
    dict_checkboxes["seal"] = True

    content = ft.Column(
        [
            ft.Container(
                content=ft.Column(
                    [
                        ft.Row([
                            ft.Checkbox(on_change=lambda e, name="marka": on_checkbox_change(e.control, name),
                                        ref=marka_checkbox, value=True),
                            ft.Text("Марка счетчика совпадает с "),
                        ]),
                        ft.Row([
                            ft.Text(f"{marka_name}", weight=ft.FontWeight.BOLD),
                            ft.Text("?")
                        ])
                    ]
                ),
                on_click=lambda e, name="marka": toggle_checkbox(e, marka_checkbox.current, name)
            ),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Row([
                            ft.Checkbox(on_change=lambda e, name="serial_number": on_checkbox_change(e.control, name),
                                        ref=serial_number_checkbox, value=True),
                            ft.Text("Заводской номер счетчика"),
                        ]),
                        ft.Row([
                            ft.Text("совпадает с "),
                            ft.Text(f"{meter_number}", weight=ft.FontWeight.BOLD),
                            ft.Text("?")
                        ]),
                    ]
                ),
                on_click=lambda e, name="serial_number": toggle_checkbox(e, serial_number_checkbox.current, name)
            ),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Row([
                            ft.Checkbox(on_change=lambda e, name="seal": on_checkbox_change(e.control, name),
                                        ref=seal_number_checkbox, value=True),
                            ft.Text("Номер пломбы совпадает с "),
                        ]),
                        ft.Row([
                            ft.Text(f"{seal_number}", weight=ft.FontWeight.BOLD),
                            ft.Text("?")
                        ]),
                    ]
                ),
                on_click=lambda e, name="seal": toggle_checkbox(e, seal_number_checkbox.current, name)
            )
        ],
        width=screen_width * 0.95
    )

    def button_yes(e):
        chect_list = [name for name, is_checked in dict_checkboxes.items() if not is_checked]
        message_string = ""
        act_string = ""
        today = datetime.datetime.now()
        date = datetime.datetime.strptime(date_of_death, "%Y-%m-%d")
        total_months = (today.year - date.year) * 12 + (today.month - date.month)
        if not chect_list:
            page.close(check_meters_data)
        for chect in chect_list:
            if chect == "marka":
                message_string += "Включите в акт несоответствие Марки счетчика\n"
                act_string += "Несоответствие Марки счетчика,"
            elif chect == "serial_number":
                message_string += "Включите в акт несоответствие Заводского номера\n"
                act_string += "Несоответствие Заводского номера,"
            elif chect == "seal":
                message_string += "Включите в акт несоответствие Номера пломбы\n"
                act_string += "Несоответствие Номера пломбы,"
        if total_months >= 6:
            message_string += "Включите в акт предписание о скором выходе МПИ\n"
            act_string += "Предписание о скором выходе МПИ,"
        page.open(dlg_modal)
        if bool(message_string):
            scr.func.show_alert_yn(page, message_string)
        if bool(act_string):
            scr.BD.bd_users.local.update_bd.update_acts_insert_meters(id_task, act_string)
        page.close(check_meters_data)

    def button_no(e):
        page.close(check_meters_data)
        scr.navigation_apps.users.doing_work.chose_meters.show_meters_data(page, id_task, where, container1)

    check_meters_data = ft.AlertDialog(
        modal=True,
        content=content,
        title=ft.Text("Уточните Данные"),
        actions=[
            ft.Row(
                [
                    ft.ElevatedButton("Да", on_click=button_yes, bgcolor=ft.colors.BLUE_200),
                    ft.ElevatedButton("Назад", on_click=button_no, bgcolor=ft.colors.BLUE_200),
                ], alignment=ft.MainAxisAlignment.CENTER
            )
        ],
        inset_padding=screen_width * 0.05
    )

    last_reading_date = "Неизвестно"
    last_reading_value = "Неизвестно"
    new_reading_value = ""

    results = scr.BD.bd_users.local.select_bd.select_meter_reading_new(meter_id)
    if results:
        for result in results:
            id_meters, last_reading_date, last_reading_value, new_reading_date, new_reading_value = result
            if new_reading_value is None:
                new_reading_value = ""
            last_reading_date = scr.func.reverse_date(last_reading_date)

    reading_value = ft.TextField(label="Показания счетчика", value=new_reading_value)
    remark = ft.TextField(label="Примечания по счетчику", value=remark_meter, multiline=True, min_lines=1,
                          max_lines=3)

    title = ft.Column(
        [
            ft.Text(result_info_meters, size=17),
        ]
    )

    # Поля ввода для редактирования данных счетчика
    marka_textfield = ft.TextField(label="Марка", value=marka_name)
    meter_number_textfield = ft.TextField(label="Заводской номер", value=meter_number)
    seal_number_textfield = ft.TextField(label="Номер пломбы", value=seal_number)
    location_textfield = ft.TextField(label="Место расположения", value=location)
    meter_type_textfield = ft.TextField(label="Тип услуги", value=type_service)

    # Расширяемый список для редактирования данных счетчика
    dop_buttons_redact = ft.Row(
        [
            ft.Column(
                [
                    marka_textfield,
                    meter_number_textfield,
                    seal_number_textfield,
                    location_textfield,
                    meter_type_textfield,
                ]
            )
        ]
    )

    panels = [
        ft.ExpansionPanel(
            header=ft.Text("Редактирование данных счётчика"),
            can_tap_header=True,
            content=dop_buttons_redact,
            expanded=False,
            aspect_ratio=100,
            bgcolor=ft.colors.BLUE_100
        ),
    ]

    panel_list = ft.ExpansionPanelList(
        elevation=10,
        controls=panels
    )

    def save_image_to_db(file_path):
        with open(file_path, 'rb') as file:
            file_data = file.read()

        file_name = os.path.basename(file_path)
        photo_id = scr.BD.bd_users.local.insert_bd.insert_photo(file_name, file_data, id_task, meter_id)
        if scr.func.check_internet():
            scr.BD.bd_users.bd_server_user.unload_photo(photo_id if isinstance(photo_id, list) else [photo_id])

    def pick_files_result(e: ft.FilePickerResultEvent):
        if e.files:
            for file in e.files:
                print(page.overlay)
                LoadingManager.show_("Добавление фотографии")
                save_image_to_db(file.path)  # Сохраняем изображение в базу данных
                update_saving_data(meter_id, id_task)
                scr.func.show_snack_bar(page, f"Изображение {file.name} сохранено в базу данных.")
        else:
            scr.func.show_snack_bar(page, "Выбор файла отменен.")

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

    # Основной контент модального окна
    meters_data = ft.Container(
        content=ft.Stack(  # <-- Stack, чтобы наложить прогрузку поверх
            controls=[
                ft.Column(
                    [
                        ft.Text(f"Дата контрольных показаний: {last_reading_date}", size=17),
                        ft.Text(f"Контрольные показания: {last_reading_value}", size=17),
                        reading_value,
                        remark,
                        save_photos,
                        ft.ElevatedButton("Добавить фотографию", on_click=zagr),
                        ft.Column(
                            [
                                panel_list
                            ],
                            scroll=ft.ScrollMode.AUTO,
                            expand=True,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        )
                    ],
                    scroll=ft.ScrollMode.AUTO,
                ),
                LoadingManager.overlay  # <-- теперь он внутри AlertDialog
            ]
        ),
        width=screen_width * 0.95
    )

    # Модальное окно с данными счетчика
    dlg_modal = ft.AlertDialog(
        modal=True,
        content=meters_data,
        title=title,
        actions=[
            ft.Row(
                [
                    ft.ElevatedButton("Сохранить", on_click=on_click_time_task, bgcolor=ft.colors.BLUE_200),
                    ft.ElevatedButton("Назад", on_click=on_click_back, bgcolor=ft.colors.RED_200)
                ], alignment=ft.MainAxisAlignment.CENTER
            )
        ],
        inset_padding=screen_width * 0.05
    )

    # Очищаем и обновляем контент страницы
    page.controls.clear()
    page.open(check_meters_data)
    page.update()
