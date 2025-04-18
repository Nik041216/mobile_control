import datetime
import flet as ft
import scr.BD.bd_users.local.select_bd as select_bd
import scr.BD.bd_users.bd_server_user as bd_server_user
import scr.constants as const
import scr.func
import scr.navigation_apps.users.doing_work.alert_check_data as check_alert
import scr.BD.bd_users.bd_server_user
from scr.components.search_field import SearchField

statuses = ['не выполнен', 'выполнен', 'в исполнении', 'просрочен']
status_icons = {
    'не выполнен': (ft.icons.HOURGLASS_EMPTY, ft.colors.BLUE),
    'в исполнении': (ft.icons.BUILD_OUTLINED, '#ffc107'),
    'выполнен': (ft.icons.CHECK_CIRCLE_OUTLINE, ft.colors.GREEN),
    'просрочен': (ft.icons.ERROR_OUTLINE, ft.colors.RED),
}
sorting = "Адрес"
menu_visible = False
column = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)


def get_appbar(page):
    checkboxes = {}

    def reset_filters(e):
        global statuses
        statuses = list(status_icons.keys())  # Восстанавливаем все статусы
        update_checkboxes()
        get_content(page)
        page.update()

    def filtration_check(e, text):
        global statuses
        if e.control.value:
            if text not in statuses:
                statuses.append(text)
        else:
            if text in statuses:
                statuses.remove(text)
        update_results(statuses, page, search_value="")
        page.update()

    def update_checkboxes():
        """Обновляет состояние чекбоксов в зависимости от массива `statuses`."""
        for text, checkbox in checkboxes.items():
            checkbox.value = text in statuses  # Устанавливаем значение из массива статусов
        page.update()

    def create_checkboxes():
        """Создаёт чекбоксы, привязывая их к массиву `statuses`."""
        rows = []
        count = select_bd.select_count_task("now")
        for status, (icon, color) in status_icons.items():
            checkbox = ft.Checkbox(label=f"{status.capitalize()} ({count[status]})",
                                   value=status in statuses,
                                   on_change=lambda e, s=status: filtration_check(e, s),
                                   label_style=ft.TextStyle(size=15, )
                                   )
            checkboxes[status] = checkbox
            rows.append(ft.Row([ft.Icon(icon, size=25, color=color), checkbox],
                               alignment=ft.MainAxisAlignment.START))
        return rows

    def toggle_drawer(page):
        global menu_visible
        menu_visible = not menu_visible
        menu_container.visible = menu_visible
        overlay_container.visible = menu_visible
        page.update()

    overlay_container = ft.Container(
        visible=False,
        bgcolor=ft.colors.BLACK54,
        expand=True,
        alignment=ft.alignment.center,
        on_click=lambda _: toggle_drawer(page)
    )

    def on_click_upload(e):
        if scr.func.check_internet():
            bd_server_user.upload_data_to_server(page)
        else:
            scr.func.show_alert_yn(page, "Нет доступа к сети, проверьте интернет соединение")

    menu_container = ft.Container(
        visible=False,
        width=250,
        height=page.window_height,
        bgcolor=ft.colors.BLUE_50,
        padding=20,
        animate=ft.animation.Animation(400, ft.AnimationCurve.DECELERATE),
        content=ft.Column([
            ft.Text("Фильтры", size=20, weight=ft.FontWeight.BOLD),
            *create_checkboxes(),
            ft.Container(expand=True),
            ft.Row([ft.ElevatedButton("Сбросить фильтры",
                                      on_click=reset_filters,
                                      bgcolor=ft.colors.RED_400,
                                      icon=ft.icons.FILTER_ALT_OFF,
                                      color=ft.colors.WHITE)]),
            ft.Row([ft.ElevatedButton("Отгрузить все данные",
                                      on_click=on_click_upload,
                                      icon="BACKUP_ROUNDED",
                                      bgcolor=ft.colors.BLUE_400,
                                      color=ft.colors.WHITE)]),
        ], expand=True),
    )

    def on_click_update(page):
        global statuses
        statuses = list(status_icons.keys())  # Сброс фильтра

        # Обновляем данные задач
        get_content(page)

        # Пересоздаём чекбоксы с актуальными данными
        new_checkboxes = create_checkboxes()

        # Перезаписываем содержимое меню
        menu_container.content.controls = ft.Column([
            ft.Text("Фильтры", size=20, weight=ft.FontWeight.BOLD),
            *new_checkboxes,
            ft.Container(expand=True),
            ft.Row([ft.ElevatedButton("Сбросить фильтры",
                                      on_click=reset_filters,
                                      bgcolor=ft.colors.RED_400,
                                      icon=ft.icons.FILTER_ALT_OFF,
                                      color=ft.colors.WHITE)]),
            ft.Row([ft.ElevatedButton("Отгрузить все данные",
                                      on_click=on_click_upload,
                                      icon="BACKUP_ROUNDED",
                                      bgcolor=ft.colors.BLUE_400,
                                      color=ft.colors.WHITE)]),
        ], expand=True).controls

        page.update()

    page.overlay.append(overlay_container)
    page.overlay.append(menu_container)

    return ft.AppBar(
        title=ft.Text("Будующие задачи"),
        center_title=True,
        toolbar_height=50,
        leading=ft.IconButton(icon=ft.icons.MENU, on_click=lambda _: toggle_drawer(page), tooltip="Меню фильтров"),
        bgcolor=ft.colors.BLUE_100,
        actions=[ft.IconButton(icon=ft.icons.AUTORENEW, on_click=lambda _: on_click_update(page),
                               tooltip="Обновить список заданий")]
    )


