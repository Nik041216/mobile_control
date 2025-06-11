import datetime
import flet as ft
import scr.BD.bd_users.local.select_bd as select_bd
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


def reschedule_to_another_date(e, id_task, date, date_end, page):
    screen_width = page.window_width

    def date_change_picker(e):
        new_ = str(date_picker.value.date())
        new_date.value = scr.func.reverse_date(new_)
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

    def on_click(e):
        current_date = datetime.datetime.now().strftime("%d-%m-%Y")
        if date_picker.value and date_picker.value.date() <= datetime.datetime.strptime(current_date,
                                                                                        "%d-%m-%Y").date():
            new_date.error_text = "Задание не может быть перенесено\n на сегодня"
        elif date_picker.value.date() > datetime.datetime.strptime(date_end, "%d-%m-%Y").date():
            new_date.error_text = "Обговорите такой перенос с мастером"
        else:
            new_date_ = date_picker.value.date()
            new_date.value = date_picker.value.date()
            new_date.value = scr.func.reverse_date(new_date.value)
            scr.BD.bd_users.local.update_bd.update_date(id_task, new_date_)
            content.get_content(page)
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
                                      bgcolor=ft.colors.BLUE_300, color=ft.Colors.BLACK87,
                                      width=page.window_width * 0.30),
                    ft.ElevatedButton("Назад",
                                      on_click=close,
                                      bgcolor=ft.colors.BLUE_300, color=ft.Colors.BLACK87,
                                      width=page.window_width * 0.30)
                ], alignment=ft.MainAxisAlignment.CENTER
            )
        ],
        inset_padding=screen_width * 0.05
    )

    page.open(change_date)
    page.update()