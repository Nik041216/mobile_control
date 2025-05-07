import flet as ft
import scr.BD.bd_users.local.select_bd
import scr.BD.bd_users.local.insert_bd
import scr.navigation_apps.users.doing_work.update_data_meters
import scr.navigation_apps.users.doing_work.photo_not_working_meters
import scr.navigation_apps.users.doing_work.sealing_meter
import scr.navigation_apps.users.doing_work.create_new_meters
import scr.func


def func_check_address_data(page, id_task, where):
    screen_width = page.window_width
    results_address_data = scr.BD.bd_users.local.select_bd.select_tasks_data_for_one(id_task)
    filtered_results = [
        result_address_data_v2 for result_address_data_v2 in results_address_data
    ]

    person_name = "Неизвестно"
    registered_residing = "Неизвестно"
    phone_number = "Неизвестно"
    area = "Неизвестно"

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
    phone_number_checkbox = ft.Ref[ft.Checkbox]()
    area_checkbox = ft.Ref[ft.Checkbox]()

    fio_checkbox_container = scr.func.create_checkbox_with_wrapped_text(
        "ФИО совпадает с ",
        person_name,
        "?",
        fio_checkbox,
        on_checkbox_change,
        toggle_checkbox,
        name="FIO"
    )
    residing_checkbox_container = scr.func.create_checkbox_with_wrapped_text(
        "Количество прописанных/проживающих совпадает с ",
        registered_residing,
        "?",
        residing_checkbox,
        on_checkbox_change,
        toggle_checkbox,
        name="registered_residing"
    )
    phone_number_checkbox_container = scr.func.create_checkbox_with_wrapped_text(
        "Контактный телефон совпадает с ",
        phone_number,
        "?",
        phone_number_checkbox,
        on_checkbox_change,
        toggle_checkbox,
        name="phone_number"
    )
    area_checkbox_container = scr.func.create_checkbox_with_wrapped_text(
        "Площадь без построек ",
        area,
        "?",
        area_checkbox,
        on_checkbox_change,
        toggle_checkbox,
        name="area"
    )

    if type_address == "МКД":
        dict_checkboxes["FIO"] = True
        dict_checkboxes["registered_residing"] = True
        dict_checkboxes["phone"] = True

        content = ft.Column(
            [
                fio_checkbox_container,
                residing_checkbox_container,
                phone_number_checkbox_container,
            ],
            width=screen_width * 0.95
        )
    elif type_address == "ЧС":
        dict_checkboxes["FIO"] = True
        dict_checkboxes["registered_residing"] = True
        dict_checkboxes["phone_number"] = True
        dict_checkboxes["area"] = True
        content = ft.Column(
            [
                fio_checkbox_container,
                residing_checkbox_container,
                phone_number_checkbox_container,
                area_checkbox_container,
            ],
            width=screen_width * 0.95
        )
    else:
        dict_checkboxes["FIO"] = True
        content = ft.Column(
            [
                fio_checkbox_container
            ],
            width=screen_width * 0.95
        )

    def button_yes(e):
        chect_list = [name for name, is_checked in dict_checkboxes.items() if not is_checked]
        message_string = ""
        if not chect_list:
            page.close(check_address_data)
            page.go(f"/choise_meters/{id_task}/{where}")
        else:
            act_string = ""
            for chect in chect_list:
                if chect == "FIO":
                    message_string += "Включите в акт пердписание о несоответствии ФИО\n"
                    act_string += "Несоотвествие ФИО,"
                elif chect == "registered_residing":
                    message_string += "Включите в акт несоответствие количества прописанных\n"
                    act_string += "Несоответствие количества прописанных,"
                elif chect == "phone_number":
                    message_string += "Включите в акт несоответствие контактного номера телефона\n"
                    act_string += "Несоответствие с нормативами,"
                elif chect == "area" and type_address == "ЧС":
                    message_string += "Включите в акт несоответствие площади\n"
                    act_string += "Несоответствие площади"
            if act_string != "":
                scr.BD.bd_users.local.insert_bd.insert_acts(id_task, act_string)

            def on_button_yes(e):
                page.close(bs)
                page.go(f"/choise_meters/{id_task}/{where}")

            bs = ft.AlertDialog(
                modal=True,
                title=ft.Text("Предупреждение"),
                content=ft.Text(message_string),
                actions=[
                    ft.Row(
                        [
                            ft.ElevatedButton("ОК", on_click=on_button_yes)
                        ], alignment=ft.MainAxisAlignment.CENTER)
                ],
            )
            if message_string != "":
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
        title=ft.Text("Уточните данные"),
        actions=[
            ft.Row(
                [
                    ft.ElevatedButton("Да", on_click=button_yes, bgcolor=ft.colors.BLUE_300, color=ft.Colors.BLACK87),
                    ft.ElevatedButton("Назад", on_click=button_no, bgcolor=ft.colors.RED_300, color=ft.Colors.BLACK87),
                ], alignment=ft.MainAxisAlignment.CENTER
            )
        ],
        inset_padding=screen_width * 0.05
    )
    page.open(check_address_data)


