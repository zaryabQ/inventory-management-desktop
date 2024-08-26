from flet import *

LABEL_COLOR = colors.WHITE
TEXT_COLOR = colors.WHITE

def create_menu_button(text: str, route: str) -> TextButton:
    return TextButton(
        content=Text(text, size=20, weight=FontWeight.BOLD, color=TEXT_COLOR),
        on_click=lambda _: Page.go(route),
        style=ButtonStyle(
            bgcolor="#2b3037",  # Background color for the button
            shape=RoundedRectangleBorder(radius=8),
            padding=Padding(left=10, right=15, top=10, bottom=10),
        ),
    )

def build_setting(page: Page):
    sidebar = Container(
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
                        on_click=lambda _: page.go("/Dashboard"),
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
                        on_click=lambda _: page.go("/Inventory"),
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
                        on_click=lambda _: page.go("/Billing"),
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
                        on_click=lambda _: page.go("/Settings"),
                        text="Settings",
                        bgcolor="#2C2C2C",
                        color="white",
                        expand=True,
                    ),
                ),
            ],
        ),
    )

    # Header with welcome message
    header = Container(
        padding=0,  # Padding around the entire container set to 0
        content=Row(
            controls=[
                Container(
                    content=Text("Welcome Back", size=40, color="#26A69A"),
                    padding=Padding(left=20, right=20, top=0, bottom=0),  # Padding to adjust text position
                ),
            ],
            alignment=MainAxisAlignment.CENTER,  # Center the Row's content horizontally
            vertical_alignment=CrossAxisAlignment.CENTER,  # Center the Row's content vertically
            expand=True,  # Ensure the Row expands to fill available space
        ),
        expand=True,  # Ensure the Container expands to fill available space
    )

    # Input fields and buttons
    input_fields = Container(
        padding=Padding(20, 20, 20, 20),  # left, right, top, bottom
        width=1000,
        height=250,
        bgcolor="#2b3037",
        border_radius=10,
        content=Column(
            controls=[
                Container(
                    width=300,  # Adjust width to make the username field smaller
                    content=TextField(
                        label="New Username",
                        bgcolor="#FFFFFF",
                        color="#000000",
                        border_radius=8,
                        height=100,
                    ),
                ),
                Row(
                    controls=[
                        Container(
                            width=300,  # Adjust width to match the size of the other fields
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
                            width=300,  # Adjust width to match the size of the other fields
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

    # Update buttons for each field
    update_buttons = Container(
        padding=Padding(0, 0, 0, 40),  # left, right, top, bottom
        content=Column(
            [
                ElevatedButton("Update", bgcolor="#2abfbf", color="#ffffff", width=100),
                ElevatedButton("Update", bgcolor="#2abfbf", color="#ffffff", width=100),
            ],
            spacing=80,
            alignment=MainAxisAlignment.START,
        ),
    )

    back_button = ElevatedButton("Back", bgcolor="#2abfbf", width=100, color="#ffffff", on_click=lambda _: page.go("/dashboard"))

    # Page layout
    return Row(
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
                                alignment=alignment.center,  # Center align button within Container
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
                expand=True,  # Ensure Column expands to fill available space
            ),
        ],
        expand=True,
    )

def main(page: Page):
    page.title = "Settings"
    page.bgcolor = "#121a26"  # Background color

    # Add the Setting screen to the page
    page.add(build_setting(page))

app(target=main)