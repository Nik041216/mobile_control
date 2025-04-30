import flet as ft
import scr.BD.bd_users.local.select_bd as select
import scr.BD.bd_users.local.update_bd as update
import scr.func
import scr.navigation_apps.users.doing_work.chose_meters as chose
from scr.components.loading import LoadingManager
import scr.BD.bd_users.bd_server_user as bd
import os
import base64


def viewing_act(page, id_task, container1):
    screen_width = page.window_width
    selected_images = {}
    save_photos = ft.Row(scroll=ft.ScrollMode.AUTO, expand=True, )
    meter_id = None

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
        if selected_images == {}:
            update.update_made_act_status(act_id, False)
        update_saving_data(meter_id, id_task)
        page.update()

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

    def save_image_to_db(file_path):
        with open(file_path, 'rb') as file:
            file_data = file.read()

        file_name = os.path.basename(file_path)
        photo_id = scr.BD.bd_users.local.insert_bd.insert_photo(file_name, file_data, id_task)
        if scr.func.check_internet():
            scr.BD.bd_users.bd_server_user.unload_photo(photo_id if isinstance(photo_id, list) else [photo_id])

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    page.overlay.append(pick_files_dialog)

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

    def bottom_sheet_yes(e):
        page.close(bottom_sheet)

    bottom_sheet = ft.BottomSheet(
        content=ft.Container(
            padding=50,
            content=ft.Column(
                tight=True,
                controls=[
                    ft.Text("Прикрепите фотографию/фотографии акта как доказательство его наличия"),
                    ft.Row(
                        [
                            ft.ElevatedButton("Хорошо", on_click=bottom_sheet_yes),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                ],
            ),
        ),
    )

    results = select.select_acts_(id_task)
    reasons = ft.Column
    if results:
        for result in results:
            act_id, task_id, date, reason, made, not_working_meters, unloaded = result
            date = scr.func.reverse_date(date)
            reasons_split = [r.strip() for r in reason.split(',') if r.strip()]
            reasons = ft.Column(
                [
                    ft.Row([
                        ft.Text(f"{idx}.", weight=ft.FontWeight.BOLD, width=30, size=17),
                        ft.Column([
                            ft.Text(item, size=17)
                        ], spacing=0,
                            expand=True)
                    ], spacing=2)
                    for idx, item in enumerate(reasons_split, 1)
                ], spacing=4, scroll=ft.ScrollMode.AUTO
            )

    act_content = ft.Column(
        [
            ft.Text(f"Номер задания: {task_id}", size=17),
            ft.Text(f"Дата формирования: {date}", size=17),
            ft.Text("Причины формировния:", size=17),
        ],
    )

    # Разделили контент на прокручиваемую и фиксированную части
    reasons_content = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        controls=[
            reasons,
        ]
    )

    fixed_content = ft.Column(
        expand=False,
        controls=[
            save_photos,
            ft.ElevatedButton("Добавить фотографию", on_click=zagr),
        ], spacing=0
    )

    act_data = ft.Container(
        content=ft.Stack(
            controls=[
                ft.Column(
                    [
                        act_content,
                        reasons_content,
                        fixed_content  # Фиксированная часть (не прокручивается)
                    ],
                    expand=True
                ),
                LoadingManager.overlay
            ]
        ),
        width=screen_width * 0.95
    )

    title = ft.Text("Сформированный акт по заданию")

    def yes_click(e):
        if not selected_images:
            page.open(bottom_sheet)
        else:
            update.update_made_act_status(act_id, True)
            chose.show_meters_data(page, id_task, container1)
            page.close(act_)
            if scr.func.check_internet():
                bd.unload_acts()
            page.update()

    def _close(e):
        page.close(act_)
        chose.show_meters_data(page, id_task, container1)
        page.update()

    act_ = ft.AlertDialog(
        modal=True,
        content=act_data,
        title=title,
        actions=[
            ft.Row(
                [
                    ft.ElevatedButton("Подтвердить акт", on_click=yes_click, bgcolor=ft.colors.BLUE_200),
                    ft.ElevatedButton("Назад", on_click=_close, bgcolor=ft.colors.RED_200)
                ], alignment=ft.MainAxisAlignment.CENTER
            )
        ],
        inset_padding=screen_width * 0.05
    )

    page.open(act_)
    page.update()