# проверка рабоспособности счетчика
def update_data_check(page, id_task, container1, meter_id="", purpose="съем", failure=False):
    screen_width = page.window_width
    meter_number = "Неизвестный прибор учета" if meter_id == "" else meter_id

    dict_checkboxes = {}

    def on_checkbox_change(checkbox, name):
        dict_checkboxes[name] = checkbox.value

    def toggle_checkbox(e, checkbox, name):
        checkbox.value = not checkbox.value
        checkbox.update()
        on_checkbox_change(checkbox, name)

    gos_seal_checkbox = ft.Ref[ft.Checkbox]()
    meter_integrity_checkbox = ft.Ref[ft.Checkbox]()
    mechanic_defect_checkbox = ft.Ref[ft.Checkbox]()
    have_cracks_holes_checkbox = ft.Ref[ft.Checkbox]()
    glass_indicator_checkbox = ft.Ref[ft.Checkbox]()
    indicators_checkbox = ft.Ref[ft.Checkbox]()
    star_spin_checkbox = ft.Ref[ft.Checkbox]()
    visual_litr_checkbox = ft.Ref[ft.Checkbox]()

    dict_checkboxes["seal"] = True
    dict_checkboxes["meter_integrity"] = True  # целостность счетчика
    dict_checkboxes["mechanic_defect"] = True  # механические повреждения
    dict_checkboxes["have_cracks_holes"] = True  # отверстий или трещин
    dict_checkboxes["glass_indicator"] = True  # Плотное прилегание стекла индикатора
    dict_checkboxes["indicators"] = True  # короче буква д или 5 пункт
    dict_checkboxes["star_spin"] = True  # вращение звездочки
    dict_checkboxes["visual_litr"] = True  # визуалный отчет литров

    meter_integrity_checkbox_container = scr.func.create_checkbox_with_wrapped_text(
        "Прибор учета ", "цел", "?",
        meter_integrity_checkbox,
        on_checkbox_change,
        toggle_checkbox,
        name="meter_integrity"
    )

    mechanic_defect_checkbox_container = scr.func.create_checkbox_with_wrapped_text(
        "Нет ли у прибора учета ", "механических повреждений", "?",
        mechanic_defect_checkbox,
        on_checkbox_change,
        toggle_checkbox,
        name="mechanic_defect"
    )

    have_cracks_holes_checkbox_container = scr.func.create_checkbox_with_wrapped_text(
        "Отстутствуют ли не предусмотренные изготовителем ", "отверстия или трещины", "?",
        have_cracks_holes_checkbox,
        on_checkbox_change,
        toggle_checkbox,
        name="have_cracks_holes"
    )

    glass_indicator_checkbox_container = scr.func.create_checkbox_with_wrapped_text(
        "Стекло индикатора прилегает ", "плотно", "?",
        glass_indicator_checkbox,
        on_checkbox_change,
        toggle_checkbox,
        name="glass_indicator"
    )

    indicators_checkbox_container = scr.func.create_checkbox_with_wrapped_text(
        "Присутствуют и сохраненны ли ", "контрольные пломбы и индикаторы антимагнитных пломб, и других"
                                         " устройств, позволяющих фиксировать факт вмешательства", "?",
        indicators_checkbox,
        on_checkbox_change,
        toggle_checkbox,
        name="indicators"
    )

    star_spin_checkbox_container = scr.func.create_checkbox_with_wrapped_text(
        "Сигнальная звездочка вращается ", "равномерно", "?",
        star_spin_checkbox,
        on_checkbox_change,
        toggle_checkbox,
        name="star_spin"
    )

    visual_litr_checkbox_container = scr.func.create_checkbox_with_wrapped_text(
        "Производится ли ", "визуальный отсчет литров", "?",
        visual_litr_checkbox,
        on_checkbox_change,
        toggle_checkbox,
        name="visual_litr"
    )

    gos_seal_checkbox_container = scr.func.create_checkbox_with_wrapped_text(
        "Есть ли пломба ", "госповерителя", "?",
        gos_seal_checkbox,
        on_checkbox_change,
        toggle_checkbox,
        name="seal"
    )

    content = ft.Column(
        [
            meter_integrity_checkbox_container,
            mechanic_defect_checkbox_container,
            have_cracks_holes_checkbox_container,
            glass_indicator_checkbox_container,
            indicators_checkbox_container,
            gos_seal_checkbox_container,
            star_spin_checkbox_container,
            visual_litr_checkbox_container
        ],
        width=screen_width * 0.95,
        expand=True,
        scroll=ft.ScrollMode.AUTO
    )

    def button_yes(e):
        chect_list = [name for name, is_checked in dict_checkboxes.items() if not is_checked]
        message_string = ""
        act_string = ""
        not_working = 0
        if not chect_list:
            page.close(check_meters_data)
        for chect in chect_list:
            if chect == "seal":
                message_string += "Включите в акт отсутствие пломбы госповерителя\n"
                act_string += f"Отсутствие пломбы госповерителя {meter_number},"
                not_working += 1
            elif chect == "meter_integrity":
                message_string += "Включите в акт проблемы с целостностью счетчика\n"
                act_string += f"Проблемы целостности прибора {meter_number},"
                not_working += 1
            elif chect == "mechanic_defect":
                message_string += "Включите в акт факт о наличии механических повреждений\n"
                act_string += f"Наличие механических повреждений {meter_number},"
                not_working += 1
            elif chect == "have_cracks_holes":
                message_string += "Включите в акт факт наличия отверстий и трещин\n"
                act_string += f"Наличие отверстий и трещин {meter_number},"
                not_working += 1
            elif chect == "glass_indicator":
                message_string += "Включите в акт неплотное прилегание стекла индикатора\n"
                act_string += f"Неплотное прилегание стекла индикатора {meter_number},"
                not_working += 1
            elif chect == "indicators":
                message_string += "Включите в акт отсутствие или порчу устройств фиксирующих вмешательство\n"
                act_string += f"Отсутствие или порча устройств фиксирующих вмешательство {meter_number},"
            elif chect == "star_spin":
                message_string += "Включите в акт информацию о неравномерном вращении сигнальной звездочки\n"
                act_string += f"Неравномерное вращение сигнальной звездочки {meter_number},"
                not_working += 1
            elif chect == "visual_litr":
                message_string += "Включите в акт информацию о непроизводимости визульного отсчета литров\n"
                act_string += f"Непроизводимость визульного отсчета литров {meter_number},"
                not_working += 1
        if bool(act_string):
            if not_working != 0:
                meter = f"{meter_number},"
            else:
                meter = ""
            scr.BD.bd_users.local.update_bd.update_acts_insert_meters(id_task, act_string, meter)

        def on_button_yes(e):
            page.close(bs)
            scr.navigation_apps.users.doing_work.photo_not_working_meters.add_photo(page, id_task, container1, meter_id)

        bs = ft.AlertDialog(
            modal=True,
            title=ft.Text("Предупреждение"),
            content=ft.Text(message_string),
            actions=[
                ft.Row(
                    [
                        ft.ElevatedButton("ОК", on_click=on_button_yes)
                    ], alignment=ft.MainAxisAlignment.CENTER)
            ],
        )
        if message_string != "":
            page.open(bs)
        else:
            if failure:
                scr.navigation_apps.users.doing_work.photo_not_working_meters.add_photo(page, id_task, container1,
                                                                                        meter_id)
            else:
                if purpose == "съем":
                    scr.navigation_apps.users.doing_work.update_data_meters.update_data(page, meter_id, id_task,
                                                                                        container1)
                elif purpose == "новый":
                    scr.navigation_apps.users.doing_work.create_new_meters.create_meter(page, id_task,
                                                                                        container1)
                else:
                    scr.navigation_apps.users.doing_work.sealing_meter.sealing(page, id_task, meter_id,
                                                                               container1)
        page.update()
        page.close(check_meters_data)

    def button_no(e):
        page.close(check_meters_data)
        scr.navigation_apps.users.doing_work.chose_meters.show_meters_data(page, id_task, container1)

    check_meters_data = ft.AlertDialog(
        modal=True,
        content=content,
        title=ft.Text("Проверка состояния прибора учета"),
        actions=[
            ft.Row(
                [
                    ft.ElevatedButton("Да", on_click=button_yes, bgcolor=ft.colors.BLUE_300, color=ft.Colors.BLACK87),
                    ft.ElevatedButton("Назад", on_click=button_no, bgcolor=ft.colors.BLUE_300, color=ft.Colors.BLACK87),
                ], alignment=ft.MainAxisAlignment.CENTER
            )
        ],
        inset_padding=screen_width * 0.05
    )
    page.open(check_meters_data)
    page.update()


