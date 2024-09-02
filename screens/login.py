import flet as ft
from flet import *
from screens.user import User
from db.db_handler import get_user

class LoginScreen:
    def __init__(self, page: Page):
        self.page = page

    def handle_login(self, name_field, password_field):
        username = name_field.value.strip()
        password = password_field.value.strip()

        # Input validations
        if not username:
            name_field.error_text = "Username is required"
            self.page.update()
            return

        if not password:
            password_field.error_text = "Password is required"
            self.page.update()
            return

        # Fetch user from database using the new db_handler function
        user = get_user(username,password)

        if user:
            if user[2] == password:
                User.set_current_user(username, password)
                print(f"Logged in as: {username}")
                self.page.go("/Home")
            else:
                password_field.error_text = "Incorrect password"
        else:
            name_field.error_text = "Username does not exist"

        self.page.update()

    def build(self):
        name = TextField(
            label="Username",
            color=colors.BLACK,
            bgcolor='#ffffff',
            border_color=colors.BLACK,
            text_align="center",
            width=250,
        )
        password = TextField(
            label="Password",
            password=True,
            can_reveal_password=True,
            color=colors.BLACK,
            bgcolor='#ffffff',
            border_color=colors.BLACK,
            text_align="center",
            width=250,
        )

        login_button = ElevatedButton(
            text="Login",
            on_click=lambda e: self.handle_login(name, password),
            width=120,
            style=ButtonStyle(
                color=colors.BLACK,
                bgcolor=colors.TEAL_ACCENT_700
            )
        )

        logo = Icon(name=icons.ACCOUNT_CIRCLE, size=100, color=colors.BLACK)

        left_side = Container(
            bgcolor=colors.BLUE_GREY_900,
            content=Image(
                src="png/mariana-proenca-_h0xG4s6NFg-unsplash.jpg",
                fit=ImageFit.COVER,
                expand=True
            ),
            expand=True,
            width=500,
            height=1000,
        )

        right_side_container = ft.Container(
            content=ft.Column(
                [
                    logo,
                    ft.Container(height=80),
                    name,
                    password,
                    ft.Container(height=30),
                    login_button
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True
            ),
            bgcolor=colors.BLUE_GREY_800,
            width=480,
            expand=False,
            border=ft.border.all(2, ft.colors.WHITE)
        )

        fullsize = Row(
            controls=[
                left_side,
                right_side_container
            ],
            expand=True,
            alignment=MainAxisAlignment.SPACE_BETWEEN
        )

        return fullsize
