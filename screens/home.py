from flet import *

class Home:
    def __init__(self, page: Page):
        self.page = page
        self.page.title = "Dashboard"
        self.page.bgcolor = "#2C2C2C"

    def build(self):
        # Left side menu bar
        menu_bar = Container(
            width=200,
            bgcolor="#383838",
            padding=10,
            content=Column(
                controls=[
                    Text("Dashboard", color="#00D0FF", size=20, weight="bold"),
                    Container(height=20),
                    ElevatedButton(
                        on_click=lambda _: self.page.go("/Dashboard"),
                        text="Dashboard",
                        bgcolor="#2C2C2C",
                        color="white",
                        width=180,
                        height=50,
                    ),
                    ElevatedButton(
                        on_click=lambda _: self.page.go("/Inventory"),
                        text="Inventory",
                        bgcolor="#2C2C2C",
                        color="white",
                        width=180,
                        height=50,
                    ),
                    ElevatedButton(
                        on_click=lambda _: self.page.go("/Billing"),
                        text="Billing",
                        bgcolor="#2C2C2C",
                        color="white",
                        width=180,
                        height=50,
                    ),
                    ElevatedButton(
                        on_click=lambda _: self.page.go("/Settings"),
                        text="Settings",
                        bgcolor="#2C2C2C",
                        color="white",
                        width=180,
                        height=50,
                    ),
                ],
            ),
        )

        # Right side content
        content_area = Container(
            expand=True,
            bgcolor="#2C2C2C",
            padding=25,
            content=Column(
                horizontal_alignment=CrossAxisAlignment.CENTER,
                alignment=MainAxisAlignment.CENTER,
                controls=[
                    Text(value="Welcome Back", color="#00D0FF", size=40),
                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            Container(
                                width=200,
                                height=150,
                                bgcolor="white",
                                border_radius=10,
                                content=Column(
                                    horizontal_alignment=CrossAxisAlignment.CENTER,
                                    alignment=MainAxisAlignment.CENTER,
                                    controls=[
                                        Text("Overview", size=18, weight="bold"),
                                        Text("Total Sales", size=16),
                                        Text("92", size=16),
                                        Text("Profit", size=16),
                                        Text("92", size=16),
                                        Text("Total Cost", size=16),
                                        Text("92", size=16),
                                    ],
                                ),
                            ),
                            Container(
                                width=200,
                                height=150,
                                bgcolor="white",
                                border_radius=10,
                                content=Column(
                                    horizontal_alignment=CrossAxisAlignment.CENTER,
                                    alignment=MainAxisAlignment.CENTER,
                                    controls=[
                                        Text("Inventory", size=18, weight="bold"),
                                        Text("Total Items", size=16),
                                        Text("92", size=16),
                                        Text("Low Stock", size=16),
                                        Text("92", size=16),
                                        Text("To be Received", size=16),
                                        Text("92", size=16),
                                    ],
                                ),
                            ),
                        ],
                    ),
                ],
            ),
        )

        # Main layout combining menu bar and content area
        layout = Row(
            controls=[
                menu_bar,
                content_area,
            ],
        )

        return layout

def main(page: Page):
    page.window.width = 800
    page.window.height = 500
    page.window.resizable = False

    home = Home(page)
    page.add(home.build())

app(target=main)