# при новом счетчике передавать "новый"
def commissioning_meters(page, id_task, container1, meter_id="", purpose=""):
    screen_width = page.window_width
    meter_number = "Неизвестный прибор учета" if meter_id == "" else meter_id

    dict_checkboxes = {}

    def on_checkbox_change(checkbox, name):
        dict_checkboxes[name] = checkbox.value

    def toggle_checkbox(e, checkbox, name):
        checkbox.value = not checkbox.value
        checkbox.update()
        on_checkbox_change(checkbox, name)

    serial_number_checkbox = ft.Ref[ft.Checkbox]()  #
    installation_checkbox = ft.Ref[ft.Checkbox]()  #
    pasport_checkbox = ft.Ref[ft.Checkbox]()  #
    schema_checkbox = ft.Ref[ft.Checkbox]()  #
    last_check_checkbox = ft.Ref[ft.Checkbox]()  #
    seal_gos_checkbox = ft.Ref[ft.Checkbox]()  #
    dovodomernye_vrezki_checkbox = ft.Ref[ft.Checkbox]()  #
    utechki_do_meter_checkbox = ft.Ref[ft.Checkbox]()  #

    dict_checkboxes["serial_number"] = True
    dict_checkboxes["installation"] = True
    dict_checkboxes["pasport"] = True
    dict_checkboxes["schema"] = True
    dict_checkboxes["last_check"] = True if purpose != "новый" else True  # заготовка на отключение всех галочек
    dict_checkboxes["seal_gos"] = True
    dict_checkboxes["dovodomernye_vrezki"] = True
    dict_checkboxes["utechki_do_meter"] = True

    pasport_checkbox_container = scr.func.create_checkbox_with_wrapped_text(
        "Есть ли ", "оригинал паспорта ", "прибора учета?",
        pasport_checkbox,
        on_checkbox_change,
        toggle_checkbox,
        name="pasport"
    )

    schema_checkbox_container = scr.func.create_checkbox_with_wrapped_text(
        "Соответствует ли ", "типовой схеме узла", "?",
        schema_checkbox,
        on_checkbox_change,
        toggle_checkbox,
        name="schema"
    )

    last_check_checkbox_container = scr.func.create_checkbox_with_wrapped_text(
        "Есть ли на приборе учета ", "знаки последней поверки", "?",
        last_check_checkbox,
        on_checkbox_change,
        toggle_checkbox,
        name="last_check"
    )

    seal_gos_checkbox_container = scr.func.create_checkbox_with_wrapped_text(
        "Есть ли на приборе учета ", "пломба госповерителя ", "(согласно паспорту)?",
        seal_gos_checkbox,
        on_checkbox_change,
        toggle_checkbox,
        name="seal_gos"
    )

    dovodomernye_vrezki_checkbox_container = scr.func.create_checkbox_with_wrapped_text(
        "Есть ли ", "доводомерные врезки", "?",
        dovodomernye_vrezki_checkbox,
        on_checkbox_change,
        toggle_checkbox,
        name="dovodomernye_vrezki"
    )

    utechki_do_meter_checkbox_container = scr.func.create_checkbox_with_wrapped_text(
        "Есть ли ", "утечки до ", "прибора учета?",
        utechki_do_meter_checkbox,
        on_checkbox_change,
        toggle_checkbox,
        name="utechki_do_meter"
    )

    serial_number_checkbox_container = scr.func.create_checkbox_with_wrapped_text(
        "Заводской номер на приборе учета ",
        "совпадает с указанным ",
        "в паспорте?",
        serial_number_checkbox,
        on_checkbox_change,
        toggle_checkbox,
        name="serial_number"
    )

    installation_checkbox_container = scr.func.create_checkbox_with_wrapped_text(
        "Прибор учета устрановлен ", "по потоку", "?",
        installation_checkbox,
        on_checkbox_change,
        toggle_checkbox,
        name="installation"
    )

    content_question = ft.Column(
        [
            pasport_checkbox_container,
            serial_number_checkbox_container,
            schema_checkbox_container,
            last_check_checkbox_container if purpose != "новый" else ft.Text(visible=False),
            seal_gos_checkbox_container,
            installation_checkbox_container,
            dovodomernye_vrezki_checkbox_container,
            utechki_do_meter_checkbox_container
        ],
        width=screen_width * 0.95
    )

    def button_yes(e):
        chect_list = [name for name, is_checked in dict_checkboxes.items() if not is_checked]
        message_string = ""
        act_string = ""
        failure = False
        if not chect_list:
            page.close(check_meters_data)
        for chect in chect_list:
            if chect == "serial_number":
                message_string += "Включите в акт несоответствие Заводского номера\n"
                act_string += f"Несоответствие Заводского номера {meter_number},"
            elif chect == "installation":
                message_string += "Включите в акт информацию об установке прибора учета не по потоку\n"
                act_string += f"Установлен не по потоку {meter_number},"
            elif chect == "pasport":
                message_string += "Включите в акт отсутствие оригинала паспорта\n"
                act_string += f"Отсутствие оригинала паспорта {meter_number},"
                failure = True
            elif chect == "schema":
                message_string += "Включите в акт несоответствие типовой схеме узла\n"
                act_string += f"Схема узла не соответствие типовой схеме узла {meter_number},"
                failure = True
            elif chect == "last_check":
                message_string += "Включите в акт отсутствие знаков последней проверки\n"
                act_string += f"Отсутствие пзнаков последней проверки {meter_number},"
            elif chect == "seal_gos":
                message_string += "Включите в акт отсутствие пломбы госповерителя\n"
                act_string += f"Отсутствие пломбы госповерителя {meter_number},"
            elif chect == "dovodomernye_vrezki":
                message_string += "Включите в акт наличие доводомерных врезок\n"
                act_string += f"Наличие доводомерных врезок {meter_number},"
            elif chect == "utechki_do_meter":
                message_string += "Включите в акт наличие утечек до прибора учета\n"
                act_string += f"Наличие утечек до прибора учета {meter_number},"
        if bool(act_string):
            if failure:
                meter = f"{meter_number},"
            else:
                meter = ""
            scr.BD.bd_users.local.update_bd.update_acts_insert_meters(id_task, act_string, meter)

        def on_button_yes(e):
            page.close(bs)
            update_data_check(page, id_task, container1, meter_number, purpose, failure)

        bs = ft.AlertDialog(
            modal=True,
            title=ft.Text("Предупреждение"),
            content=ft.Text(message_string),
            actions=[
                ft.Row(
                    [
                        ft.ElevatedButton("ОК", on_click=on_button_yes)
                    ], alignment=ft.MainAxisAlignment.CENTER)
            ],
        )
        if message_string != "":
            page.open(bs)
        else:
            update_data_check(page, id_task, container1, meter_number, purpose)
        page.update()
        page.close(check_meters_data)

    def button_no(e):
        page.close(check_meters_data)
        scr.navigation_apps.users.doing_work.chose_meters.show_meters_data(page, id_task, container1)

    check_meters_data = ft.AlertDialog(
        modal=True,
        content=content_question,
        title=ft.Text("Проверка пригодности ввода в эксплуатацию"),
        actions=[
            ft.Row(
                [
                    ft.ElevatedButton("Ввод прибора учета",
                                      on_click=button_yes,
                                      bgcolor=ft.colors.BLUE_300,
                                      color=ft.Colors.BLACK87
                                      ),
                    ft.ElevatedButton("Назад",
                                      on_click=button_no,
                                      bgcolor=ft.colors.RED_300,
                                      color=ft.Colors.BLACK87),
                ], alignment=ft.MainAxisAlignment.CENTER
            )
        ],
        inset_padding=screen_width * 0.05
    )

    page.open(check_meters_data)
    page.update()
