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


def call_show_meters_data(page, id_task, where):
    show_meters_data(page, id_task, where)


def show_meters_data(page, id_task, where):
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

    def onclick_floating_button(e):
        new_meters.create_meter(page, id_task, where)

    if purpose == "Замена/Поверка ИПУ":
        page.floating_action_button = ft.FloatingActionButton(icon=ft.icons.ADD,
                                                              on_click=onclick_floating_button)
        page.update()
    result_info_address = f"Адрес: ул.{street} д.{dom} кв.{apartment}"
    result_info_person = f"ФИО владельца: {person_name}"

    def on_click_back(e):
        if where == "task":
            scr.navigation_apps.users.pages.main_users_screen.user_main(page)
        else:
            scr.navigation_apps.users.pages.future_user_screen.main(page)

    def on_click_save(e):
        scr.BD.bd_users.local.update_bd.update_dop_data_address(
            remark_textfield.value, registered_residing_textfield.value, standarts_textfield.value,
            area_textfield.value, id_address, id_task)
        call_show_meters_data(page, id_task, where)
        page.update()

    button_back = ft.ElevatedButton("Назад", on_click=on_click_back, bgcolor=ft.colors.RED_200)
    button_save_v2 = ft.ElevatedButton("Сохранить", on_click=on_click_save, bgcolor=ft.colors.BLUE_200,
                                       visible=False)
    filtered_results_meters = [result for result in results_meters_data]
    column = ft.Column(scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    color = ft.colors.GREY
    column.controls.clear()

    def on_change_dop_data(e):
        button_save_v2.visible = True
        page.update()

    for result in filtered_results_meters:
        id_meters, seal_number, instalation_day, meter_type, marka_id, marka, date_meter_end, \
             location, status_filling, antimagnetic_protection, average_consumption = result

        if status_filling == 'выполнен':
            color = const.tasks_completed_color
        elif status_filling == 'в_исполнении':
            color = const.tasks_unloaded_color
        else:
            color = const.tasks_pending_color

        result_info_meters = f"Марка: {marka}\nЗаводской номер: {id_meters}\nТип: {meter_type}"

        row_to_container = ft.Column(
            [
                ft.Text(result_info_meters, size=17, ),
            ],
        )

        # Используем замыкание для передачи правильного apartment
        def create_on_click(id_task, id_meters):
            def on_click(e):
                if purpose == "Контрольный съем с ИПУ" or purpose == "Замена/Поверка ИПУ":
                    scr.navigation_apps.users.doing_work.update_data_meters.update_data(page, id_meters, id_task, where)
                elif purpose == "Повторная опломбировка ИПУ":
                    scr.navigation_apps.users.doing_work.sealing_meter.sealing(page, id_task, id_meters, where)

            return on_click

        on_click_container = create_on_click(id_task, id_meters)

        container = ft.Container(
            content=row_to_container,
            padding=ft.padding.only(top=20, left=50, right=50, bottom=20),
            margin=5,
            border_radius=15,
            bgcolor=color,
            ink=True,
            shadow=ft.BoxShadow(
                offset=ft.Offset(0, 7),
                blur_radius=10,
                color=ft.colors.BLACK38
            ),
            alignment=ft.alignment.center,
            on_click=on_click_container
        )
        column.controls.append(container)

    remark_textfield = ft.TextField(label="Примечание", value=remark_task, on_change=on_change_dop_data)
    registered_residing_textfield = ft.TextField(label="Прописанно", value=registered_residing,
                                                 on_change=on_change_dop_data)
    for i in const.norma_water_supply:
        if i == standarts:
            standarts = i
    standarts_textfield = ft.Dropdown(
        on_change=on_change_dop_data,
        label="Нормативы",
        value=standarts,
        options=[
            ft.dropdown.Option(value) for value in const.norma_water_supply
        ],
    )
    area_textfield = ft.TextField(label="Площадь", value=area, on_change=on_change_dop_data)

    dop_buttons_redact = ft.Row(
        [
            ft.Column(
                [
                    remark_textfield,
                    registered_residing_textfield,
                    standarts_textfield,
                    area_textfield

                ]
            )
        ]
    )
    panels = [
        ft.ExpansionPanel(
            header=ft.Row(
                [
                    ft.Text("Редактирование данных адреса")
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True
            ),
            can_tap_header=True,
            content=dop_buttons_redact,
            expanded=False,
            aspect_ratio=100,
            bgcolor=ft.colors.BLUE_100,
        ),
    ]
    panel_list = ft.ExpansionPanelList(
        elevation=25,
        controls=panels,
        expanded_header_padding=3
    )
    container = ft.Container(
        content=panel_list,
        width=screen_width * 0.9,
        border_radius=15,
    )
    column.controls.append(container)
    content_dialog = column
    title = ft.Column(
        [
            ft.Text(result_info_address, size=17, ),
            ft.Text(result_info_person, size=17, ),
            ft.Text(f"Номер телефона владельца {phone_number}", size=17, ),
            ft.Text(f"Примечание по адрессу: {remark_task}", size=17, ),
        ]
    )
    row_button = ft.Row(alignment=ft.MainAxisAlignment.CENTER)
    row_button.controls.append(button_save_v2)
    row_button.controls.append(button_back)

    page.add(
        ft.Column(
            [
                title,
                content_dialog,
                row_button
            ],
            scroll=ft.ScrollMode.AUTO, expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )
    page.update()
