import flet as ft
import scr.BD.bd_users.local.select_bd as select_bd
import scr.BD.bd_users.bd_server_user as bd_server_user
import scr.constants as const
import scr.BD.bd_users.bd_server_user
from scr.components.search_field import SearchField
from scr.func import create_filter_button
import scr.navigation_apps.users.doing_work.alert_check_data as check_alert

statuses = ['не выполнен', 'выполнен', 'в исполнении', 'просрочен']
sorting = "Адрес"
menu_visible = False
column = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)


def get_appbar(page):
    checkboxes = []
    global column

    def reset_filters(e):
        global statuses
        statuses = ['не выполнен', 'выполнен', 'в исполнении', 'просрочен']
        for checkbox in checkboxes:
            checkbox.value = True
        get_content(page)
        page.update()

    def create_checkbox_with_icon(label, icon, status_text, color):
        checkbox = ft.Checkbox(label=label,
                               on_change=lambda e: filtration_check(e, status_text), value=True)
        row = ft.Row([ft.Icon(icon, size=25, color=color), checkbox], alignment=ft.MainAxisAlignment.START)
        checkboxes.append(checkbox)
        return row

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

    menu_container = ft.Container(
        visible=False,
        width=250,
        height=page.window_height,
        bgcolor=ft.colors.BLUE_50,
        padding=20,
        animate=ft.animation.Animation(400, ft.AnimationCurve.DECELERATE),
        content=ft.Column([
            ft.Text("Фильтры", size=20, weight=ft.FontWeight.BOLD),
            create_checkbox_with_icon("Не выполненные", ft.icons.HOURGLASS_EMPTY, 'не выполнен',
                                      color=ft.colors.BLUE),
            create_checkbox_with_icon("В работе", ft.icons.BUILD_OUTLINED, 'в исполнении',
                                      color='#ffc107'),
            create_checkbox_with_icon("Выполненные", ft.icons.CHECK_CIRCLE_OUTLINE, 'выполнен',
                                      color=ft.colors.GREEN),
            create_checkbox_with_icon("Просроченные", ft.icons.ERROR_OUTLINE, 'просрочен',
                                      color=ft.colors.RED),
            ft.Container(expand=True),

            ft.Row([ft.ElevatedButton("Сбросить фильтры",
                                      on_click=reset_filters,
                                      bgcolor=ft.colors.RED_400,
                                      icon=ft.icons.FILTER_ALT_OFF,
                                      color=ft.colors.WHITE),
                    ],
                   alignment=ft.MainAxisAlignment.CENTER
                   ),
            ft.Row(
                [ft.ElevatedButton(
                    text="Отгрузить все данные",
                    on_click=lambda _: bd_server_user.upload_data_to_server(page),
                    icon="BACKUP_ROUNDED",
                    bgcolor=ft.colors.BLUE_400,
                    color=ft.colors.WHITE
                )],
                alignment=ft.MainAxisAlignment.CENTER
            )
        ], expand=True),
    )

    def on_click_update(page):
        global statuses
        if scr.func.check_internet():
            statuses.clear()
            statuses = ['не выполнен', 'выполнен', 'в исполнении', 'просрочен']
            scr.BD.bd_users.bd_server_user.select_task_data_for_update(page)
            get_content(page)
        else:
            scr.func.show_alert_yn(page, "Нет доступа к сети, проверьте интернет соединение")
        page.update()

    page.overlay.append(overlay_container)
    page.overlay.append(menu_container)

    return ft.AppBar(
        title=ft.Text("Задачи"),
        center_title=True,
        toolbar_height=50,
        leading=ft.IconButton(icon=ft.icons.MENU, on_click=lambda _: toggle_drawer(page)),
        bgcolor=ft.colors.BLUE_100,
        actions=[ft.IconButton(icon=ft.icons.AUTORENEW, on_click=lambda _: on_click_update(page))]
    )


def get_content(page):
    container = ft.Container(expand=True)
    user_main(page, container)
    return container


def update_results(filter_statuses, page, search_value):
    completed_icon = ft.Icon(ft.icons.CHECK_CIRCLE_OUTLINE)
    failed_icon = ft.Icon(ft.icons.ERROR_OUTLINE)
    pending_icon = ft.Icon(ft.icons.HOURGLASS_EMPTY)
    unloaded_icon = ft.Icon(ft.icons.BUILD)

    def click_conteiner(e, id_task):
        where = "task"
        check_alert.func_check_address_data(page, id_task, where)

    def create_task_container(result):
        id_task, _, _, _, street, dom, apartment, phone, _, _, _, _, status, purpose, *_ = result
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
            color = const.tasks_failed_color

        result_info = ft.Column([
            ft.Text(f"ул.{street} д.{dom} кв.{apartment}", weight=ft.FontWeight.BOLD),
            stat,
            ft.Text(f"Номер: {phone}"),
            ft.Text(f"Цель: {purpose}")
        ])

        return ft.Card(
            content=ft.Container(
                content=ft.Row([
                    ft.Container(width=10, height=105, bgcolor=color),
                    result_info
                ]),
                padding=10,
                margin=5,
                border_radius=15,
                alignment=ft.alignment.bottom_left,
                on_click=lambda e: click_conteiner(e, id_task)
            ),
            elevation=2
        )

    results = select_bd.select_tasks_data_new(sorting, search_value, "now")
    filtered_results = [result for result in results if result[12] in filter_statuses]

    tasks_by_street = {}
    for result in filtered_results:
        street = result[4]
        if street not in tasks_by_street:
            tasks_by_street[street] = {"tasks": [], "total": 0, "completed": 0}

        tasks_by_street[street]["total"] += 1
        if result[12] == 'выполнен':
            tasks_by_street[street]["completed"] += 1

        task_container = create_task_container(result)
        tasks_by_street[street]["tasks"].append(task_container)

    panel_list = ft.ExpansionPanelList(elevation=25, expanded_header_padding=3, divider_color=ft.colors.BLACK)
    for street, data in tasks_by_street.items():
        panel = ft.ExpansionPanel(
            header=ft.ListTile(title=ft.Text(f"{street} ({data['completed']}/{data['total']})")),
            content=ft.Column(data["tasks"]),
            expanded=True,
            can_tap_header=True
        )
        panel_list.controls.append(panel)

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
                                expand=True,
                                label="Сортировка",
                                options=[ft.dropdown.Option("Адрес"), ft.dropdown.Option("Статус")],
                                col=1.8,
                                bgcolor=ft.colors.WHITE,
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
