import flet as ft
import scr.BD.bd_users.local.select_bd as select_bd
import scr.constants as const
import scr.BD.bd_users.bd_server_user
import scr.func
import scr.navigation_apps.users.doing_work.alert_dialog.alert_check_data as check_alert
import scr.navigation_apps.users.pages.future_task_page.viewing as view
import scr.navigation_apps.users.pages.future_task_page.reschedule_to_another_date as reschedule

completed_icon = ft.Icon(ft.icons.CHECK_CIRCLE_OUTLINE, ft.Colors.GREEN)
failed_icon = ft.Icon(ft.icons.ERROR_OUTLINE, ft.Colors.RED)
pending_icon = ft.Icon(ft.icons.HOURGLASS_EMPTY, ft.Colors.BLUE)
unloaded_icon = ft.Icon(ft.icons.BUILD, '#ffc107')


def create_task_container(page, where, result):
    screen_width = page.window_width
    id_task, _, _, _, street, dom, apartment, phone, _, date, date_end, _, status, purpose, *_ = result
    date_reverse = scr.func.reverse_date(date)
    date_end_reverse = scr.func.reverse_date(date_end)

    stat = ft.Row([ft.Text(f"Статус: {status}")])

    def click_conteiner(e, id_task, status):
        if where == "task":
            res = select_bd.select_acts_(id_task)
            if res or status == "выполнен" or status == "в исполнении":
                page.go(f"/choise_meters/{id_task}/{where}")
            else:
                check_alert.func_check_address_data(page, id_task, where)
        else:
            def on_click(e):
                res = select_bd.select_acts_(id_task)
                where = "future"
                if res or status == "выполнен" or status == "в исполнении":
                    page.go(f"/choise_meters/{id_task}/{where}")
                else:
                    check_alert.func_check_address_data(page, id_task, where)

            chose_action = ft.AlertDialog(
                title=ft.Text("Вы хотите просмотреть данные или выполнить задание?"),
                content=ft.Row(width=screen_width * 0.95),
                actions=[
                    ft.Column([
                        ft.Row(
                            [
                                ft.ElevatedButton("Просмотреть",
                                                  on_click=lambda ex: view.viewing(ex, id_task, page),
                                                  bgcolor=ft.colors.BLUE_300, color=ft.Colors.BLACK87,
                                                  width=page.window_width * 0.35),
                                ft.ElevatedButton("Выполнить",
                                                  on_click=on_click,
                                                  bgcolor=ft.colors.BLUE_300, color=ft.Colors.BLACK87,
                                                  width=page.window_width * 0.30)
                            ], alignment=ft.MainAxisAlignment.CENTER
                        ),
                        ft.Row(
                            [
                                ft.ElevatedButton("Перенос задания",
                                                  on_click=lambda ex: reschedule.reschedule_to_another_date(
                                                      ex, id_task, date, date_end, page
                                                  ),
                                                  bgcolor=ft.colors.BLUE_300, color=ft.Colors.BLACK87),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        )
                    ])
                ],
                inset_padding=screen_width * 0.05
            )

            def show(e):
                page.open(
                    chose_action
                )

            return show

    if status == 'выполнен':
        stat.controls.append(completed_icon)
        color = ft.Colors.GREEN
    elif status == 'в исполнении':
        stat.controls.append(unloaded_icon)
        color = '#ffc107'
    elif status == 'не выполнен':
        stat.controls.append(pending_icon)
        color = ft.colors.BLUE
    elif status == 'просрочен':
        stat.controls.append(failed_icon)
        color = ft.Colors.RED

    result_info = ft.Column([
        ft.Text(f"ул.{street}, д.{dom}, кв.{apartment}", weight=ft.FontWeight.BOLD),
        stat,
        ft.Text(f"Срок: {date_reverse} - {date_end_reverse}"),
        ft.Text(f"Цель: {purpose}")
    ], col=4)

    def call_click(e):
        page.launch_url(f"tel:+7{phone}")

    call_ = ft.ResponsiveRow([
        result_info,
        ft.Container(
            content=ft.Row([
                ft.Icon(ft.icons.PHONE, color=ft.colors.WHITE),
            ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            padding=ft.padding.only(top=40, bottom=40),
            bgcolor=const.tasks_completed_text_color,
            border_radius=ft.border_radius.all(25),
            shadow=ft.BoxShadow(
                offset=ft.Offset(5, 5),
                blur_radius=10,
                color=ft.colors.BLACK38
            ),
            ink=True,
            ink_color=ft.colors.RED_200, col=1, on_click=call_click)
    ], columns=5, expand=True, vertical_alignment=ft.CrossAxisAlignment.CENTER
    )

    return ft.Card(
        content=ft.Container(
            content=ft.Row([
                ft.Container(
                    width=10,
                    height=125 if purpose != "Повторная опломбировка ИПУ" else 135,
                    bgcolor=color
                ),
                call_ if phone is not None and phone != "" else result_info
            ]),
            padding=10,
            margin=5,
            border_radius=15,
            alignment=ft.alignment.bottom_left,
            on_click=lambda e: click_conteiner(e, id_task, status)
        ),
        elevation=2
    )
