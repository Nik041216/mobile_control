import flet as ft


class SearchField:
    search_history_list = []

    def __init__(self, on_change, on_submit):
        self.on_change = on_change
        self.on_submit = on_submit

    def create_search_field(self):
        def handle_tap(e):
            self.search_bar.open_view()

        def handle_change(e):
            if self.search_bar.value != '':
                self.search_bar.close_view(e.control.value)
            self.on_change(e.control.value)

        def handle_submit(e):
            query = e.control.value.strip()
            if query and query not in self.search_history_list:
                if len(self.search_history_list) >= 10:
                    del self.search_history_list[9]
                self.search_history_list.insert(0, query)
                self.update_search_history()
            self.on_submit(query)
            self.search_bar.close_view(query)

        def close_anchor(e):
            self.search_bar.value = e.control.data
            self.on_submit(e.control.data)
            self.search_bar.close_view()

        def create_search_list():
            return [
                ft.ListTile(
                    title=ft.Text(query),
                    on_click=close_anchor,
                    data=query
                )
                for query in self.search_history_list
            ]

        self.search_bar = ft.SearchBar(
            view_elevation=4,
            divider_color=ft.colors.AMBER,
            bar_hint_text="Поиск задания...",
            view_hint_text="Последние результаты...",
            on_change=handle_change,
            on_submit=handle_submit,
            on_tap=handle_tap,
            value="",
            controls=create_search_list(),
            col=3.4,
        )

        return self.search_bar

    def update_search_history(self):
        self.search_bar.controls = [
            ft.ListTile(
                title=ft.Text(query),
                on_click=lambda e, q=query: self.close_anchor(e, q),
                data=query
            )
            for query in self.search_history_list
        ]
