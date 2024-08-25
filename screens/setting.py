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

def build_setting(page: Page):
    # Create a dummy container for content
    content = Column(
        controls=[
            Text("This is the Settings Screen", size=30, color=TEXT_COLOR),
            Container(height=20),  # Spacer
            ElevatedButton(
                text="Back to Home",
                on_click=lambda e: page.go("/Home"),
                width=120,
                bgcolor=LOGIN_BUTTON_COLOR,
                color=TEXT_COLOR
            )
        ],
        alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER
    )

    # Create a full-size container
    full_size_container = Container(
        content=content,
        expand=True,
        bgcolor=BG
    )

    return full_size_container

def main(page: Page):
    page.title = "Settings"

    # Create the full page layout
    full_page_container = Container(
        content=build_setting(page),
        expand=True
    )

    page.add(full_page_container)

app(target=main)
