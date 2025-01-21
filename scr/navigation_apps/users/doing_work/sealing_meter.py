import datetime
import flet as ft
import scr.BD.bd_users.local.update_bd
import scr.BD.bd_users.local.delete_bd
import scr.BD.bd_users.local.insert_bd
import scr.BD.bd_users.local.select_bd
import scr.BD.bd_users.bd_server_user
import scr.func
import scr.navigation_apps.users.doing_work.chose_meters


def sealing(page, id_task, meter_id, where):
    screen_width = page.width
    results_meters_data_v2 = scr.BD.bd_users.local.select_bd.select_meters_data_new_for_one(id_task, meter_id)
    if results_meters_data_v2:
        for result in results_meters_data_v2:
            meter_number, seal_number, seal_date_instalation, instalation_date, type_service, \
                marka_id, marka_name, date_next_verification, location, \
                status_filling, antimagnetic_protection, average_consumption, remark_meter = result
    result_info_meters = f"Счетчик: {marka_name} \nДата установки: {instalation_date} \nТип: {type_service}"

    if antimagnetic_protection is not None:
        if antimagnetic_protection is True:
            seal_type = "роторную"
        else:
            seal_type = "антимагнитную пломбу"
    else:
        seal_type = ""

    dict_checkboxes = {}

    def on_checkbox_change(checkbox, name):
        dict_checkboxes[name] = checkbox.value

    def toggle_checkbox(e, checkbox, name):
        checkbox.value = not checkbox.value
        checkbox.update()
        on_checkbox_change(checkbox, name)

    marka_checkbox = ft.Ref[ft.Checkbox]()
    serial_number_checkbox = ft.Ref[ft.Checkbox]()
    installation_checkbox = ft.Ref[ft.Checkbox]()
    star_checkbox = ft.Ref[ft.Checkbox]()

    dict_checkboxes["marka"] = False
    dict_checkboxes["serial_number"] = False
    dict_checkboxes["installation"] = False
    dict_checkboxes["star"] = False

    content_question = ft.Column(
        [
            ft.Container(
                content=ft.Column(
                        [
                            ft.Row([
                                ft.Checkbox(on_change=lambda e, name="marka": on_checkbox_change(e.control, name),
                                            ref=marka_checkbox),
                                ft.Text("Марка счетчика совпадает с "),
                            ]),
                            ft.Row([
                                ft.Text(f"{marka_name}", weight=ft.FontWeight.BOLD),
                                ft.Text("?")
                            ]),
                        ]
                    ),
                on_click=lambda e, name="marka": toggle_checkbox(e, marka_checkbox.current, name)
            ),
            ft.Container(
                content=ft.Column(
                        [
                            ft.Row([
                                ft.Checkbox(
                                    on_change=lambda e, name="serial_number": on_checkbox_change(e.control, name),
                                    ref=serial_number_checkbox),
                                ft.Text("Заводской номер счетчика"),
                            ]),
                            ft.Row([
                                ft.Text("совпадает с "),
                                ft.Text(f"{meter_number}", weight=ft.FontWeight.BOLD),
                                ft.Text("?")
                            ]),
                        ]
                    ),
                on_click=lambda e, name="serial_number": toggle_checkbox(e, serial_number_checkbox.current, name)
            ),
            ft.Container(
                content=ft.Column(
                        [
                            ft.Row([
                                ft.Checkbox(
                                    on_change=lambda e, name="installation": on_checkbox_change(e.control, name),
                                    ref=installation_checkbox),
                                ft.Text("Прибор учета устрановлен"),
                            ]),
                            ft.Row([
                                ft.Text("по протоколу?"),
                            ]),
                        ]
                    ),
                on_click=lambda e, name="seal": toggle_checkbox(e, installation_checkbox.current, name)
            ),
            ft.Container(
                content=ft.Column(
                        [
                            ft.Row([
                                ft.Checkbox(on_change=lambda e, name="star": on_checkbox_change(e.control, name),
                                            ref=star_checkbox),
                                ft.Text("Сигнальная звезочка"),
                            ]),
                            ft.Row([
                                ft.Text("вращается равномерно? "),
                            ]),
                        ]
                    ),
                on_click=lambda e, name="seal": toggle_checkbox(e, star_checkbox.current, name)
            )
        ]
    )

    def button_yes(e):
        chect_list = [name for name, is_checked in dict_checkboxes.items() if not is_checked]
        message_string = ""
        if not chect_list:
            page.close(check_meters_data)
        for chect in chect_list:
            if chect == "marka":
                message_string += "Включите в акт несоответствие Марки счетчика\n"
            elif chect == "serial_number":
                message_string += "Включите в акт несоответствие Заводского номера\n"
            elif chect == "installation":
                message_string += "Включите в акт информацию о неправильной установки прибора учета\n"
            elif chect == "star":
                message_string += "Включите в акт информацию о некоректной работе звездочки\n"
        page.close(check_meters_data)
        page.open(alert)
        page.open(seal_al)
        scr.func.show_alert_yn(page, message_string)

    def button_no(e):
        page.close(check_meters_data)
        scr.navigation_apps.users.doing_work.chose_meters.show_meters_data(page, id_task, where)

    check_meters_data = ft.AlertDialog(
        modal=True,
        content=content_question,
        title=ft.Text("Проверте работоспособность счетчика"),
        actions=[
            ft.Row(
                [
                    ft.ElevatedButton("Ввод прибора учета",
                                      on_click=button_yes,
                                      bgcolor=ft.colors.BLUE_200,
                                      width=screen_width*0.30
                                      ),
                    ft.ElevatedButton("Назад",
                                      on_click=button_no,
                                      bgcolor=ft.colors.BLUE_200),
                ], alignment=ft.MainAxisAlignment.CENTER
            )
        ],
    )

    def close(e):
        page.close(seal_al)
        page.open(alert)

    def not_installed(e):
        page.close(seal_al)
        scr.navigation_apps.users.doing_work.chose_meters.show_meters_data(page, id_task, where)

    seal_al = ft.AlertDialog(
        modal=True,
        title=ft.Text(f"Установите {seal_type} пломбу"),
        actions=[
            ft.Row(
                [
                    ft.ElevatedButton("Установлена", on_click=close, bgcolor=ft.colors.BLUE_200),
                    ft.ElevatedButton("Назад", on_click=not_installed, bgcolor=ft.colors.BLUE_200),
                ], alignment=ft.MainAxisAlignment.CENTER
            )
        ],
    )

    title = ft.Column(
        [
            ft.Text(result_info_meters, size=17),
        ]
    )

    seal_number_new = ft.TextField(label="Номер пломбы", )
    remark = ft.TextField(label="Примечание", value=remark_meter, multiline=True, min_lines=1,
                          max_lines=3)

    seal_type_radio = ft.RadioGroup(
        content=ft.Column([
            ft.Radio(value="антимагнитная", label="Антимагнитная пломба"),
            ft.Radio(value="роторная", label="Роторная пломба"),
        ])
    )

    # Добавление кнопок выбора типа защиты счетчика
    protection_type_radio = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(value="с антимагнитной защитой", label="Да"),
            ft.Radio(value="без антимагнитной защиты", label="Нет"),
        ])
    )
    meter_reading = ft.TextField(label="Показания счетчика")

    # Добавление кнопки для выбора фотографии
    photo_button = ft.ElevatedButton("Выбрать фотографию")

    content = ft.Column(
        [
            seal_number_new,
            meter_reading,
            ft.Column(
                [
                    ft.Text("Есть ли антимагнитная защита у счетчика?", weight=ft.FontWeight.BOLD),
                    protection_type_radio
                ]
            ),
            ft.Column(
                [
                    ft.Text("Тип пломбы", weight=ft.FontWeight.BOLD),
                    seal_type_radio
                ]
            ),
            remark,
            photo_button
        ]
    )

    def on_click_save(e):
        if seal_number_new.value is None:
            seal_number_new.error_text = "Введите номер пломбы"
        else:
            scr.BD.bd_users.local.update_bd.update_seal(seal_number_new.value, meter_id, id_task, remark.value)
        page.close(alert)

    def on_click_back(e):
        scr.navigation_apps.users.doing_work.chose_meters.show_meters_data(page, id_task, where)

    alert = ft.AlertDialog(
        modal=True,
        title=title,
        content=content,
        actions=[
            ft.Row(
                [
                    ft.ElevatedButton("Сохранить", on_click=on_click_save),
                    ft.ElevatedButton("Назад", on_click=on_click_back)
                ]
            )
        ]
    )
    page.open(check_meters_data)

    page.update()
