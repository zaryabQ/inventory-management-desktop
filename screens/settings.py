import flet as ft
from flet import *
TEXT_COLOR = colors.BLACK
class SettingsScreen:
    def __init__(self, page: Page):
        self.page = page

    def create_menu_button(self, text: str, route: str) -> TextButton:
        """Helper function to create menu buttons."""
        return TextButton(
            content=Text(text, size=20, weight=FontWeight.BOLD, color=TEXT_COLOR),
            on_click=lambda _: self.page.go(route),
            style=ButtonStyle(
                bgcolor="#2b3037",  # Background color for the button
                shape=RoundedRectangleBorder(radius=8),
                padding=Padding(left=10, right=15, top=10, bottom=10),
            ),
        )

    def build(self):
        # Sidebar
        sidebar = Container(
            width=200,
            bgcolor="#383838",
            padding=10,
            content=Column(
                expand=True,
                controls=[
                    Text("Dashboard", color="#00D0FF", size=20, weight="bold"),
                    Container(height=20),
                    self.create_menu_button("Dashboard", "/Home"),
                    Container(height=10),
                    self.create_menu_button("Inventory", "/Inventory"),
                    Container(height=10),
                    self.create_menu_button("Billing", "/Billing"),
                    Container(height=10),
                    self.create_menu_button("Settings", "/Settings"),
                ],
            ),
        )

        # Header with welcome message
        header = Container(
            padding=0,
            content=Row(
                controls=[
                    Container(
                        content=Text("Welcome Back", size=40, color="#26A69A"),
                        padding=Padding(left=20, right=20, top=0, bottom=0),
                    ),
                ],
                alignment=MainAxisAlignment.CENTER,
                vertical_alignment=CrossAxisAlignment.CENTER,
                expand=True,
            ),
            expand=True,
        )

        # Input fields and buttons
        input_fields = Container(
            padding=Padding(20, 20, 20, 20),
            width=1000,
            height=250,
            bgcolor="#2b3037",
            border_radius=10,
            content=Column(
                controls=[
                    Container(
                        width=300,
                        content=TextField(
                            label="New Username",
                            bgcolor="#FFFFFF",
                            color="#000000",
                            border_radius=8,
                            height=50,
                        ),
                    ),
                    Row(
                        controls=[
                            Container(
                                width=300,
                                content=TextField(
                                    label="Old Password",
                                    bgcolor="#FFFFFF",
                                    color="#000000",
                                    border_radius=8,
                                    password=True,
                                    height=50,
                                ),
                            ),
                            Container(
                                width=300,
                                content=TextField(
                                    label="New Password",
                                    bgcolor="#FFFFFF",
                                    color="#000000",
                                    border_radius=8,
                                    password=True,
                                    height=50,
                                ),
                            ),
                        ],
                        spacing=10,
                        alignment=MainAxisAlignment.START,
                    ),
                ],
                spacing=20,
            ),
        )

        # Update buttons
        update_buttons = Container(
            padding=Padding(0, 0, 0, 40),
            content=Column(
                [
                    ElevatedButton("Update", bgcolor="#2abfbf", color="#ffffff", width=100),
                    ElevatedButton("Update", bgcolor="#2abfbf", color="#ffffff", width=100),
                ],
                spacing=80,
                alignment=MainAxisAlignment.START,
            ),
        )

        # Back button
        back_button = ElevatedButton("Back", bgcolor="#2abfbf", width=100, color="#ffffff", on_click=lambda _: self.page.go("/Dashboard"))

        # Page layout
        layout = Row(
            controls=[
                sidebar,
                VerticalDivider(width=1, color="#2abfbf"),
                Column(
                    controls=[
                        header,
                        Row(
                            controls=[
                                input_fields,
                                update_buttons,
                            ],
                            alignment=MainAxisAlignment.START,
                        ),
                        Row(
                            controls=[
                                Container(
                                    content=back_button,
                                    alignment=alignment.center,
                                    padding=Padding(left=0, right=0, top=0, bottom=20)
                                )
                            ],
                            alignment=MainAxisAlignment.CENTER,
                            expand=True,
                        ),
                    ],
                    spacing=20,
                    alignment=MainAxisAlignment.START,
                    width=800,
                    expand=True,
                ),
            ],
            expand=True,
        )

        return layout


