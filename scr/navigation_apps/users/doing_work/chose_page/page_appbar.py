import flet as ft
import scr.BD.bd_users.local.update_bd
import scr.BD.bd_users.local.select_bd
import scr.func
import scr.navigation_apps.users.doing_work.chose_page.page_content as content


def get_appbar(page, id_task, container1):
    screen_width = page.window_width
    results_address_data = scr.BD.bd_users.local.select_bd.select_tasks_data_for_one(id_task)
    filtered_results = [
        result_address_data_v2 for result_address_data_v2 in results_address_data
    ]

    for result in filtered_results:
        id_address, id_task, person_name, street, dom, apartment, phone_number, \
            personal_account, date, date_end, remark_task, status, purpose, registered_residing, \
            standarts, area, saldo, type_address = result

    def on_click_save(e):
        scr.BD.bd_users.local.update_bd.update_remark_task(remark_textfield.value, id_task)
        content.show_meters_data(page, id_task, container1)
        save_button.visible = False
        page.update()

    def on_change_dop_data(e):
        save_button.visible = True
        page.update()

    remark_textfield = ft.TextField(
        label="Примечание", value=remark_task, on_change=on_change_dop_data, multiline=True, min_lines=3, max_lines=3
    )
    save_button = ft.ElevatedButton("Сохранить", visible=False, on_click=on_click_save)
    back_button = ft.ElevatedButton("Назад", on_click=lambda e: page.close(show_details_alert))
    show_details_alert = ft.AlertDialog(
        modal=True,
        title=ft.Text(f"Все данные по заявке {id_task}"),
        content=ft.Column(
            [
                ft.Text(
                    spans=[
                        ft.TextSpan("Адрес: "),
                        ft.TextSpan(f"ул. {street}, д. {dom}, кв. {apartment}",
                                    ft.TextStyle(weight=ft.FontWeight.BOLD)),
                    ],
                    no_wrap=False
                ),
                ft.Text(
                    spans=[
                        ft.TextSpan("ФИО владельца: "),
                        ft.TextSpan(person_name, ft.TextStyle(weight=ft.FontWeight.BOLD)),
                    ],
                    no_wrap=False
                ),
                ft.Text(
                    spans=[
                        ft.TextSpan("Лицевой счет: "),
                        ft.TextSpan(personal_account, ft.TextStyle(weight=ft.FontWeight.BOLD)),
                    ],
                    no_wrap=False
                ),
                ft.Text(
                    spans=[
                        ft.TextSpan("Номер телефона: "),
                        ft.TextSpan(phone_number, ft.TextStyle(weight=ft.FontWeight.BOLD)),
                    ],
                    no_wrap=False
                ),
                ft.Text(
                    spans=[
                        ft.TextSpan("Количество прописанных: "),
                        ft.TextSpan(registered_residing, ft.TextStyle(weight=ft.FontWeight.BOLD)),
                    ],
                    no_wrap=False
                ),
                ft.Text(
                    spans=[
                        ft.TextSpan("Нормативы: "),
                        ft.TextSpan(standarts, ft.TextStyle(weight=ft.FontWeight.BOLD)),
                    ],
                    no_wrap=False
                ),
                ft.Text(
                    spans=[
                        ft.TextSpan("Площадь огорода: "),
                        ft.TextSpan(area, ft.TextStyle(weight=ft.FontWeight.BOLD)),
                    ],
                    no_wrap=False
                ),
                remark_textfield
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            width=screen_width * 0.95
        ),
        inset_padding=screen_width * 0.05,
        actions=[
            ft.Row([
                save_button,
                back_button
            ], alignment=ft.MainAxisAlignment.CENTER)
        ]
    )

    return ft.AppBar(
        title=ft.Text("Выбор счетчика"),
        center_title=True,
        toolbar_height=50,
        bgcolor=ft.colors.BLUE_100,
        actions=[ft.IconButton(icon=ft.Icons.DESCRIPTION_OUTLINED, on_click=lambda e: page.open(show_details_alert),
                               tooltip="Полная информация об адресе")]
    )