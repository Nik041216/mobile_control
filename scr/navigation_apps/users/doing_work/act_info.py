import flet as ft
import scr.BD.bd_users.local.select_bd as select
import scr.func
import scr.navigation_apps.users.doing_work.chose_meters as chose
from scr.components.loading import LoadingManager


def viewing_act(page, id_task):
    screen_width = page.window_width
    selected_images = {}
    save_photos = ft.Row(scroll=ft.ScrollMode.AUTO, expand=True, )

    def bottom_sheet_yes(e):
        page.close(bottom_sheet)

    bottom_sheet = ft.BottomSheet(
        content=ft.Container(
            padding=50,
            content=ft.Column(
                tight=True,
                controls=[
                    ft.Text("Прикрепите фотографию/фотографии акта как доказательство его наличия"),
                    ft.Row(
                        [
                            ft.ElevatedButton("Хорошо", on_click=bottom_sheet_yes),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                ],
            ),
        ),
    )

    results = select.select_acts_(id_task)
    reasons = ft.Column
    if results:
        for result in results:
            act_id, task_id, date, reason, made = result
            date = scr.func.reverse_date(date)
            reasons_split = [r.strip() for r in reason.split(',') if r.strip()]
            reasons = ft.Column(
                [
                    ft.Row([
                        ft.Text(f"{idx}.", weight=ft.FontWeight.BOLD, width=30, size=17),
                        ft.Column([
                            ft.Text(item, size=17)
                        ], spacing=0,
                            expand=True)
                    ], spacing=2)
                    for idx, item in enumerate(reasons_split, 1)
                ], spacing=4
            )

    title = ft.Text("Сформированный акт по заданию")
    act_data = ft.Container(
        content=ft.Stack(  # <-- Stack, чтобы наложить прогрузку поверх
            controls=[
                ft.Column(
                    [
                        ft.Text(f"Номер задания: {task_id}", size=17),
                        ft.Text(f"Дата формирования: {date}", size=17),
                        ft.Text("Причины формировния", size=17),
                        reasons,
                        save_photos,
                        ft.ElevatedButton("Добавить фотографию",),
                    ],
                    scroll=ft.ScrollMode.AUTO,
                ),
                LoadingManager.overlay  # <-- теперь он внутри AlertDialog
            ]
        ),
        width=screen_width * 0.95
    )

    def yes_click(e):
        if not selected_images:
            page.open(bottom_sheet)

    def _close(e):
        page.close(act_)
        chose.get_content(page, task_id)

    act_ = ft.AlertDialog(
        modal=True,
        content=act_data,
        title=title,
        actions=[
            ft.Row(
                [
                    ft.ElevatedButton("Подтвердить акт", on_click=yes_click, bgcolor=ft.colors.BLUE_200),
                    ft.ElevatedButton("Назад", on_click=_close, bgcolor=ft.colors.RED_200)
                ], alignment=ft.MainAxisAlignment.CENTER
            )
        ],
        inset_padding=screen_width * 0.05
    )

    page.open(act_)
    page.update()

