import flet as ft
import scr.BD.bd_users.local.update_bd
import scr.BD.bd_users.local.select_bd
import scr.func
import scr.navigation_apps.users.doing_work.alert_dialog.alert_check_data as alert


def get_floating_action_button(page, id_task, container1):
    def onclick_floating_button(e):
        alert.commissioning_meters(page, id_task, container1, meter_id="", purpose="новый")

    results_address_data = scr.BD.bd_users.local.select_bd.select_tasks_data_for_one(id_task)
    filtered_results = [
        result_address_data_v2 for result_address_data_v2 in results_address_data
    ]

    for result in filtered_results:
        _, _, _, _, _, _, _, _, _, _, _, _, purpose, *_ = result
    if purpose == "Замена/Поверка ИПУ":
        floating_action_button = ft.FloatingActionButton(icon=ft.icons.ADD, on_click=onclick_floating_button,
                                                         tooltip="Добавление нового счетчика")
    else:
        floating_action_button = None
    return floating_action_button
