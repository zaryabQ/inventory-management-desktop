import flet as ft
from flet import *
from screens.user import User
from db.db_handler import get_user
import asyncio

class LoginScreen:
    def __init__(self, page: Page):
        self.page = page

    def handle_login(self, name_field, password_field):
        username = name_field.value.strip()
        password = password_field.value.strip()  # Use password_field for password

        # Validation: Check if username and password are provided
        if not username:
            name_field.error_text = "Username is required"
            self.page.update()
            return

        if not password:
            password_field.error_text = "Password is required"
            self.page.update()
            return

        # Fetch user from the database
        user = get_user(username, password)

        if user and user[2] == password:
            User.set_current_user(username, password)
            print(f"Logged in as: {username}")
            self.page.go("/Home")  # Navigate to home screen
        else:
            password_field.error_text = "Incorrect username or password"
            self.page.update()


    def build_login_screen(self):
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
                bgcolor=colors.TEAL_ACCENT_700,
            ),
        )

        logo = Icon(name=icons.ACCOUNT_CIRCLE, size=100, color=colors.BLACK)

        left_side = Container(
            bgcolor=colors.BLUE_GREY_900,
            content=Image(
                src="png/photovoltaic-solar-power-panel-field-green-clean-alternative-power-energy-concept-ai-generative.jpg",
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

    async def show_splash_screen(self):
        # Define the splash screen layout
        splash_screen = Container(
            content=Image(
                src="png/rm373batch10-blogbanner-08.jpg",  # Use your logo file here
                width=200,
                height=200,
                fit=ImageFit.CONTAIN
            ),
            alignment=alignment.center,
            expand=True,
            bgcolor=colors.BLACK,  # Set the background color of the splash screen
        )

        self.page.add(splash_screen)  # Add splash screen to the page
        self.page.update()

        # Asynchronously wait for 6 seconds before transitioning to the login screen
        await asyncio.sleep(3)
        self.page.controls.clear()  # Clear the splash screen
        self.page.add(self.build_login_screen())  # Add the login screen after the splash screen
        self.page.update()

