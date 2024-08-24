import flet as ft
import sqlite3

# Define colors
TEXT_COLOR = ft.colors.BLACK
LABEL_COLOR = ft.colors.BLACK
BG = ft.colors.BLUE_GREY_800
LEFT_BG = ft.colors.BLUE_GREY_900
LOGIN_BUTTON_COLOR = ft.colors.TEAL_ACCENT_700
TEXT_FIELD_BG = '#FFFFFF'

# Set up SQLite connection
con = sqlite3.connect('sql.db', check_same_thread=False)
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

def handle_login(page: ft.Page, name: ft.TextField, password: ft.TextField):
    username = name.value
    password_value = password.value

    res = cur.execute(
        '''SELECT * FROM Users WHERE username = ? AND password = ?''',
        (username, password_value)
    )
    users = res.fetchall()
    if users:
        page.go("/Home")
    else:
        print("Error! Invalid credentials")

def build_login(page: ft.Page):
    # Create the username and password fields
    name = ft.TextField(
        label="Username",
        color=TEXT_COLOR,
        bgcolor=TEXT_FIELD_BG,
        border_color=TEXT_COLOR,
        text_align="center",
        width=250,
      
    )
    password = ft.TextField(
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
    login_button = ft.ElevatedButton(
        text="Login",
        on_click=lambda e: handle_login(page, name, password),
        width=120,
        style=ft.ButtonStyle(
            color=TEXT_COLOR,
            bgcolor=LOGIN_BUTTON_COLOR
        )
    )

    # Create the logo
    logo = ft.Icon(name=ft.icons.ACCOUNT_CIRCLE, size=100, color=TEXT_COLOR)

    # Create the right side layout
    right_side = ft.Column(
        [
            logo,
            ft.Container(height=20),  # Spacer
            name,
            password,
            ft.Container(height=20),  # Spacer
            login_button
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    return right_side

def main(page: ft.Page):
    page.title = "Login"
    page.window.width = 1280
    page.window.height = 720
    page.window.resizable = True
    page.window.bgcolor = ft.colors.WHITE

    left_side = ft.Container(
        width=650,
        height=page.window.height,
        bgcolor=LEFT_BG,
        content=ft.Image(
            src="person-with-solar-panel.jpg",
            fit=ft.ImageFit.COVER,
            expand=True
        )
    )

    right_side_container = ft.Container(
        content=build_login(page),
        padding=20,
        bgcolor=BG,
        width=400,
        expand=True
    )

    main_layout = ft.Row(
        [
            left_side,
            right_side_container
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True
    )

    page.add(main_layout)

ft.app(target=main)
