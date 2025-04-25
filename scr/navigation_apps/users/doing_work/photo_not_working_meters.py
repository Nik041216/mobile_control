import flet as ft
import scr.BD.bd_users.local.insert_bd
import scr.func
import scr.navigation_apps.users.doing_work.chose_meters
from scr.components.loading import LoadingManager
import base64
import os


def add_photo(page, id_task, where, container1, meter_id):
    screen_width = page.window_width

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
        button_save.visible = False
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
                            width=200,
                            height=200,
                            alignment=ft.Alignment(1.0, -1.0)
                        ),
                    )
                )
            button_save.visible = True
        page.update()
        LoadingManager.hide_()

    update_saving_data(meter_id, id_task)

    def zagr(e):
        pick_files_dialog.pick_files(allow_multiple=True, allowed_extensions=["jpeg", "gif", "png", "webp"])

    content = ft.Container(
        content=ft.Stack(  # <-- Stack, чтобы наложить прогрузку поверх
            controls=[
                ft.Column(
                    [
                        save_photos,
                        ft.ElevatedButton("Добавить фотографию", on_click=zagr),
                    ],
                    scroll=ft.ScrollMode.AUTO,
                ),
                LoadingManager.overlay  # <-- теперь он внутри AlertDialog
            ]
        ),
        width=screen_width * 0.95
    )

    def on_click_save(e):
        scr.navigation_apps.users.doing_work.chose_meters.show_meters_data(page, id_task, where, container1)
        page.close(dlg)
        page.update()

    button_save = ft.ElevatedButton("Сохранить", on_click=on_click_save, bgcolor=ft.colors.BLUE_200, visible=False)

    dlg = ft.AlertDialog(
        modal=True,
        content=content,
        title=ft.Text("Прикрепите фотографию счетчика"),
        actions=[
            ft.Row(
                [
                     button_save
                ], alignment=ft.MainAxisAlignment.CENTER
            )
        ],
        inset_padding=screen_width * 0.05
    )
    page.open(dlg)
    page.update()
