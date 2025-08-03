import flet as ft
from flet import *
from screens.user import User
from db.db_handler import get_user
from screens.theme import (
    ZeroYellowTheme, 
    zero_yellow_container, 
    zero_yellow_button, 
    zero_yellow_text_field, 
    zero_yellow_text,
    zero_yellow_icon
)
import asyncio

class LoginScreen:
    def __init__(self, page: Page):
        self.page = page

    def handle_login(self, name_field, password_field):
        try:
            username = name_field.value
            password = password_field.value
            
            # Clear any previous error messages
            name_field.error_text = ""
            password_field.error_text = ""
            
            if not username or not password:
                if not username:
                    name_field.error_text = "Username is required"
                if not password:
                    password_field.error_text = "Password is required"
                self.page.update()
                return
            
            # Get user from database
            user = get_user(username, password)
            if user:
                # Save user data in session
                self.page.session.set("username", username)
                self.page.session.set("password", password)
                self.page.session.set("user_id", user[0])
                
                # Navigate to home page
                self.page.go("/Home")
            else:
                # Show error for incorrect credentials
                name_field.error_text = "Incorrect username or password"
                password_field.error_text = "Incorrect username or password"
                self.page.update()
        except Exception as e:
            print(f"Login error: {e}")
            name_field.error_text = "Login failed"
            password_field.error_text = "Login failed"
            self.page.update()

    def build_login_screen(self):
        # Create form fields with zero-yellow guarantee
        name_field = zero_yellow_text_field(
            label="Username",
            hint_text="Enter your username",
            width=300,
            height=55
        )
        
        password_field = zero_yellow_text_field(
            label="Password",
            hint_text="Enter your password",
            password=True,
            can_reveal_password=True,
            width=300,
            height=55
        )

        # Login button with zero yellow
        login_button = zero_yellow_button(
            text="Sign In",
            on_click=lambda e: self.handle_login(name_field, password_field),
            width=300,
            primary=True
        )

        # App logo/icon
        logo = zero_yellow_icon(
            icon=Icons.ACCOUNT_CIRCLE,
            size=80,
            color=ZeroYellowTheme.ACCENT_PRIMARY
        )

        # Left side branding panel
        left_side = Container(
            content=Column([
                Container(height=50),
                zero_yellow_text(
                    "Solar Panel",
                    size=48,
                    weight=FontWeight.BOLD,
                    color=ZeroYellowTheme.TEXT_PRIMARY
                ),
                zero_yellow_text(
                    "Inventory Management",
                    size=24,
                    color=ZeroYellowTheme.TEXT_SECONDARY
                ),
                Container(height=30),
                zero_yellow_text(
                    "Manage your solar panel inventory efficiently",
                    size=16,
                    color=ZeroYellowTheme.TEXT_TERTIARY
                ),
                zero_yellow_text(
                    "Track stock levels, billing, and sales",
                    size=16,
                    color=ZeroYellowTheme.TEXT_TERTIARY
                ),
            ], alignment=MainAxisAlignment.CENTER, horizontal_alignment=CrossAxisAlignment.CENTER),
            bgcolor=ZeroYellowTheme.BG_SECONDARY,
            expand=True,
            width=500,
            height=1000,
        )

        # Right side login form
        right_side = zero_yellow_container(
            content=Column([
                logo,
                Container(height=40),
                zero_yellow_text(
                    "Welcome Back",
                    size=32,
                    weight=FontWeight.BOLD,
                    color=ZeroYellowTheme.TEXT_PRIMARY
                ),
                zero_yellow_text(
                    "Sign in to your account",
                    size=16,
                    color=ZeroYellowTheme.TEXT_SECONDARY
                ),
                Container(height=40),
                name_field,
                Container(height=20),
                password_field,
                Container(height=30),
                login_button,
                Container(height=20),
                zero_yellow_text(
                    "Secure login powered by modern encryption",
                    size=12,
                    color=ZeroYellowTheme.TEXT_TERTIARY
                ),
            ], alignment=MainAxisAlignment.CENTER, horizontal_alignment=CrossAxisAlignment.CENTER),
            width=500,
            height=600,
            bgcolor=ZeroYellowTheme.BG_GLASS,
            border_color=ZeroYellowTheme.GLASS_BORDER
        )

        # Main layout
        fullsize = Container(
            content=Row([
                left_side,
                right_side,
            ], alignment=MainAxisAlignment.CENTER, vertical_alignment=CrossAxisAlignment.CENTER),
            expand=True,
            bgcolor=ZeroYellowTheme.BG_PRIMARY,
        )

        return fullsize

    async def show_splash_screen(self):
        # Simple splash screen with zero yellow
        splash_screen = zero_yellow_container(
            content=Column([
                Image(
                    src="png/Blue Black Minimalist Solar Panel Logo.png",
                    width=200,
                    height=200
                ),
                Container(height=30),
                zero_yellow_text(
                    "Solar Panel Inventory",
                    size=28,
                    weight=FontWeight.BOLD,
                    color=ZeroYellowTheme.TEXT_PRIMARY
                ),
                zero_yellow_text(
                    "Management System",
                    size=20,
                    color=ZeroYellowTheme.TEXT_SECONDARY
                ),
                Container(height=20),
                zero_yellow_text(
                    "Loading...",
                    size=14,
                    color=ZeroYellowTheme.TEXT_TERTIARY
                ),
            ], alignment=MainAxisAlignment.CENTER, horizontal_alignment=CrossAxisAlignment.CENTER),
            width=400,
            height=400,
            bgcolor=ZeroYellowTheme.BG_TERTIARY,
        )

        # Display splash screen
        splash_container = Container(
            content=splash_screen,
            alignment=alignment.center,
            expand=True,
            bgcolor=ZeroYellowTheme.BG_PRIMARY,
        )

        self.page.clean()
        self.page.add(splash_container)
        self.page.update()
        
        # Wait for 3 seconds
        await asyncio.sleep(3)
        
        # Clear splash and show login
        self.page.clean()
        self.page.add(self.build_login_screen())
        self.page.update()

