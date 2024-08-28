import flet as ft
from flet import *

TEXT_COLOR = colors.BLACK

class SettingsScreen:
    def __init__(self, page: Page):
        self.page = page

    def create_menu_button(self, text, route):
        """Helper function to create menu buttons."""
        return Container(
            width=180,
            height=50,
            margin=margin.only(bottom=10),
            content=ElevatedButton(
                text=text,
                on_click=lambda _: self.page.go(route),
                bgcolor="#2C2C2C",
                color="white",
                expand=True,
            ),
        )
    def build(self):
        # Sidebar
        sidebar = Container(
            width=250,
            bgcolor="#383838",
            padding=10,
            content=Column(
                expand=True,
                controls=[
                    Text("Setting", color="#00D0FF", size=20, weight="bold"),
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
        header = Row(
                controls=[
                    Container(
                        content=Text("Welcome Back", size=40, color="#26A69A"),
                        padding=Padding(left=20, right=20, top=0, bottom=0),
                    ),
                ],
                alignment=MainAxisAlignment.CENTER,
                vertical_alignment=CrossAxisAlignment.CENTER,
                
                expand=True,
            )

        # Input fields and buttons
        input_fields = Container(
            padding=Padding(20, 20, 20, 20),
            width=1000,
            height=250,
            bgcolor="#383838",  # Keeping the input fields container's background color different
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
                        alignment=alignment.center
                    ),
                    # Adding some vertical space before password fields
                    Container(height=20),  # Adjust the height to move the fields down
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
                                alignment=alignment.center
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
                                alignment=alignment.center
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
                    ElevatedButton("Update", bgcolor="#2abfbf", color="#000000", width=100),
                    ElevatedButton("Update", bgcolor="#2abfbf", color="#000000", width=100),
                ],
                spacing=80,
                alignment=MainAxisAlignment.START,
            ),
        )

        # Back button
        back_button = ElevatedButton("Logout", bgcolor="#2abfbf", width=100, color="#000000", on_click=lambda _: self.page.go("/"))

        # Page layout
        layout = Container(
            bgcolor="#2b3037",  # Background color for the right side container
            expand=True,
            content=Row(
                controls=[
                    sidebar,
             
                    Column(
                        controls=[
                            header,
                            Row(
                                controls=[
                                    input_fields,
                                    update_buttons,
                                ],
                                alignment=MainAxisAlignment.CENTER,
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
                        alignment=MainAxisAlignment.CENTER,
                        expand=True,
                    ),
                ],
                expand=True,
            )
        )
 
        return layout
