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
import scr.navigation_apps.users.doing_work.chose_page.page_content as content
import base64
from scr.components.loading import LoadingManager


def update_data(page, meter_id, id_task, container1):
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
        content.show_meters_data(page, id_task, container1)
        page.close(dlg_modal)
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
    marka_textfield = ft.TextField(label="Марка", value=marka_name, read_only=True)
    meter_number_textfield = ft.TextField(label="Заводской номер", value=meter_number, read_only=True)
    seal_number_textfield = ft.TextField(label="Номер пломбы", value=seal_number, read_only=True)
    location_textfield = ft.TextField(label="Место расположения", value=location, read_only=True)
    meter_type_textfield = ft.TextField(label="Тип услуги", value=type_service, read_only=True)

    # Расширяемый список для редактирования данных счетчика
    dop_buttons_redact = ft.Container(
        content=ft.Column(
            [
                marka_textfield,
                meter_number_textfield,
                seal_number_textfield,
                location_textfield,
                meter_type_textfield,
            ],
            spacing=5  # Уменьшенное расстояние между полями
        ),
        padding=ft.padding.symmetric(horizontal=10, vertical=5),  # Отступы внутри контейнера
        border_radius=ft.border_radius.vertical(bottom=10),
    )

    panels = [
        ft.ExpansionPanel(
            header=ft.Container(
                content=ft.Text(
                    "Данные по прибору учета",
                    style=ft.TextStyle(size=14, weight=ft.FontWeight.W_500)
                ),
                alignment=ft.alignment.center,
                padding=ft.padding.symmetric(vertical=8),
                border_radius=ft.border_radius.vertical(top=10),
            ),
            can_tap_header=True,
            content=dop_buttons_redact,
            expanded=False,
            bgcolor=ft.colors.BLUE_100,
        )
    ]

    panel_list = ft.Container(
        content=ft.ExpansionPanelList(
            controls=panels,
            elevation=0  # Убираем стандартную тень
        ),
        border_radius=10,  # Скругляем внешний контейнер
        clip_behavior=ft.ClipBehavior.HARD_EDGE,  # Обрезаем содержимое по границам
        bgcolor=ft.colors.BLUE_50,
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
                        ft.Row([
                            photo_picker_button
                        ], alignment=ft.MainAxisAlignment.CENTER),
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
                    ft.ElevatedButton("Сохранить", on_click=on_click_time_task, bgcolor=ft.colors.BLUE_300,
                                      color=ft.Colors.BLACK87,),
                    ft.ElevatedButton("Назад", on_click=on_click_back, bgcolor=ft.colors.RED_300,
                                      color=ft.Colors.BLACK87)
                ], alignment=ft.MainAxisAlignment.CENTER
            )
        ],
        inset_padding=screen_width * 0.05
    )

    # Очищаем и обновляем контент страницы
    page.controls.clear()
    page.open(dlg_modal)
    page.update()
