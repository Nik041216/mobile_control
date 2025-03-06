import flet as ft
import scr.BD.bd_users.local.select_bd
import scr.func


def func_check_address_data(page, id_task, where):
    screen_width = page.width
    results_address_data = scr.BD.bd_users.local.select_bd.select_tasks_data_for_one(id_task)
    filtered_results = [
        result_address_data_v2 for result_address_data_v2 in results_address_data
    ]

    for result in filtered_results:
        id_address, id_task, person_name, street, dom, apartment, phone_number, \
            personal_account, date, date_end, remark_task, status, purpose, registered_residing, \
            standarts, area, saldo, type_address = result
    dict_checkboxes = {}

    def on_checkbox_change(checkbox, name):
        dict_checkboxes[name] = checkbox.value

    def toggle_checkbox(e, checkbox, name):
        checkbox.value = not checkbox.value
        checkbox.update()
        on_checkbox_change(checkbox, name)

    fio_checkbox = ft.Ref[ft.Checkbox]()
    residing_checkbox = ft.Ref[ft.Checkbox]()
    standarts_checkbox = ft.Ref[ft.Checkbox]()
    area_checkbox = ft.Ref[ft.Checkbox]()

    if type_address == "МКД":
        dict_checkboxes["FIO"] = False
        dict_checkboxes["registered_residing"] = False
        dict_checkboxes["standarts"] = False

        content = ft.Column(
            [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row([
                                ft.Checkbox(on_change=lambda e, name="FIO": on_checkbox_change(e.control, name),
                                            ref=fio_checkbox),
                                ft.Text("ФИО совпадает с "),
                            ]),
                            ft.Row([
                                ft.Text(f"{person_name}", weight=ft.FontWeight.BOLD),
                                ft.Text("?")
                            ])
                        ]
                    ),
                    on_click=lambda e, name="FIO": toggle_checkbox(e, fio_checkbox.current, name)
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row([
                                ft.Checkbox(
                                    on_change=lambda e, name="registered_residing": on_checkbox_change(e.control, name),
                                    ref=residing_checkbox),
                                ft.Text("Количество прописанных "),
                            ]),
                            ft.Row([
                                ft.Text("/проживающих совпадает с "),
                                ft.Text(f"{registered_residing}", weight=ft.FontWeight.BOLD),
                                ft.Text("?")
                            ]),
                        ]
                    ),
                    on_click=lambda e, name="registered_residing": toggle_checkbox(e, residing_checkbox.current, name)
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row([
                                ft.Checkbox(on_change=lambda e, name="standarts": on_checkbox_change(e.control, name),
                                            ref=standarts_checkbox),
                                ft.Text("Нормативы совпадают с "),
                            ]),
                            ft.Row([
                                ft.Text(f"{standarts}", weight=ft.FontWeight.BOLD),
                                ft.Text("?")
                            ]),
                        ]
                    ),
                    on_click=lambda e, name="standarts": toggle_checkbox(e, standarts_checkbox.current, name)
                )
            ]
        )
    elif type_address == "ЧС":
        dict_checkboxes["FIO"] = False
        dict_checkboxes["registered_residing"] = False
        dict_checkboxes["standarts"] = False
        dict_checkboxes["area"] = False
        content = ft.Column(
            [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row([
                                ft.Checkbox(on_change=lambda e, name="FIO": on_checkbox_change(e.control, name),
                                            ref=fio_checkbox),
                                ft.Text("ФИО совпадает с "),
                            ]),
                            ft.Row([
                                ft.Text(f"{person_name}", weight=ft.FontWeight.BOLD),
                                ft.Text("?")
                            ])
                        ]
                    ),
                    on_click=lambda e, name="FIO": toggle_checkbox(e, fio_checkbox.current, name)
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row([
                                ft.Checkbox(
                                    on_change=lambda e, name="registered_residing": on_checkbox_change(e.control, name),
                                    ref=residing_checkbox),
                                ft.Text("Количество прописанных "),
                            ]),
                            ft.Row([
                                ft.Text("/проживающих совпадает с "),
                                ft.Text(f"{registered_residing}", weight=ft.FontWeight.BOLD),
                                ft.Text("?")
                            ]),
                        ]
                    ),
                    on_click=lambda e, name="registered_residing": toggle_checkbox(e, residing_checkbox.current, name)
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row([
                                ft.Checkbox(on_change=lambda e, name="standarts": on_checkbox_change(e.control, name),
                                            ref=standarts_checkbox),
                                ft.Text("Нормативы совпадают с "),
                            ]),
                            ft.Row([
                                ft.Text(f"{standarts}", weight=ft.FontWeight.BOLD),
                                ft.Text("?")
                            ]),
                        ]
                    ),
                    on_click=lambda e, name="standarts": toggle_checkbox(e, standarts_checkbox.current, name)
                ),
                ft.Container(
                    content=
                    ft.Column(
                        [
                            ft.Row([
                                ft.Checkbox(on_change=lambda e, name="area": on_checkbox_change(e.control, name),
                                            ref=area_checkbox),
                                ft.Text("Площадь без построек "),

                            ]),
                            ft.Row([
                                ft.Text("совпадает с "),
                                ft.Text(f"{area}", weight=ft.FontWeight.BOLD),
                                ft.Text("?")
                            ]),
                        ]
                    ),

                    on_click=lambda e, name="area": toggle_checkbox(e, area_checkbox.current, name)
                ),
            ]
        )
    else:
        dict_checkboxes["FIO"] = False
        content = ft.Column(
            [
                ft.Container(
                    content=ft.Row([
                        ft.Checkbox(on_change=lambda e, name="FIO": on_checkbox_change(e.control, name),
                                    ref=fio_checkbox),
                        ft.Text("ФИО совпадает с "),
                        ft.Text(f"{person_name}", weight=ft.FontWeight.BOLD),
                        ft.Text("?")
                    ]),
                    on_click=lambda e, name="FIO": toggle_checkbox(e, fio_checkbox.current, name)
                )
            ]
        )

    def button_yes(e):
        chect_list = [name for name, is_checked in dict_checkboxes.items() if not is_checked]
        message_string = ""
        if not chect_list:
            page.close(check_address_data)
            page.go(f"/choise_meters/{id_task}/{where}")
        else:
            for chect in chect_list:
                if chect == "FIO":
                    message_string += "Включите в акт пердписание о несоответствии ФИО\n"
                elif chect == "registered_residing":
                    message_string += "Включите в акт несоответствие количества прописанных\n"
                elif chect == "standarts":
                    message_string += "Включите в акт несоответствие с нормативами\n"
                elif chect == "area" and type_address == "ЧС":
                    message_string += "Включите в акт несоответствие площади\n"

            def on_button_yes(e):
                page.close(bs)
                page.go(f"/choise_meters/{id_task}/{where}")

            def on_button_no(e):
                page.close(bs)
                page.go(f"/choise_meters/{id_task}/{where}")

            bs = ft.AlertDialog(
                modal=True,
                title=ft.Text("Предупреждение"),
                content=ft.Text(message_string),
                actions=[
                    ft.ElevatedButton("Да", on_click=on_button_yes),
                    ft.ElevatedButton("Назад", on_click=on_button_no)
                ],
            )
            page.open(bs)
            page.update()
            page.close(check_address_data)

    def button_no(e):
        page.close(check_address_data)
        if where == "task":
            page.go("/")
        else:
            page.go("/future")

    check_address_data = ft.AlertDialog(
        modal=True,
        content=content,
        title=ft.Text("Уточните Данные"),
        actions=[
            ft.Row(
                [
                    ft.ElevatedButton("Да", on_click=button_yes, bgcolor=ft.colors.BLUE_200),
                    ft.ElevatedButton("Назад", on_click=button_no, bgcolor=ft.colors.BLUE_200),
                ], alignment=ft.MainAxisAlignment.CENTER
            )
        ],
        inset_padding=screen_width * 0.10
    )
    page.open(check_address_data)


def update_data_check(page, id_task, meter_id, where):
    pass
