import flet as ft
import scr.BD.bd_users.local.select_bd as select_bd
import scr.func
import scr.BD.bd_users.bd_server_user

statuses = ['не выполнен', 'в исполнении', 'просрочен']
status_icons = {
    'не выполнен': (ft.icons.HOURGLASS_EMPTY, ft.colors.BLUE),
    'в исполнении': (ft.icons.BUILD_OUTLINED, '#ffc107'),
    'выполнен': (ft.icons.CHECK_CIRCLE_OUTLINE, ft.colors.GREEN),
    'просрочен': (ft.icons.ERROR_OUTLINE, ft.colors.RED),
}
sorting = "Адрес"
menu_visible = False
column = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)


def viewing(e, id_task, page):
    def on_click(e):
        page.close(view)

    screen_width = page.window_width

    results_address_data = scr.BD.bd_users.local.select_bd.select_tasks_data_for_one(id_task)
    filtered_results = [
        result_address_data for result_address_data in results_address_data
    ]

    for result in filtered_results:
        id_address, id_task, person_name, street, dom, apartment, phone_number, \
            personal_account, date, date_end, remark, status, purpose, registered_residing, \
            standarts, area, saldo, type_address = result
        if date and date_end:
            date = scr.func.reverse_date(date)
            date_end = scr.func.reverse_date(date_end)
    result_info_address = f"Адрес: ул.{street}, д.{dom}, кв.{apartment}"
    result_info_person = f"ФИО владельца: {person_name}"
    view = ft.AlertDialog(
        modal=True,
        title=ft.Text(result_info_address),
        content=ft.Column(
            [
                ft.Text(
                    spans=[
                        ft.TextSpan("Лицевой счет: "),
                        ft.TextSpan(personal_account, ft.TextStyle(weight=ft.FontWeight.BOLD)),
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
                        ft.TextSpan("Номер телефона: "),
                        ft.TextSpan(phone_number, ft.TextStyle(weight=ft.FontWeight.BOLD)),
                    ],
                    no_wrap=False
                ),
                ft.Text(
                    spans=[
                        ft.TextSpan("Тип адресса: "),
                        ft.TextSpan(type_address, ft.TextStyle(weight=ft.FontWeight.BOLD)),
                    ],
                    no_wrap=False
                ),
                ft.Text(
                    spans=[
                        ft.TextSpan("Дата начала выполнения: "),
                        ft.TextSpan(date, ft.TextStyle(weight=ft.FontWeight.BOLD)),
                    ],
                    no_wrap=False
                ),
                ft.Text(
                    spans=[
                        ft.TextSpan("Конечная дата выполнения: "),
                        ft.TextSpan(date_end, ft.TextStyle(weight=ft.FontWeight.BOLD)),
                    ],
                    no_wrap=False
                ),
                ft.Text(
                    spans=[
                        ft.TextSpan("Тип задания: "),
                        ft.TextSpan(purpose, ft.TextStyle(weight=ft.FontWeight.BOLD)),
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
                ft.Text(
                    spans=[
                        ft.TextSpan("Примечание: "),
                        ft.TextSpan(remark, ft.TextStyle(weight=ft.FontWeight.BOLD)),
                    ],
                    no_wrap=False
                )
            ],
            width=screen_width * 0.95, scroll=ft.ScrollMode.AUTO
        ),
        actions=[
            ft.Row(
                [
                    ft.ElevatedButton("Назад", on_click=on_click, bgcolor=ft.colors.RED_300,
                                      color=ft.Colors.BLACK87)
                ], alignment=ft.MainAxisAlignment.CENTER
            )
        ],
        inset_padding=screen_width * 0.05
    )
    page.open(view)