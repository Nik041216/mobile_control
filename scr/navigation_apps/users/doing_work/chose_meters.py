import flet as ft
import scr.BD.bd_users.local.update_bd
import scr.BD.bd_users.local.select_bd
import scr.func
import scr.constants as const
import scr.navigation_apps.users.pages.main_users_screen
import scr.navigation_apps.users.pages.future_user_screen
import scr.navigation_apps.users.doing_work.update_data_meters
import scr.navigation_apps.users.doing_work.sealing_meter
import scr.navigation_apps.users.doing_work.create_new_meters as new_meters


def get_appbar(page, id_task, where, container1):
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
        show_meters_data(page, id_task, where, container1)
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
                ft.Text(f"Адрес: {street} {dom} {apartment}"),
                ft.Text(f"ФИО владельца: {person_name}"),
                ft.Text(f"Номер телефона: {phone_number}"),
                ft.Text(f"Кол-во прописаных: {registered_residing}"),
                ft.Text(f"Нормативы: {standarts}"),
                ft.Text(f"Площадь огорода: {area}"),
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


def get_floating_action_button(page, id_task, where, container1):
    def onclick_floating_button(e):
        new_meters.create_meter(page, id_task, where, container1)

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


def get_content(page, id_task, where):
    container = ft.Container(expand=True)
    show_meters_data(page, id_task, where, container)
    return container


def show_meters_data(page, id_task, where, container_chose_meters):
    screen_width = page.width
    screen_height = page.height
    page.controls.clear()
    results_meters_data = scr.BD.bd_users.local.select_bd.select_meters_data_new(id_task)
    results_address_data = scr.BD.bd_users.local.select_bd.select_tasks_data_for_one(id_task)
    filtered_results = [
        result_address_data_v2 for result_address_data_v2 in results_address_data
    ]

    for result in filtered_results:
        id_address, id_task, person_name, street, dom, apartment, phone_number, \
            personal_account, date, date_end, remark_task, status, purpose, registered_residing, \
            standarts, area, saldo, type_address = result
        if date and date_end:
            date = scr.func.reverse_date(date)
            date_end = scr.func.reverse_date(date_end)

    result_info_address = f"Адрес: ул.{street} д.{dom} кв.{apartment}"

    def on_click_back(e):
        if where == "task":
            page.go("/")
        else:
            page.go("/future")

    button_back = ft.ElevatedButton("Назад", on_click=on_click_back, bgcolor=ft.colors.RED_200)
    filtered_results_meters = [result for result in results_meters_data]
    column = ft.Column(scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True)
    color = ft.colors.GREY
    column.controls.clear()

    for result in filtered_results_meters:
        id_meters, seal_number, instalation_day, meter_type, marka_id, marka, date_meter_end, \
            location, status_filling, antimagnetic_protection, average_consumption = result

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
                if purpose == "Контрольный съем с ИПУ" or purpose == "Замена/Поверка ИПУ":
                    scr.navigation_apps.users.doing_work.update_data_meters.update_data(
                        page, id_meters, id_task, where, container_chose_meters
                    )
                elif purpose == "Повторная опломбировка ИПУ":
                    scr.navigation_apps.users.doing_work.sealing_meter.sealing(
                        page, id_task, id_meters, where, container_chose_meters
                    )
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
            ft.Text(f"Срок выполнения: {date} - {date_end}"),
            ft.Text(f"Примечание: {remark_task}", size=17)
        ],
    )
    row_button = ft.Row(alignment=ft.MainAxisAlignment.CENTER)
    row_button.controls.append(button_back)

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
