from flet import *
import sqlite3

# Define colors
TEXT_COLOR = colors.BLACK
LABEL_COLOR = colors.BLACK
BG = colors.BLUE_GREY_800
LEFT_BG = colors.BLUE_GREY_900
LOGIN_BUTTON_COLOR = colors.TEAL_ACCENT_700
TEXT_FIELD_BG = '#FFFFFF'

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

def build_login(page: Page):
    # Create the username and password fields
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
        on_click=lambda e: handle_login(page, name, password),
        width=120,
        style=ButtonStyle(
            color=TEXT_COLOR,
            bgcolor=LOGIN_BUTTON_COLOR
        )
    )

    # Create the logo
    logo = Icon(name=icons.ACCOUNT_CIRCLE, size=100, color=TEXT_COLOR)

    # Create the right side layout
    right_side = Column(
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
    )

    return right_side

def handle_login(page: Page, name, password):
    print("none")
    #page.go("/Home")
    # Add your login logic here
    # e.g., Check username and password against the database

def main(page: Page):
    page.title = "Login"
    
    left_side = Container(
        bgcolor=LEFT_BG,
        expand=7,  # Takes 70% width
        content=Image(
            src="png/person-with-solar-panel.jpg",  # Ensure the image is in your assets or provide the correct path
            fit=ImageFit.COVER,
            expand=True
        )
    )

    right_side_container = Container(
        content=build_login(page),
        bgcolor=BG,
        expand=3,  # Takes 30% width
    )

    main_layout = Row(
        [
            left_side,
            right_side_container
        ],
        alignment=MainAxisAlignment.CENTER,  # Ensure the containers fill the available space
        expand=True
    )

    # Create a container that expands to fill the whole window
    full_page_container = Container(
        content=main_layout,
        expand=True
    )

    page.add(full_page_container)

app(target=main)
