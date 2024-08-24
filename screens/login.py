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

class Login(UserControl):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page

    def handle_login(self, e):
        username = self.name.value
        password_value = self.password.value

        res = cur.execute(
            '''SELECT * FROM Users WHERE username = ? AND password = ?''',
            (username, password_value)
        )
        users = res.fetchall()
        if users:
            self.page.go("/Home")
        else:
            print("Error! Invalid credentials")

    def build_login(self):
        # Create the username and password fields
        self.name = TextField(
            label="Username",
            color=TEXT_COLOR,
            bgcolor=TEXT_FIELD_BG,
            border_color=TEXT_COLOR,
            text_align="center",
            width=250,
        )
        self.password = TextField(
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
            on_click=self.handle_login,
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
                self.name,
                self.password,
                Container(height=20),  # Spacer
                login_button
            ],
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER,
            expand=True
        )

        return right_side

    def build(self):
        left_side = Container(
            bgcolor=LEFT_BG,
            expand=7,  # Takes 70% width
           # height=1,  # Takes full height of the parent container
            content=Image(
                src="png/person-with-solar-panel.jpg",  # Ensure the image is in your assets or provide the correct path
                fit=ImageFit.COVER,
                expand=True
            )
        )

        right_side_container = Container(
            content=self.build_login(),
            bgcolor=BG,
            expand = 3,  # Takes 30% width
           # height=1,  # Takes full height of the parent container
        )

        main_layout = Row(
            [
                left_side,
                right_side_container
            ],
            alignment=MainAxisAlignment.CENTER,  # Ensure the containers fill the available space
            expand=True
        )

        return main_layout

def main(page: Page):
    page.title = "Cashier App"
    
    # Create a container that expands to fill the whole window
    full_page_container = Container(
        content=Login(page),
        expand=True
    )

    page.add(full_page_container)

app(target=main)
