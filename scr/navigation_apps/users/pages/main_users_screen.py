import flet as ft
import scr.BD.bd_users.local.select_bd as select_bd
import scr.BD.bd_users.bd_server_user as bd_server_user
import scr.constants as const
import scr.navigation_apps.users.doing_work.chose_meters as chose_meters
import scr.navigation_apps.users.doing_work.alert_check_data as check_alert
import scr.BD.bd_users.bd_server_user
from scr.components.search_field import SearchField
from scr.func import create_filter_button

statuses = []
sorting = "Адрес"
menu_visible = False


def user_main(page: ft.Page):
    page.window.width = 362.4
    page.window.height = 800
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.controls.clear()
    page.floating_action_button = None

    completed_icon = ft.Icon(ft.icons.CHECK_CIRCLE_OUTLINE)
    failed_icon = ft.Icon(ft.icons.ERROR_OUTLINE)
    pending_icon = ft.Icon(ft.icons.HOURGLASS_EMPTY)
    unloaded_icon = ft.Icon(ft.icons.BUILD)
    checkboxes = []

    # Создание чекбоксов и добавление их в список
    def create_checkbox_with_icon(label, icon, status_text):
        checkbox = ft.Checkbox(label=label, on_change=lambda e: filtration_check(e, status_text))
        row = ft.Row([ft.Icon(icon, size=20), checkbox], alignment=ft.MainAxisAlignment.START)
        checkboxes.append(checkbox)  # Добавляем в список для сброса
        return row

    def reset_filters(e):
        global statuses
        statuses.clear()
        for checkbox in checkboxes:
            checkbox.value = False
        update_results(filter_statuses=statuses)
        page.update()

    search_field = SearchField(on_change=lambda _: update_results(), on_submit=lambda _: update_results())
    search_bar = search_field.create_search_field()

    column = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

    def update_results(filter_statuses=None):
        results = select_bd.select_tasks_data_new(sorting, search_bar.value, "now")
        filtered_results = [result for result in results if not filter_statuses or result[12] in filter_statuses]

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

        column.controls = [panel_list]
        page.update()

    def click_conteiner(e, id_task):
        check_alert.func_check_address_data(page, id_task, where="task")
        chose_meters.show_meters_data(page, id_task, where="task")

    def create_task_container(result):
        id_task, _, _, _, street, dom, apartment, phone, _, _, _, _, status, purpose, *_ = result
        stat = ft.Row([
                ft.Text(f"Статус: {status}"),
            ])
        if status == 'выполнен':
            stat.controls.append(completed_icon)
            color = const.tasks_completed_color
        if status == 'в_исполнении':
            stat.controls.append(unloaded_icon)
            color = const.tasks_unloaded_color
        if status == 'не выполнен':
            stat.controls.append(pending_icon)
            color = ft.colors.BLUE
        if status == 'просрочен':
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

    def filtration_check(e, text):
        global statuses
        if text not in statuses:
            statuses.append(text)
            update_results(filter_statuses=statuses)
        else:
            statuses.remove(text)
            update_results(filter_statuses=statuses)

    def toggle_drawer(e=None):
        global menu_visible
        menu_visible = not menu_visible
        menu_container.visible = menu_visible
        overlay_container.visible = menu_visible
        page.update()

    # Полупрозрачный фон для затемнения экрана при открытом меню
    overlay_container = ft.Container(
        visible=False,
        bgcolor=ft.colors.BLACK54,
        expand=True,
        alignment=ft.alignment.center,
        on_click=toggle_drawer  # Закрывает меню при клике
    )

    # Боковое меню
    menu_container = ft.Container(
        visible=False,
        width=250,
        height=page.window.height,
        bgcolor=ft.colors.WHITE,
        padding=20,
        animate=ft.animation.Animation(400, ft.AnimationCurve.DECELERATE),  # Исправлена ошибка
        content=ft.Column([
            ft.Text("Фильтры", size=20, weight=ft.FontWeight.BOLD),
            create_checkbox_with_icon("Не выполненные", ft.icons.HOURGLASS_EMPTY, 'не выполнен'),
            create_checkbox_with_icon("В работе", ft.icons.BUILD, 'в_исполнении'),
            create_checkbox_with_icon("Выполненные", ft.icons.CHECK_CIRCLE_OUTLINE, 'выполнен'),
            create_checkbox_with_icon("Просроченные", ft.icons.ERROR_OUTLINE, 'просрочен'),
            ft.Container(expand=True),  # Заполняет пространство

            ft.Row(
                [ft.ElevatedButton("Сбросить фильтры", on_click=reset_filters), ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.Row(
                [ft.ElevatedButton(
                    text="Отгрузить все данные",
                    on_click=lambda _: bd_server_user.upload_data_to_server(page),
                    icon="BACKUP_ROUNDED"
                )],
                alignment=ft.MainAxisAlignment.CENTER
            )
        ], expand=True),
    )

    page.appbar = ft.AppBar(
        title=ft.Text("Задачи"),
        center_title=True,
        toolbar_height=50,
        leading=ft.IconButton(icon=ft.icons.MENU, on_click=lambda _: toggle_drawer(_)),
        bgcolor=ft.colors.BLUE_GREY_50,
        actions=[ft.IconButton(icon=ft.icons.AUTORENEW, on_click=lambda _: on_click_update(_))]
    )

    def on_click_update(e):
        if scr.func.check_internet():
            statuses.clear()
            scr.BD.bd_users.bd_server_user.select_task_data_for_update(page)
            update_results()
        else:
            scr.func.show_alert_yn(page, "Нет доступа к сети, проверте интернет соеденение")
        page.update()

    page.add(
        ft.Stack([
            ft.Column([
                ft.ResponsiveRow(
                    [
                        ft.ResponsiveRow(
                            [
                                search_bar,
                                ft.Dropdown(
                                    on_change=lambda e: globals().update(sorting=e.control.value) or update_results(),
                                    value=sorting,
                                    width=100,
                                    label="Сортировка",
                                    options=[ft.dropdown.Option("Адрес"), ft.dropdown.Option("Статус")],
                                    col=1.6
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
    )
    page.overlay.append(overlay_container)
    page.overlay.append(menu_container)
    update_results()
    page.update()
