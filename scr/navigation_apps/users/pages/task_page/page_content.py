import flet as ft
import scr.BD.bd_users.local.select_bd as select_bd
from scr.components.search_field import SearchField
import scr.components.card_for_task as card
import scr.func

statuses = ['не выполнен', 'в исполнении', 'просрочен']
sorting = "Адрес"
column = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)


def get_content(page):
    container = ft.Container(expand=True)
    user_main(page, container)
    return container


def update_results(filter_statuses, page, search_value):

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
        where = "task"
        task_container = card.create_task_container(page, where, result)
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