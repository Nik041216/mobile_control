import flet as ft
import asyncio


class LoadingManager:
    overlay: ft.Container = None
    text: ft.Text = None
    page: ft.Page = None

    @classmethod
    def init(cls, page: ft.Page):
        cls.text = ft.Text("Загрузка...", size=20, color=ft.Colors.BLUE)
        cls.overlay = ft.Container(
            content=ft.Column(
                [
                    ft.ProgressRing(color=ft.Colors.BLUE),
                    cls.text,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
            bgcolor=ft.colors.with_opacity(0.5, ft.colors.BLACK),
            visible=False,
            expand=True
        )
        cls.page = page
        if cls.overlay in cls.page.overlay:
            cls.page.overlay.remove(cls.overlay)
        cls.page.overlay.append(cls.overlay)  # Добавляем в конец (поверх всех)
        cls.page.update()

    @classmethod
    async def show(cls, message: str = "Загрузка..."):
        if cls.overlay and cls.text:
            cls.text.value = message
            cls.overlay.visible = True
            cls.page.update()
            await asyncio.sleep(0.1)

    @classmethod
    def show_(cls, message: str = "Загрузка..."):
        if cls.overlay and cls.text:
            cls.text.value = message
            cls.overlay.visible = True
            cls.page.update()

    @classmethod
    async def hide(cls):
        if cls.overlay:
            cls.overlay.visible = False
            cls.page.update()

    @classmethod
    def hide_(cls):
        if cls.overlay:
            cls.overlay.visible = False
            cls.page.update()
