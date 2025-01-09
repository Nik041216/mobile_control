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
sorting = "Адрес"


def user_main(page):
    page.window.width = 362.4
    page.window.height = 800
    page.update()
    page.controls.clear()
    screen_width = page.window.width
    screen_height = page.height
    page.vertical_alignment = ft.MainAxisAlignment.START
    global statuses, sorting

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

        scr.BD.bd_users.bd_server_user.select_task_data_for_update_v2(page)
        update_results()
        page.update()

    page.appbar = ft.AppBar(
        title=ft.Text("Задачи"),
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
                elif text == 'не выполнен':
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
        search_value = search_bar.value
        # results = scr.BD.bd_users.local.select_bd.select_tasks_data_new_v2(sorting, search_value, "today")
        results_v2 = scr.BD.bd_users.local.select_bd.select_tasks_data_new_v2(sorting, search_value, "now")
        # if filter_statuses:
        #     filtered_results = [result for result in results if result[10] in filter_statuses]
        # else:
        #     filtered_results = [
        #         result for result in results
        #     ]
        if filter_statuses:
            filtered_results_v2 = [result_v2 for result_v2 in results_v2 if result_v2[12] in filter_statuses]
        else:
            filtered_results_v2 = [
                result_v2 for result_v2 in results_v2
            ]

        column.controls.clear()

        # Словарь для хранения задач по районам
        tasks_by_street = {}
        panel_list = ft.ExpansionPanelList(
            elevation=25,
            expanded_header_padding=3
        )

        for result_v2 in filtered_results_v2:
            id_task, fio, district, hamlet, street, dom, apartment, phone_number, \
                personal_account, date, date_end, remark_task, status, purpose, \
                registered_residing, standarts, area, saldo = result_v2

        # for result in filtered_results:
        #     id_task, person_name, district, street, dom, apartment, phone_number, \
        #         personal_account, date, remark, status, purpose, registered_residing, \
        #         status_address, standarts, area, saldo = result

            # Проверяем, существует ли уже ключ для этого района, если нет - создаем
            if street not in tasks_by_street:
                tasks_by_street[street] = []

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
                ]
            )

            # Используем замыкание для передачи правильного apartment
            def create_on_click(id_task):
                def on_click(e):
                    scr.navigation_apps.users.doing_work.chose_meters.show_meters_data(page, id_task, where="task")

                return on_click

            on_click_container = create_on_click(id_task)

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

            # Добавляем контейнер с задачей в соответствующий район
            tasks_by_street[street].append(task_container)

        # Создаем раскрывающиеся панели для каждого района
        for street, tasks in tasks_by_street.items():
            panel = ft.ExpansionPanel(
                header=ft.Text(f"{street}"),
                content=ft.Column(tasks),  # Добавляем список задач в панель
                expanded=True,
                can_tap_header=True
            )
            panel_list.controls.append(panel)

        column.controls.append(panel_list)

        page.update()

    column = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

    def on_click_upload(e):
        scr.BD.bd_users.bd_server_user.upload_data_to_server_v2(page)

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
