from flet import *

def build_setting(page: Page):
    # Sidebar
    sidebar = Container(
        width=200,
        bgcolor="#2b3037",
        padding=Padding(10, 50, 10, 10),
        content=Column(
            [
                TextButton("Dashboard", on_click=lambda _: page.go("/Home"), style=ButtonStyle(color="#ffffff")),
                TextButton("Inventory", on_click=lambda _: page.go("/Menu"), style=ButtonStyle(color="#ffffff")),
                TextButton("Billing", on_click=lambda _: page.go("/Billing"), style=ButtonStyle(color="#ffffff")),
                TextButton("Settings", style=ButtonStyle(color="#2abfbf")),
            ],
            alignment=MainAxisAlignment.CENTER,
        ),
    )

    # Header
    header = Text("Settings", size=24, color="#2abfbf", weight=FontWeight.BOLD)

    # Input fields and buttons
    input_fields = Container(
        padding=20,
        width=500,
        height=300,
        bgcolor="#2b3037",
        border_radius=10,
        content=Column(
            [
                TextField(label="New Username", bgcolor="#3b414a", color="#d9d9d9", border_radius=8),
                Row(
                    [
                        TextField(label="Old Password", bgcolor="#3b414a", color="#d9d9d9", border_radius=8, password=True),
                        TextField(label="New Password", bgcolor="#3b414a", color="#d9d9d9", border_radius=8, password=True),
                    ],
                    spacing=10,
                ),
                Row(
                    [
                        ElevatedButton("Update Username", bgcolor="#2abfbf", color="#ffffff", width=150),
                        ElevatedButton("Update Password", bgcolor="#2abfbf", color="#ffffff", width=150),
                    ],
                    alignment=MainAxisAlignment.END,
                ),
            ],
            spacing=15,
        ),
    )

    # Back button
    back_button = ElevatedButton("Back", bgcolor="#2abfbf", color="#ffffff", on_click=lambda _: page.go("/Home"))

    # Page layout
    return Row(
        [
            sidebar,
            VerticalDivider(width=1, color="#2abfbf"),
            Column(
                [
                    header,
                    input_fields,
                    Container(content=back_button, alignment=alignment.center_right, padding=20),
                ],
                spacing=20,
                alignment=MainAxisAlignment.START,
                width=800,
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
