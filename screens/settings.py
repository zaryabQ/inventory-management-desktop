import flet as ft
from flet import *
from screens.user import User
from db.db_handler import update_user_username, update_user_password

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

    def update_username(self, new_username):
        current_user = User.get_current_user()
        if current_user is None:
            self.page.snack_bar = SnackBar(Text("No user is currently logged in"), open=True)
            self.page.update()
            return

        if not new_username:
            self.page.snack_bar = SnackBar(Text("New username is required"), open=True)
            self.page.update()
            return

        if len(new_username) < 5 or not new_username.isalpha():
            self.page.snack_bar = SnackBar(Text("Username must be more than 4 characters and only alphabets"), open=True)
            self.page.update()
            return

        message = update_user_username(current_user.username, new_username)
        self.page.snack_bar = SnackBar(Text(f"{message}"), open=True)
        self.page.go("/")
        self.page.update()

    def update_password(self, new_password):
        current_user = User.get_current_user()

        if current_user is None:
            self.page.snack_bar = SnackBar(Text("No user is currently logged in"), open=True)
            self.page.update()
            return

        if not new_password:
            self.page.snack_bar = SnackBar(Text("New password is required"), open=True)
            self.page.update()
            return

        if len(new_password) < 8 or len(new_password) > 16 or not new_password.isalnum():
            self.page.snack_bar = SnackBar(Text("Password must be 8-16 alphanumeric characters"), open=True)
            self.page.update()
            return

        message = update_user_password(current_user.username, new_password)
        self.page.snack_bar = SnackBar(Text(f"{message}"), open=True)
        self.page.go("/")
        self.page.update()

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
        header = Container(
            content=Text("Welcome Back", size=40, color="#26A69A"),
            alignment=alignment.center,
            expand=True,
            padding=Padding(left=20, right=20, top=20, bottom=20),
        )

        # Input fields
        new_username_field = TextField(
            label="New Username",
            bgcolor="#FFFFFF",
            color="#000000",
            border_radius=8,
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
            expand=True,
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
                    Container(
                        width=300,
                        content=new_password_field,
                        alignment=alignment.center
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
                new_username_field.value
            )
        )

        update_password_button = ElevatedButton(
            "Update Password",
            bgcolor="#2abfbf",
            color="#000000",
            width=200,
            on_click=lambda _: self.update_password(
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
