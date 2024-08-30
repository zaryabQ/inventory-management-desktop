import flet as ft
from flet import *
import sqlite3

# Constants for styling
TEXT_COLOR = colors.BLACK
LABEL_COLOR = colors.BLACK
BG = colors.BLUE_GREY_800
LEFT_BG = colors.BLUE_GREY_900
LOGIN_BUTTON_COLOR = colors.TEAL_ACCENT_700

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

# Add a sample user (for testing purposes)
def insert_sample_user(username, password):
    try:
        cur.execute("INSERT INTO Users (username, password) VALUES (?, ?)", (username, password))
        con.commit()
    except sqlite3.IntegrityError:
        print("User already exists!")

# Insert a sample user (Remove or comment this out once you have actual users)
# insert_sample_user("ammar", "123")

class LoginScreen:

    def __init__(self, page: Page):
        self.page = page

    def handle_login(self, name_field, password_field):
        username = name_field.value
        password = password_field.value
        
        # Check if the username and password match any record in the database
        cur.execute("SELECT * FROM Users WHERE username = ? AND password = ?", (username, password))
        user = cur.fetchone()

        if user:
            self.page.go("/Home")  # Redirect to home page if login is successful
        else:
            name_field.error_text = "Invalid username or password"
            password_field.error_text = "Invalid username or password"
            self.page.update()  # Refresh the page to show the error

    def build(self):
        name = TextField(
            label="Username",
            color=TEXT_COLOR,
            bgcolor='#ffffff',
            border_color=TEXT_COLOR,
            text_align="center",
            width=250,
        )
        password = TextField(
            label="Password",
            password=True,
            can_reveal_password=True,
            color=TEXT_COLOR,
            bgcolor='#ffffff',
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

        # Container for the left side with image
        left_side = Container(
            bgcolor=LEFT_BG,
            content=Image(
                src="png/mariana-proenca-_h0xG4s6NFg-unsplash.jpg",  # Adjust the path to the image
                fit=ImageFit.COVER,   # Ensure the image covers the container
                expand=True  # Ensure the image expands to fill the container
            ),
            expand=True,  # Take full available height and width
            width=500,  # Ensure the container has a defined width
            height=1000,  # Ensure the container has a defined height
        )

        right_side_container = ft.Container(
            content=ft.Column(
                [
                    logo,
                    ft.Container(height=80),  # Spacer
                    name,
                    password,
                    ft.Container(height=30),  # Spacer
                    login_button
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True
            ),
            bgcolor=BG,
            width=480,  # Set a fixed width for the right side
            expand=False,  # Do not expand beyond its set width
            border=ft.border.all(2, ft.colors.WHITE)  # Add a border with a thickness of 2 and color white
        )

        fullsize = Row(
            controls=[
                left_side,
                right_side_container
            ],
            expand=True,
            alignment=MainAxisAlignment.SPACE_BETWEEN  # Distribute space between left and right sides
        )

        return fullsize
