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


def user_main(page: ft.Page):
    page.window.width = 362.4
    page.window.height = 800
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.controls.clear()
    page.floating_action_button = None

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

    completed_tasks_container = create_filter_button(
        completed_icon,
        const.tasks_completed_text_color,
        'выполнен',
        filtration
    )
    failed_tasks_container = create_filter_button(
        failed_icon,
        const.tasks_failed_text_color,
        'просрочен',
        filtration
    )
    pending_tasks_container = create_filter_button(
        pending_icon,
        const.tasks_pending_text_color,
        'не выполнен',
        filtration
    )
    unloaded_tasks_container = create_filter_button(
        unloaded_icon,
        const.tasks_unloaded_text_color,
        'в_исполнении',
        filtration
    )

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
        result_info = ft.Column([
            ft.Text(f"ул.{street} д.{dom} кв.{apartment}", weight=ft.FontWeight.BOLD),
            ft.Row([
                ft.Text(f"Статус: {status}"),
            ]),
            ft.Text(f"Номер: {phone}"),
            ft.Text(f"Цель: {purpose}")
        ])
        color = const.tasks_completed_color if status == 'выполнен' else (
            const.tasks_unloaded_color if status == 'в_исполнении' else
            (ft.colors.BLUE if status == 'не выполнен' else const.tasks_failed_color)
        )
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

    drawer = ft.NavigationDrawer(
        controls=[
            ft.Container(
                content=ft.Text("Фильтры", size=20, weight=ft.FontWeight.BOLD),
                padding=20,
            ),
            ft.Checkbox(label="Новые", ),
            ft.Checkbox(label="В работе"),
            ft.Checkbox(label="Выполненные"),
            ft.Checkbox(label="Просроченные"),
            ft.ElevatedButton("Сбросить фильтры", on_click=lambda _: print("Сброс фильтров"))
        ],
        bgcolor=ft.colors.WHITE,
    )

    # Боковое меню
    def toggle_drawer(e):
        page.open(drawer)
        drawer.update()

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
        else:
            scr.func.show_alert_yn(page, "Нет доступа к сети, проверте интернет соеденение")
        page.update()

    page.add(
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
                unloaded_tasks_container,
                pending_tasks_container,
                completed_tasks_container,
                failed_tasks_container
            ],
            columns=4,
            spacing=5,
            alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.Container(content=ft.Column([ft.Divider(thickness=4, color=ft.colors.WHITE)])),
        column,
        ft.Row(
            [ft.ElevatedButton(text="Отгрузить все данные",
                               on_click=lambda _: bd_server_user.upload_data_to_server(page), icon="BACKUP_ROUNDED")],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )

    update_results()
    page.update()
