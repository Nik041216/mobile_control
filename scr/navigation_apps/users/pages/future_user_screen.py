import datetime
import flet as ft
import scr.BD.bd_users.local.update_bd
import scr.BD.bd_users.local.delete_bd
import scr.BD.bd_users.local.insert_bd
import scr.BD.bd_users.local.select_bd
import scr.BD.bd_users.bd_server_user
import scr.toggle_user_sessions
import scr.func
import scr.constants as const
import scr.navigation_apps.users.doing_work.chose_meters
from scr.components.search_field import SearchField

statuses = []
sorting = "Дата"


def recall_main(page):
    main(page)


def main(page):
    page.update()
    page.controls.clear()
    screen_width = page.width
    screen_height = page.height
    page.vertical_alignment = ft.MainAxisAlignment.START
    global statuses, sorting

    page.floating_action_button = None


    def on_click_update(e):
        statuses.clear()
        unloaded_icon.color = ft.colors.WHITE
        unloaded_tasks_container.shadow.color = ft.colors.BLACK38
        pending_icon.color = ft.colors.WHITE
        pending_tasks_container.shadow.color = ft.colors.BLACK38
        failed_icon.color = ft.colors.WHITE
        failed_tasks_container.shadow.color = ft.colors.BLACK38
        completed_icon.color = ft.colors.WHITE
        completed_tasks_container.shadow.color = ft.colors.BLACK38

        scr.BD.bd_users.bd_server_user.select_task_data_for_update(page)
        update_results()
        page.update()

    page.appbar = ft.AppBar(
        title=ft.Text("Будущие задачи"),
        center_title=True,
        toolbar_height=40,
        bgcolor=ft.colors.BLUE_GREY_50,
        actions=[
            ft.IconButton(icon=ft.icons.AUTORENEW, on_click=on_click_update)
        ]
    )
    page.update()

    completed_icon = ft.Icon(ft.icons.TASK_ALT, color=ft.colors.WHITE)
    failed_icon = ft.Icon(ft.icons.ERROR_OUTLINE, color=ft.colors.WHITE)
    pending_icon = ft.Icon(ft.icons.HOURGLASS_EMPTY, color=ft.colors.WHITE)
    unloaded_icon = ft.Icon(ft.icons.BUILD, color=ft.colors.WHITE)

    def filtration(e, color, text):
        global statuses
        if text not in statuses:
            if color == ft.colors.WHITE:
                statuses.append(text)
                if text == 'выполнен':
                    completed_icon.color = ft.colors.BLACK
                    completed_tasks_container.shadow.color = const.tasks_completed_text_color
                    update_results(filter_statuses=statuses)
                elif text == 'просрочен':
                    failed_icon.color = ft.colors.BLACK
                    failed_tasks_container.shadow.color = const.tasks_failed_text_color
                    update_results(filter_statuses=statuses)
                elif text == 'не выполнен':
                    pending_icon.color = ft.colors.BLACK
                    pending_tasks_container.shadow.color = ft.colors.BLACK54
                    update_results(filter_statuses=statuses)
                elif text == 'в_исполнении':
                    unloaded_icon.color = ft.colors.BLACK
                    unloaded_tasks_container.shadow.color = const.tasks_unloaded_text_color
                    update_results(filter_statuses=statuses)
        else:
            if color != ft.colors.WHITE:
                statuses.remove(text)
                if text == 'выполнен':
                    completed_icon.color = ft.colors.WHITE
                    completed_tasks_container.shadow.color = ft.colors.BLACK38
                    update_results(filter_statuses=statuses)
                elif text == 'просрочен':
                    failed_icon.color = ft.colors.WHITE
                    failed_tasks_container.shadow.color = ft.colors.BLACK38
                    update_results(filter_statuses=statuses)
                elif text == 'невыполнен':
                    pending_icon.color = ft.colors.WHITE
                    pending_tasks_container.shadow.color = ft.colors.BLACK38
                    update_results(filter_statuses=statuses)
                elif text == 'в_исполнении':
                    unloaded_icon.color = ft.colors.WHITE
                    unloaded_tasks_container.shadow.color = ft.colors.BLACK38
                    update_results(filter_statuses=statuses)

    completed_tasks_container = scr.func.create_filter_button(
        completed_icon,
        const.tasks_completed_text_color,
        'выполнен',
        filtration
    )
    failed_tasks_container = scr.func.create_filter_button(
        failed_icon,
        const.tasks_failed_text_color,
        'просрочен',
        filtration
    )
    pending_tasks_container = scr.func.create_filter_button(
        pending_icon,
        const.tasks_pending_text_color,
        'не выполнен',
        filtration
    )
    unloaded_tasks_container = scr.func.create_filter_button(
        unloaded_icon,
        const.tasks_unloaded_text_color,
        'в_исполнении',
        filtration
    )

    def on_search_change(e):
        update_results(statuses)

    def on_search_submit(e):
        update_results(statuses)

    search_field = SearchField(on_change=on_search_change, on_submit=on_search_submit)
    search_bar = search_field.create_search_field()

    def update_results(filter_statuses=None):

        def date_change_picker(e):
            new_date.value = str(date_picker.value.date())
            new_date.update()

        date_picker = ft.DatePicker(cancel_text="Отмена",
                                    confirm_text="Выбрать",
                                    error_format_text="Не правильный формат даты",
                                    field_hint_text="дд.мм.гггг",
                                    field_label_text="Введите дату",
                                    help_text="Выберете дату",
                                    last_date=datetime.datetime(year=2300, month=1, day=1),
                                    on_change=date_change_picker)
        new_date = ft.TextField(
            label="Новая дата",
            suffix=ft.IconButton(icon=ft.icons.CALENDAR_MONTH,
                                 on_click=lambda _: page.open(date_picker))
        )

        page.overlay.append(date_picker)
        search_value = search_bar.value
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
                        personal_account, date, remark, status, purpose, registered_residing, \
                        status_address, standarts, area, saldo, type_address = result
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
                            ft.Text(f"Дата выполнения: {date}"),
                            ft.Text(f"Тип задания: {purpose}"),
                            ft.Text(f"Количество прописанных: {registered_residing}"),
                            ft.Text(f"Нормативы: {standarts}"),
                            ft.Text(f"Площадь: {area}"),
                        ]
                    ),
                    actions=[
                        ft.Row(
                            [
                                ft.ElevatedButton("Назад", on_click=on_click, bgcolor=ft.colors.RED_200)
                            ], alignment=ft.MainAxisAlignment.CENTER
                        )
                    ],
                )
                page.open(view)

            def reschedule_to_another_date(e, task_id, date):

                def on_click(e):
                    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
                    if date_picker.value.date() <= datetime.datetime.strptime(current_date, '%Y-%m-%d').date():
                        new_date.error_text = "Задание не может быть перенесено на сегодня"
                    elif date_picker.value.date() > datetime.datetime.strptime(date_end, '%Y-%m-%d').date():
                        new_date.error_text = "Обговорите такой перенос с мастером"
                    else:
                        new_date.value = date_picker.value.date()
                        scr.BD.bd_users.local.update_bd.update_date(id_task, new_date.value)
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
                        ]
                    ),
                    actions=[
                        ft.Row(
                            [
                                ft.ElevatedButton("Подтвердить",
                                                  on_click=on_click,
                                                  bgcolor=ft.colors.BLUE_200,
                                                  width=screen_width * 0.30),
                                ft.ElevatedButton("Назад",
                                                  on_click=close,
                                                  bgcolor=ft.colors.BLUE_200,
                                                  width=screen_width * 0.30)
                            ], alignment=ft.MainAxisAlignment.CENTER
                        )
                    ]
                )

                page.open(change_date)
                page.update()

            # Используем замыкание для передачи правильного id_task + выбор действия
            def create_on_click(id_task, date):
                def show(e):
                    page.open(
                        ft.AlertDialog(
                            title=ft.Text("Вы хотите просмотреть данные или выполнить задание?"),
                            actions=[
                                ft.Row(
                                    [
                                        ft.ElevatedButton("Просмотреть",
                                                          on_click=lambda e: viewing(e, id_task),
                                                          bgcolor=ft.colors.BLUE_200,
                                                          width=screen_width * 0.35),
                                        ft.ElevatedButton("Выполнить",
                                                          on_click=on_click,
                                                          bgcolor=ft.colors.BLUE_200,
                                                          width=screen_width * 0.30)
                                    ], alignment=ft.MainAxisAlignment.CENTER
                                ),
                                ft.Row(),
                                ft.Row(
                                    [
                                        ft.ElevatedButton("Перенос задания",
                                                          on_click=lambda e: reschedule_to_another_date(e, id_task,
                                                                                                        date),
                                                          bgcolor=ft.colors.BLUE_200),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER
                                )
                            ]
                        )
                    )

                def on_click(e):
                    scr.navigation_apps.users.doing_work.chose_meters.show_meters_data(page, id_task, where="fff")

                return show

            on_click_container = create_on_click(id_task, date)

            task_container = ft.Container(
                content=row,
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
                alignment=ft.alignment.bottom_left,
                on_click=on_click_container
            )

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

        column.controls.append(panel_list)

        page.update()

    column = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

    def on_click_upload(e):
        scr.BD.bd_users.bd_server_user.upload_data_to_server(page)

    update_results()

    def sorting_change(e):
        global sorting
        sorting = e.control.value
        update_results(statuses)

    page.add(
        ft.ResponsiveRow(
            [
                ft.ResponsiveRow(
                    [
                        search_bar,
                        ft.Dropdown(
                            on_change=sorting_change,
                            value=sorting,
                            width=100,
                            label="Сортировка",
                            options=[
                                ft.dropdown.Option("Дата"),
                                ft.dropdown.Option("Адрес"),
                                ft.dropdown.Option("Статус"),
                            ],
                            col=1.6
                        )
                    ], columns=5
                ),
                unloaded_tasks_container,
                pending_tasks_container,
                completed_tasks_container,
                failed_tasks_container
            ],
            columns=4,
            spacing=5,
            alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.Container(
            content=ft.Column([ft.Divider(thickness=4, color=ft.colors.WHITE)]),

        )
    )

    page.add(column)

    page.vertical_alignment = ft.MainAxisAlignment.END
    page.add(
        ft.Row(
            [
                ft.ElevatedButton(text="Отгрузить все данные", on_click=on_click_upload, icon="BACKUP_ROUNDED", ),
            ], alignment=ft.MainAxisAlignment.CENTER
        )
    )
    page.update()
