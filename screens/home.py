from flet import *
from assets.styles import BG, FW

class Home(UserControl):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page

    def build(self):
        self.container = Container(
            Column(
                alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    Container(
                        content=Text(value="Welcome To Icecream Alley", color="#FCC8D1", size=50),
                    ),
                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        vertical_alignment=CrossAxisAlignment.CENTER,
                        expand=1,
                        controls=[
                            ElevatedButton(
                                on_click=lambda _: self.page.go("/Menu"),
                                text="Menu",
                                bgcolor="#FAB3A9",
                                color="red",
                                width=200,
                                height=100,
                            ),
                            ElevatedButton(
                                on_click=lambda _: self.page.go("/Billing"),
                                text="Billing",
                                bgcolor="#FAB3A9",
                                color="red",
                                width=200,
                                height=100,
                            ),
                            ElevatedButton(
                                on_click=lambda _: self.page.go("/Setting"),
                                text="Settings",
                                bgcolor="#FAB3A9",
                                color="red",
                                width=200,
                                height=100,
                            ),
                        ],
                    ),
                ],
            ),
            height=600,
            width=700,
            padding=25,
            border_radius=50,
        )
        return self.container
