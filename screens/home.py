import flet as ft
from flet import *

class HomeScreen:
    def __init__(self, page: Page):
        self.page = page

    def build(self):
        # Left side menu bar
        menu_bar = Container(
            width=200,
            bgcolor="#383838",
            padding=10,
            content=Column(
                expand=True,
                controls=[
                    Text("Dashboard", color="#00D0FF", size=20, weight="bold"),
                    Container(height=20),
                    Container(
                        width=180,
                        height=50,
                        margin=margin.only(bottom=10),
                        content=ElevatedButton(
                            on_click=lambda _: self.page.go("/Home"),
                            text="Dashboard",
                            bgcolor="#2C2C2C",
                            color="white",
                            expand=True,
                        ),
                    ),
                    Container(
                        width=180,
                        height=50,
                        margin=margin.only(bottom=10),
                        content=ElevatedButton(
                            on_click=lambda _: self.page.go("/Inventory"),
                            text="Inventory",
                            bgcolor="#2C2C2C",
                            color="white",
                            expand=True,
                        ),
                    ),
                    Container(
                        width=180,
                        height=50,
                        margin=margin.only(bottom=10),
                        content=ElevatedButton(
                            on_click=lambda _: self.page.go("/Billing"),
                            text="Billing",
                            bgcolor="#2C2C2C",
                            color="white",
                            expand=True,
                        ),
                    ),
                    Container(
                        width=180,
                        height=50,
                        margin=margin.only(bottom=10),
                        content=ElevatedButton(
                            on_click=lambda _: self.page.go("/Settings"),
                            text="Settings",
                            bgcolor="#2C2C2C",
                            color="white",
                            expand=True,
                        ),
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
                expand=True,
                controls=[
                    Text(value="Welcome Back", color="#00D0FF", size=40),
                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        expand=True,
                        controls=[
                            Container(
                                expand=True,  # Expand box according to available space
                                bgcolor="white",
                                border_radius=10,
                                padding=10,
                                content=Column(
                                    horizontal_alignment=CrossAxisAlignment.CENTER,
                                    alignment=MainAxisAlignment.CENTER,
                                    expand=True,
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
                                expand=True,  # Expand box according to available space
                                bgcolor="white",
                                border_radius=10,
                                padding=10,
                                content=Column(
                                    horizontal_alignment=CrossAxisAlignment.CENTER,
                                    alignment=MainAxisAlignment.CENTER,
                                    expand=True,
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
            expand=True,
            controls=[
                menu_bar,
                content_area,
            ],
        )

        return layout
