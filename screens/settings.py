import flet as ft
from flet import *
import sqlite3

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

    def update_username(self, new_username, old_password):
        # Connect to the SQLite database
        conn = sqlite3.connect('db/sql.db')
        cursor = conn.cursor()

        # Check if the old password is correct
        cursor.execute("SELECT * FROM Users WHERE password = ?", (old_password,))
        user = cursor.fetchone()

        if user:
            # Update the username
            cursor.execute("UPDATE Users SET username = ? WHERE id = ?", 
                           (new_username, user[0]))
            conn.commit()
            self.page.snack_bar = SnackBar(Text("Username updated successfully!"), open=True)
        else:
            self.page.snack_bar = SnackBar(Text("Incorrect old password!"), open=True)

        conn.close()

    def update_password(self, old_password, new_password):
        # Connect to the SQLite database
        conn = sqlite3.connect('db/sql.db')
        cursor = conn.cursor()

        # Check if the old password is correct
        cursor.execute("SELECT * FROM Users WHERE password = ?", (old_password,))
        user = cursor.fetchone()

        if user:
            # Update the password
            cursor.execute("UPDATE Users SET password = ? WHERE id = ?", 
                           (new_password, user[0]))
            conn.commit()
            self.page.snack_bar = SnackBar(Text("Password updated successfully!"), open=True)
        else:
            self.page.snack_bar = SnackBar(Text("Incorrect old password!"), open=True)

        conn.close()

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

        # Input fields
        new_username_field = TextField(
            label="New Username",
            bgcolor="#FFFFFF",
            color="#000000",
            border_radius=8,
            height=50,
        )

        old_password_field = TextField(
            label="Old Password",
            bgcolor="#FFFFFF",
            color="#000000",
            border_radius=8,
            password=True,
            height=50,
        )

        new_password_field = TextField(
            label="New Password",
            bgcolor="#FFFFFF",
            color="#000000",
            border_radius=8,
            password=True,
            height=50,
        )

        input_fields = Container(
            padding=Padding(20, 20, 20, 20),
            width=1000,
            height=250,
            bgcolor="#383838",
            border_radius=10,
            content=Column(
                controls=[
                    Container(
                        width=300,
                        content=new_username_field,
                        alignment=alignment.center
                    ),
                    Container(height=20),
                    Row(
                        controls=[
                            Container(
                                width=300,
                                content=old_password_field,
                                alignment=alignment.center
                            ),
                            Container(
                                width=300,
                                content=new_password_field,
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
        update_username_button = ElevatedButton(
            "Update Username",
            bgcolor="#2abfbf",
            color="#000000",
            width=200,
            on_click=lambda _: self.update_username(
                new_username_field.value,
                old_password_field.value
            )
        )

        update_password_button = ElevatedButton(
            "Update Password",
            bgcolor="#2abfbf",
            color="#000000",
            width=200,
            on_click=lambda _: self.update_password(
                old_password_field.value,
                new_password_field.value
            )
        )

        # Back button
        back_button = ElevatedButton("Logout", bgcolor="#2abfbf", width=100, color="#000000", on_click=lambda _: self.page.go("/"))

        # Page layout
        layout = Container(
            bgcolor="#2b3037",
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
                                    Column(
                                    controls=[
                                        update_username_button,
                                        Container(height=20),
                                        Container(
                                            content=update_password_button,
                                            padding=Padding(left=0, right=0, top=0, bottom=45) 
                                        ),
                                    ],
                                    alignment=MainAxisAlignment.CENTER,
                                    spacing=35,
                                ),
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