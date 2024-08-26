import flet as ft
from flet import *
import sqlite3

TEXT_COLOR = colors.BLACK
LABEL_COLOR = colors.BLACK
BG = colors.BLUE_GREY_800
LEFT_BG = colors.BLUE_GREY_900
LOGIN_BUTTON_COLOR = colors.TEAL_ACCENT_700
TEXT_FIELD_BG = '#fffff'

# Set up SQLite connection
con = sqlite3.connect('db/sql.db', check_same_thread=False)
cur = con.cursor()

# Create the users table if it doesn't exist
cur.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
''')
con.commit()

class LoginScreen:

    def __init__(self, page: Page):
        self.page = page

    def handle_login(self,name,password):

        self.page.go("/Home")


    def build(self):
        name = TextField(
            label="Username",
            color=TEXT_COLOR,
            bgcolor=TEXT_FIELD_BG,
            border_color=TEXT_COLOR,
            text_align="center",
            width=250,
        )
        password = TextField(
            label="Password",
            password=True,
            can_reveal_password=True,
            color=TEXT_COLOR,
            bgcolor=TEXT_FIELD_BG,
            border_color=TEXT_COLOR,
            text_align="center",
            width=250,
        )

        # Create the login button
        login_button = ElevatedButton(
            text="Login",
            on_click=lambda e: self.handle_login(name, password),
            width=120,
            style=ButtonStyle(
                color=TEXT_COLOR,
                bgcolor=LOGIN_BUTTON_COLOR
            )
        )
        logo = Icon(name=icons.ACCOUNT_CIRCLE, size=100, color=TEXT_COLOR)

        left_side = Container(
            bgcolor=colors.BLUE_GREY_900,
            expand=7,  # Takes 70% width
            content=Image(
                src="png/person-with-solar-panel.jpg",  # Ensure the image is in your assets or provide the correct path
                fit=ImageFit.COVER,
                expand=True
            )
        )

        right_side_container = Container(
            content=Column(
                [
                    logo,
                    Container(height=20),  # Spacer
                    name,
                    password,
                    Container(height=20),  # Spacer
                    login_button
                ],
                alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                expand=True
            ),
            bgcolor=BG,
            expand=3,  
        )

        fullsize = Container(
            content=Row(
                [
                    left_side,
                    right_side_container
                ],
                alignment=MainAxisAlignment.CENTER,  # Ensure the containers fill the available space
                expand=True
            ),
            alignment= alignment.center,
            width=self.page.width,
            height=self.page.height

        )

        return fullsize