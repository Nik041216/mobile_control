import flet as ft
import scr.BD.bd_users.local.select_bd as select_bd
import scr.BD.bd_users.bd_server_user as bd_server_user
import scr.func
import scr.BD.bd_users.bd_server_user
import scr.navigation_apps.users.pages.future_task_page.page_content as content

statuses = ['не выполнен', 'в исполнении', 'просрочен']
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
    total_future_task = 0
    total_task = select_bd.select_count_all_task()

    def reset_filters(e):
        global statuses
        statuses = ['не выполнен', 'в исполнении', 'просрочен']
        update_checkboxes()
        content.get_content(page)
        page.update()

    def filtration_check(e, text):
        global statuses
        if e.control.value:
            if text not in statuses:
                statuses.append(text)
        else:
            if text in statuses:
                statuses.remove(text)
        content.update_results(statuses, page, search_value="")
        page.update()

    def update_checkboxes():
        """Обновляет состояние чекбоксов в зависимости от массива `statuses`."""
        for text, checkbox in checkboxes.items():
            checkbox.value = text in statuses  # Устанавливаем значение из массива статусов
        page.update()

    def create_checkboxes():
        """Создаёт чекбоксы, привязывая их к массиву `statuses`."""
        rows = []
        count = select_bd.select_count_task("future")
        nonlocal total_future_task
        total_future_task = sum(count.values())
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
            ft.Divider(color=ft.Colors.BLACK),
            ft.Text(
                spans=[
                    ft.TextSpan("Общее количество будующих заданий: ", ),
                    ft.TextSpan(str(total_future_task), ft.TextStyle(weight=ft.FontWeight.BOLD)),
                ], size=17
            ),
            ft.Divider(color=ft.Colors.BLACK),
            ft.Text(
                spans=[
                    ft.TextSpan("Общее количество заданий: ", ),
                    ft.TextSpan(str(total_task), ft.TextStyle(weight=ft.FontWeight.BOLD)),
                ], size=17
            ),
            ft.Divider(color=ft.Colors.BLACK),
            ft.Container(expand=True),
            ft.Row([ft.ElevatedButton("Сбросить фильтры",
                                      on_click=reset_filters,
                                      bgcolor=ft.colors.RED_400,
                                      icon=ft.icons.FILTER_ALT_OFF,
                                      icon_color=ft.Colors.BLUE_50,
                                      color=ft.colors.WHITE)], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([ft.ElevatedButton("Отгрузить все данные",
                                      on_click=on_click_upload,
                                      icon="BACKUP_ROUNDED",
                                      icon_color=ft.Colors.BLUE_50,
                                      bgcolor=ft.colors.BLUE_400,
                                      color=ft.colors.WHITE)], alignment=ft.MainAxisAlignment.CENTER),
        ], expand=True),
    )

    def on_click_update(page):
        global statuses
        statuses = ['не выполнен', 'в исполнении', 'просрочен']

        # Обновляем данные задач
        content.get_content(page)

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
                                      icon_color=ft.Colors.BLUE_50,
                                      color=ft.colors.WHITE)], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([ft.ElevatedButton("Отгрузить все данные",
                                      on_click=on_click_upload,
                                      icon="BACKUP_ROUNDED",
                                      icon_color=ft.Colors.BLUE_50,
                                      bgcolor=ft.colors.BLUE_400,
                                      color=ft.colors.WHITE)], alignment=ft.MainAxisAlignment.CENTER),
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