def get_content(page):
    container = ft.Container(expand=True)
    user_main(page, container)
    return container


def update_results(filter_statuses, page, search_value):
    screen_width = page.window_width
    completed_icon = ft.Icon(ft.icons.CHECK_CIRCLE_OUTLINE)
    failed_icon = ft.Icon(ft.icons.ERROR_OUTLINE)
    pending_icon = ft.Icon(ft.icons.HOURGLASS_EMPTY)
    unloaded_icon = ft.Icon(ft.icons.BUILD)

    def create_task_container(result):
        id_task, _, _, _, street, dom, apartment, phone, _, date, date_end, _, status, purpose, *_ = result
        date_reverse = scr.func.reverse_date(date)
        date_end_reverse = scr.func.reverse_date(date_end)

        stat = ft.Row([ft.Text(f"Статус: {status}")])

        if status == 'выполнен':
            stat.controls.append(completed_icon)
            color = const.tasks_completed_color
        elif status == 'в исполнении':
            stat.controls.append(unloaded_icon)
            color = const.tasks_unloaded_color
        elif status == 'не выполнен':
            stat.controls.append(pending_icon)
            color = ft.colors.BLUE
        elif status == 'просрочен':
            stat.controls.append(failed_icon)
            color = ft.Colors.RED

        result_info = ft.Column([
            ft.Text(f"ул.{street} д.{dom} кв.{apartment}", weight=ft.FontWeight.BOLD),
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
                on_click=on_click_container
            ),
            elevation=2
        )

    def date_change_picker(e):
        new_date.value = str(date_picker.value.date())
        new_date.update()

    date_picker = ft.DatePicker(cancel_text="Отмена",
                                confirm_text="Выбрать",
                                error_format_text="Не правильный формат даты",
                                field_hint_text="дд.мм.гггг",
                                field_label_text="Введите дату",
                                help_text="Выберете дату",
                                last_date=datetime.date(year=2300, month=1, day=1),
                                on_change=date_change_picker)
    new_date = ft.TextField(
        label="Новая дата",
        suffix=ft.IconButton(icon=ft.icons.CALENDAR_MONTH,
                             on_click=lambda _: page.open(date_picker))
    )

    page.overlay.append(date_picker)
    results = scr.BD.bd_users.local.select_bd.select_tasks_data_new(sorting, search_value, "future")
    if filter_statuses:
        filtered_results = [result for result in results if result[12] in filter_statuses]
    else:
        filtered_results = [
            result for result in results
        ]

    column.controls.clear()

    # Словарь для хранения задач по датам и улицам
    tasks_by_date = {}

    panel_list = ft.ExpansionPanelList(
        elevation=25,
        expanded_header_padding=3
    )

    for result in filtered_results:
        id_task, fio, district, hamlet, street, dom, apartment, phone_number, \
            personal_account, date, date_end, remark_task, status, purpose, \
            registered_residing, standarts, area, saldo = result

        if date:
            date = scr.func.reverse_date(date)
        if date_end:
            date_end = scr.func.reverse_date(date_end)

        # Проверяем, существует ли уже ключ для этой даты, если нет - создаем
        if date not in tasks_by_date:
            tasks_by_date[date] = {}

        # Проверяем, существует ли уже ключ для этой улицы внутри даты, если нет - создаем
        if street not in tasks_by_date[date]:
            tasks_by_date[date][street] = []

        if status == 'выполнен':
            color = const.tasks_completed_color
        elif status == 'в_исполнении':
            color = const.tasks_unloaded_color
        else:
            color = const.tasks_pending_color

        result_info = f"ул.{street} д.{dom} кв.{apartment}"
        row = ft.Column(
            [
                ft.Text(result_info, size=17, color=const.tasks_text_color),
                ft.Text(f"{phone_number}")
            ]
        )

        def viewing(e, id_task):
            def on_click(e):
                page.close(view)

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
            result_info_address = f"Адрес: ул.{street} д.{dom} кв.{apartment}"
            result_info_person = f"ФИО владельца: {person_name}"
            view = ft.AlertDialog(
                modal=True,
                title=ft.Text(result_info_address),
                content=ft.Column(
                    [
                        ft.Text(f"Лицевой счет: {personal_account}"),
                        ft.Text(f"{result_info_person}"),
                        ft.Text(f"Номер телефона: {phone_number}"),
                        ft.Text(f"Тип адресса: {type_address}"),
                        ft.Text(f"Дата начала выполнения: {date}"),
                        ft.Text(f"Конечная дата выполнения: {date_end}"),
                        ft.Text(f"Тип задания: {purpose}"),
                        ft.Text(f"Количество прописанных: {registered_residing}"),
                        ft.Text(f"Нормативы: {standarts}"),
                        ft.Text(f"Площадь: {area}"),
                    ],
                    width=screen_width * 0.95
                ),
                actions=[
                    ft.Row(
                        [
                            ft.ElevatedButton("Назад", on_click=on_click, bgcolor=ft.colors.RED_200)
                        ], alignment=ft.MainAxisAlignment.CENTER
                    )
                ],
                inset_padding=screen_width * 0.05
            )
            page.open(view)

        def reschedule_to_another_date(e, id_task, date):

            def on_click(e):
                current_date = datetime.datetime.now().strftime('%Y-%m-%d')
                if date_picker.value and date_picker.value.date() <= datetime.datetime.strptime(current_date, '%Y-%m-%d').date():
                    new_date.error_text = "Задание не может быть перенесено\n на сегодня"
                elif date_picker.value.date() > datetime.datetime.strptime(date_end, '%Y-%m-%d').date():
                    new_date.error_text = "Обговорите такой перенос с мастером"
                else:
                    new_date.value = date_picker.value.date()
                    scr.BD.bd_users.local.update_bd.update_date(id_task, new_date.value)
                    update_results(filter_statuses, page, search_value)
                    page.close(change_date)
                page.update()
                new_date.update()

            def close(e):
                page.close(change_date)

            new_date.value = date
            change_date = ft.AlertDialog(
                title=ft.Text("Перенести задание на другой день"),
                content=ft.Column(
                    [
                        ft.Text(f"Старая дата: {date}"),
                        new_date
                    ],
                    width=screen_width * 0.95,
                    expand=True
                ),
                actions=[
                    ft.Row(
                        [
                            ft.ElevatedButton("Подтвердить",
                                              on_click=on_click,
                                              bgcolor=ft.colors.BLUE_200,
                                              width=page.window_width * 0.30),
                            ft.ElevatedButton("Назад",
                                              on_click=close,
                                              bgcolor=ft.colors.BLUE_200,
                                              width=page.window_width * 0.30)
                        ], alignment=ft.MainAxisAlignment.CENTER
                    )
                ],
                inset_padding=screen_width * 0.05
            )

            page.open(change_date)
            page.update()

        # Используем замыкание для передачи правильного id_task + выбор действия
        def create_on_click(id_task, date):
            def on_click(e):
                page.close(chose_action)
                check_alert.func_check_address_data(page, id_task, where="future")

            chose_action = ft.AlertDialog(
                title=ft.Text("Вы хотите просмотреть данные или выполнить задание?"),
                content=ft.Row(width=screen_width * 0.95),
                actions=[
                    ft.Column([
                        ft.Row(
                            [
                                ft.ElevatedButton("Просмотреть",
                                                  on_click=lambda e: viewing(e, id_task),
                                                  bgcolor=ft.colors.BLUE_200,
                                                  width=page.window_width * 0.35),
                                ft.ElevatedButton("Выполнить",
                                                  on_click=on_click,
                                                  bgcolor=ft.colors.BLUE_200,
                                                  width=page.window_width * 0.30)
                            ], alignment=ft.MainAxisAlignment.CENTER
                        ),
                        ft.Row(
                            [
                                ft.ElevatedButton("Перенос задания",
                                                  on_click=lambda e: reschedule_to_another_date(e, id_task,
                                                                                                date),
                                                  bgcolor=ft.colors.BLUE_200),
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

        on_click_container = create_on_click(id_task, date)

        task_container = create_task_container(result)

        # Добавляем контейнер с задачей в соответствующий список по улице
        tasks_by_date[date][street].append(task_container)

    # Создаем раскрывающиеся панели по датам
    for date, streets in tasks_by_date.items():
        street_panel_list = ft.ExpansionPanelList(
            elevation=10,
            expanded_header_padding=3
        )

        # Создаем раскрывающиеся панели по улицам для каждой даты
        for street, tasks in streets.items():
            street_panel = ft.ExpansionPanel(
                header=ft.Text(f"{street}"),
                content=ft.Column(tasks, scroll=ft.ScrollMode.AUTO),  # Добавляем список задач в панель
                expanded=True,
                can_tap_header=True
            )
            street_panel_list.controls.append(street_panel)

        # Добавляем панель с улицами в панель по дате
        date_panel = ft.ExpansionPanel(
            header=ft.Text(f"{date}"),
            content=street_panel_list,  # Добавляем список улиц в панель по дате
            expanded=True,
            can_tap_header=True
        )
        panel_list.controls.append(date_panel)

    # Обновляем содержимое колонки
    column.controls.clear()
    column.controls.append(panel_list)
    page.update()


def user_main(page: ft.Page, container: ft.Container):
    global statuses, column
    page.window_width = 362.4
    page.window_height = 800
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.floating_action_button = None

    search_field = SearchField(on_change=lambda _: update_results(statuses, page, search_bar.value),
                               on_submit=lambda _: update_results(statuses, page, search_bar.value))
    search_bar = search_field.create_search_field()

    update_results(statuses, page, search_bar.value)

    content = ft.Stack([
        ft.Column([
            ft.ResponsiveRow(
                [
                    ft.ResponsiveRow(
                        [
                            search_bar,
                            ft.Dropdown(
                                on_change=lambda e: globals().update(sorting=e.control.value) or update_results(
                                    statuses, page, search_bar.value),
                                value=sorting,
                                label="Сортировка",
                                options=
                                [
                                    ft.dropdown.Option("Адрес"),
                                    ft.dropdown.Option("Статус"),
                                    ft.dropdown.Option("Дата")
                                ],
                                col=1.8,
                                bgcolor=ft.colors.WHITE
                            )
                        ],
                        columns=5
                    ),
                ],
                columns=4,
                spacing=5,
                alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.Container(
                content=column,
                expand=True,
            ),
        ], expand=True),
    ], expand=True)

    container.content = content
    page.update()
