import flet as ft
import datetime
import scr.BD.bd_users.local.update_bd
import scr.BD.bd_users.local.select_bd
import scr.func
import scr.constants as const
import scr.navigation_apps.users.doing_work.alert_dialog.alert_check_data as alert
import scr.navigation_apps.users.doing_work.alert_dialog.update_data_meters as update
import scr.navigation_apps.users.doing_work.alert_dialog.sealing_meter as sealing
import scr.navigation_apps.users.doing_work.alert_dialog.photo_not_working_meters as not_working
import scr.navigation_apps.users.doing_work.alert_dialog.act_info as act
from scr.components.loading import LoadingManager


def get_content(page, id_task):
    container = ft.Container(expand=True)
    show_meters_data(page, id_task, container)
    return container


def show_meters_data(page, id_task, container_chose_meters):
    screen_width = page.width
    screen_height = page.height
    page.controls.clear()
    results_meters_data = scr.BD.bd_users.local.select_bd.select_meters_data_new(id_task)
    results_address_data = scr.BD.bd_users.local.select_bd.select_tasks_data_for_one(id_task)
    result_act = scr.BD.bd_users.local.select_bd.select_acts_(id_task)
    meters_split = []
    if result_act:
        for result in result_act:
            act_id, task_id, date, reason, made, not_working_meters, unloaded = result
            try:
                meters_split = [r.strip() for r in not_working_meters.split(',') if r.strip()]
            except:
                pass
    filtered_results = [
        result_address_data_v2 for result_address_data_v2 in results_address_data
    ]

    completed = 0
    all_ = 0

    for result in filtered_results:
        id_address, id_task, person_name, street, dom, apartment, phone_number, \
            personal_account, date, date_end, remark_task, status, purpose, registered_residing, \
            standarts, area, saldo, type_address = result
        if date and date_end:
            date = scr.func.reverse_date(date)
            date_end = scr.func.reverse_date(date_end)

    result_info_address = f"Адрес: ул.{street}, д.{dom}, кв.{apartment}"

    def on_click_save(e):
        LoadingManager.show_()
        today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        scr.BD.bd_users.local.update_bd.completed_task(id_task, str(today))
        LoadingManager.hide_()

    def on_click_act(e):
        act.viewing_act(page, id_task, container_chose_meters)

    button_save = ft.ElevatedButton("Выполнить", on_click=on_click_save, bgcolor=ft.Colors.GREEN_200,
                                    color=ft.Colors.BLACK, visible=False)
    button_act = ft.ElevatedButton("Акт", on_click=on_click_act, bgcolor=ft.Colors.PINK_200, color=ft.Colors.BLACK,
                                   visible=False)
    filtered_results_meters = [result for result in results_meters_data]
    column = ft.Column(scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True)
    color = ft.colors.GREY
    column.controls.clear()

    for result in filtered_results_meters:
        id_meters, seal_number, instalation_day, meter_type, marka_id, marka, date_meter_end, \
            location, status_filling, antimagnetic_protection, average_consumption = result
        all_ += 1
        if status_filling is not None:
            completed += 1

        if status_filling == 'выполнен':
            color = const.tasks_completed_color
        elif status_filling == 'в_исполнении':
            color = const.tasks_unloaded_color
        else:
            color = const.tasks_pending_color

        row_to_container = ft.Column(
            [
                ft.Text(f"Марка {marka}", size=17),
                ft.Text(f"Заводской номер: {id_meters}", size=17),
                ft.Text(f"Тип: {meter_type}", size=17)
            ],
            spacing=0
        )

        def create_on_click(id_task, id_meters):
            def on_click(e):
                if result_act:
                    if id_meters in meters_split:
                        not_working.add_photo(page, id_task, container_chose_meters, id_meters)
                    elif status_filling == 'выполнен':
                        if purpose == "Контрольный съем с ИПУ" or purpose == "Замена/Поверка ИПУ":
                            update.update_data(
                                page, id_meters, id_task, container_chose_meters
                            )
                        elif purpose == "Повторная опломбировка ИПУ":
                            sealing.sealing(page, id_task, id_meters, container_chose_meters)
                        else:
                            scr.func.show_alert_yn(page, "Для этого типа заданий нет логики")
                    else:
                        if purpose == "Контрольный съем с ИПУ" or purpose == "Замена/Поверка ИПУ":
                            alert.update_data_check(
                                page, id_task, container_chose_meters, id_meters
                            )
                        elif purpose == "Повторная опломбировка ИПУ":
                            alert.commissioning_meters(page, id_task, container_chose_meters, id_meters)
                        else:
                            scr.func.show_alert_yn(page, "Для этого типа заданий нет логики")

                elif status_filling == 'выполнен':
                    if purpose == "Контрольный съем с ИПУ" or purpose == "Замена/Поверка ИПУ":
                        update.update_data(
                            page, id_meters, id_task, container_chose_meters
                        )
                    elif purpose == "Повторная опломбировка ИПУ":
                        sealing.sealing(page, id_task, id_meters, container_chose_meters)
                    else:
                        scr.func.show_alert_yn(page, "Для этого типа заданий нет логики")
                else:
                    if purpose == "Контрольный съем с ИПУ" or purpose == "Замена/Поверка ИПУ":
                        alert.update_data_check(
                            page, id_task, container_chose_meters, id_meters
                        )
                    elif purpose == "Повторная опломбировка ИПУ":
                        alert.commissioning_meters(page, id_task, container_chose_meters, id_meters)
                    else:
                        scr.func.show_alert_yn(page, "Для этого типа заданий нет логики")

            return on_click

        on_click_container = create_on_click(id_task, id_meters)

        container = ft.Container(
            content=row_to_container,
            padding=ft.padding.only(top=10, left=25, right=25, bottom=10),
            margin=5,
            border_radius=15,
            bgcolor=color,
            ink=True,
            shadow=ft.BoxShadow(
                offset=ft.Offset(0, 7),
                blur_radius=10,
                color=ft.colors.BLACK38
            ),
            alignment=ft.alignment.bottom_left,
            on_click=on_click_container
        )
        column.controls.append(container)

    content_dialog = column
    title = ft.Column(
        [
            ft.Text(result_info_address, size=17, ),
            ft.Text(purpose, size=17, ),
            ft.Text(f"Срок выполнения: \n{date} - {date_end}", size=17),
            ft.Text(f"Примечание: {remark_task}", size=17)
        ], spacing=2.5
    )

    if all_ == completed:
        if result_act:
            if made:
                button_save.visible = True
        else:
            button_save.visible = True
    if result_act:
        button_act.visible = True
    row_button = ft.Row(alignment=ft.MainAxisAlignment.CENTER)
    row_button.controls.append(button_act)
    row_button.controls.append(button_save)

    content1 = ft.Column([
        ft.Column(
            [
                title,
                ft.Divider(color=ft.Colors.BLACK),
                content_dialog,
                row_button
            ], expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0,
        )
    ])
    container_chose_meters.content = content1
    return container_chose_meters
