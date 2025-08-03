import flet as ft
from flet import *
from screens.user import User
from db.db_handler import update_user_username, update_user_password
from screens.theme import (
    ZeroYellowTheme, 
    zero_yellow_container, 
    zero_yellow_button, 
    zero_yellow_text_field, 
    zero_yellow_text,
    zero_yellow_icon,
    zero_yellow_snackbar,
    # Legacy compatibility
    IOS26Theme,
    glass_container,
    modern_card,
    heading_text,
    body_text,
    caption_text,
    primary_button,
    secondary_button,
    modern_text_field,
    modern_icon
)

class SettingsScreen:
    def __init__(self, page: Page):
        self.page = page

    def create_navigation_button(self, text, route, icon_name, is_active=False):
        """Create a modern navigation button with zero yellow styling"""
        return zero_yellow_container(
            content=Column(
                controls=[
                    zero_yellow_icon(
                        icon=icon_name,
                        size=24,
                        color=ZeroYellowTheme.PURE_WHITE if is_active else ZeroYellowTheme.TEXT_QUATERNARY  # White when focused
                    ),
                    Container(height=8),
                    zero_yellow_text(
                        text,
                        size=14,
                        color=ZeroYellowTheme.PURE_WHITE if is_active else ZeroYellowTheme.TEXT_QUATERNARY,  # White when focused
                        weight=FontWeight.W_500
                    )
                ],
                horizontal_alignment=CrossAxisAlignment.CENTER,
                spacing=4
            ),
            on_click=lambda _: self.page.go(route),
            padding=16,
            border_radius=12,
            bgcolor=ZeroYellowTheme.BG_PRIMARY if is_active else ZeroYellowTheme.BG_GLASS,  # Dark background when focused
            border_color=ZeroYellowTheme.GLASS_BORDER if is_active else "transparent"
        )

    def update_username(self, new_username):
        current_user = User.get_current_user()
        if current_user is None:
            self.page.snack_bar = zero_yellow_snackbar("No user is currently logged in")
            self.page.snack_bar.open = True
            self.page.update()
            return

        if not new_username:
            self.page.snack_bar = zero_yellow_snackbar("New username is required")
            self.page.update()
            return

        if len(new_username) < 5 or not new_username.isalpha():
            self.page.snack_bar = zero_yellow_snackbar("Username must be more than 4 characters and only alphabets")
            self.page.update()
            return

        message = update_user_username(current_user.username, new_username)
        self.page.snack_bar = zero_yellow_snackbar(f"{message}")
        self.page.go("/")
        self.page.update()

    def update_password(self, new_password):
        current_user = User.get_current_user()

        if current_user is None:
            self.page.snack_bar = zero_yellow_snackbar("No user is currently logged in")
            self.page.update()
            return

        if not new_password:
            self.page.snack_bar = zero_yellow_snackbar("New password is required")
            self.page.update()
            return

        if len(new_password) < 8 or len(new_password) > 16 or not new_password.isalnum():
            self.page.snack_bar = zero_yellow_snackbar("Password must be 8-16 alphanumeric characters")
            self.page.update()
            return

        message = update_user_password(current_user.username, new_password)
        self.page.snack_bar = zero_yellow_snackbar(f"{message}")
        self.page.go("/")
        self.page.update()

    def build(self):
        # Left side navigation with glass effect
        navigation_bar = zero_yellow_container(
            content=Column(
                controls=[
                    Container(height=20),
                    zero_yellow_text(
                        "Settings",
                        size=24,
                        weight=FontWeight.BOLD,
                        color=ZeroYellowTheme.PURE_BLACK  # Black heading for visibility
                    ),
                    Container(height=30),
                    self.create_navigation_button("Dashboard", "/Home", Icons.DASHBOARD),
                    Container(height=12),
                    self.create_navigation_button("Inventory", "/Inventory", Icons.INVENTORY),
                    Container(height=12),
                    self.create_navigation_button("Billing", "/Billing", Icons.RECEIPT),
                    Container(height=12),
                    self.create_navigation_button("Settings", "/Settings", Icons.SETTINGS, True),
                    Container(height=20),
                    # User info section
                    zero_yellow_container(
                        content=Column(
                            controls=[
                                zero_yellow_icon(
                                    icon=Icons.ACCOUNT_CIRCLE,
                                    size=48,
                                    color=ZeroYellowTheme.PURE_BLACK  # Black icon for visibility
                                ),
                                Container(height=8),
                                zero_yellow_text(
                                    "Admin User",
                                    size=16,
                                    color=ZeroYellowTheme.TEXT_PRIMARY,
                                    weight=FontWeight.W_600
                                ),
                                zero_yellow_text(
                                    "System Administrator",
                                    size=12,
                                    color=ZeroYellowTheme.TEXT_TERTIARY
                                )
                            ],
                            horizontal_alignment=CrossAxisAlignment.CENTER
                        ),
                        padding=padding.all(16),
                        margin=margin.all(0)
                    )
                ],
                expand=True,
                horizontal_alignment=CrossAxisAlignment.CENTER
            ),
            width=280,
            height=800,
            padding=padding.all(20),
            margin=margin.all(20)
        )

        # Input fields
        new_username_field = zero_yellow_text_field(
            label="New Username",
            hint_text="Enter new username",
            width=350,
            height=55
        )

        new_password_field = zero_yellow_text_field(
            label="New Password",
            hint_text="Enter new password",
            password=True,
            can_reveal_password=True,
            width=350,
            height=55
        )

        # Main content area - responsive
        content_area = Container(
            expand=True,
            bgcolor=ZeroYellowTheme.BG_PRIMARY,
            padding=padding.symmetric(horizontal=20, vertical=15),  # Responsive padding
            content=Column(
                controls=[
                    # Header
                    Row(
                        controls=[
                            Column(
                                controls=[
                                    zero_yellow_text(
                                        "Account Settings",
                                        size=36,
                                        weight=FontWeight.BOLD,
                                        color=ZeroYellowTheme.PURE_BLACK  # Black heading
                                    ),
                                    zero_yellow_text(
                                        "Update your account information",
                                        size=16,
                                        color=ZeroYellowTheme.TEXT_SECONDARY
                                    )
                                ],
                                horizontal_alignment=CrossAxisAlignment.START
                            ),
                            Container(expand=True),
                            zero_yellow_icon(
                                icon=Icons.SETTINGS,
                                size=32,
                                color=ZeroYellowTheme.PURE_BLACK  # Black icon
                            )
                        ],
                        alignment=MainAxisAlignment.SPACE_BETWEEN
                    ),
                    Container(height=40),
                    
                    # Settings Form
                    Row(
                        controls=[
                            # Left side - Form fields
                            zero_yellow_container(
                                content=Column(
                                    controls=[
                                        zero_yellow_text(
                                            "Update Information",
                                            size=24,
                                            weight=FontWeight.BOLD,
                                            color=ZeroYellowTheme.PURE_BLACK
                                        ),
                                        Container(height=30),
                                        new_username_field,
                                        Container(height=20),
                                        new_password_field,
                                        Container(height=30),
                                        Row(
                                            controls=[
                                                zero_yellow_button(
                                                    text="Update Username",
                                                    on_click=lambda _: self.update_username(new_username_field.value),
                                                    width=160,
                                                    height=45,
                                                    primary=True
                                                ),
                                                Container(width=20),
                                                zero_yellow_button(
                                                    text="Update Password",
                                                    on_click=lambda _: self.update_password(new_password_field.value),
                                                    width=160,
                                                    height=45,
                                                    primary=True
                                                ),
                                            ],
                                            alignment=MainAxisAlignment.CENTER,
                                        ),
                                    ],
                                    horizontal_alignment=CrossAxisAlignment.CENTER,
                                    spacing=20
                                ),
                                width=400,
                                height=400,
                                padding=30
                            ),
                            
                            Container(width=40),
                            
                            # Right side - Account info
                            zero_yellow_container(
                                content=Column(
                                    controls=[
                                        zero_yellow_icon(
                                            icon=Icons.ACCOUNT_CIRCLE,
                                            size=80,
                                            color=ZeroYellowTheme.PURE_BLACK
                                        ),
                                        Container(height=20),
                                        zero_yellow_text(
                                            "Account Details",
                                            size=24,
                                            weight=FontWeight.BOLD,
                                            color=ZeroYellowTheme.PURE_BLACK
                                        ),
                                        Container(height=20),
                                        zero_yellow_container(
                                            content=Column(
                                                controls=[
                                                    Row(
                                                        controls=[
                                                            zero_yellow_icon(
                                                                icon=Icons.PERSON,
                                                                size=20,
                                                                color=ZeroYellowTheme.PURE_BLACK
                                                            ),
                                                            Container(width=10),
                                                            zero_yellow_text(
                                                                "Username: admin",
                                                                size=16,
                                                                color=ZeroYellowTheme.TEXT_PRIMARY
                                                            )
                                                        ],
                                                        alignment=MainAxisAlignment.START
                                                    ),
                                                    Container(height=10),
                                                    Row(
                                                        controls=[
                                                            zero_yellow_icon(
                                                                icon=Icons.EMAIL,
                                                                size=20,
                                                                color=ZeroYellowTheme.PURE_BLACK
                                                            ),
                                                            Container(width=10),
                                                            zero_yellow_text(
                                                                "Role: Administrator",
                                                                size=16,
                                                                color=ZeroYellowTheme.TEXT_PRIMARY
                                                            )
                                                        ],
                                                        alignment=MainAxisAlignment.START
                                                    ),
                                                    Container(height=10),
                                                    Row(
                                                        controls=[
                                                            zero_yellow_icon(
                                                                icon=Icons.SECURITY,
                                                                size=20,
                                                                color=ZeroYellowTheme.PURE_BLACK
                                                            ),
                                                            Container(width=10),
                                                            zero_yellow_text(
                                                                "Status: Active",
                                                                size=16,
                                                                color=ZeroYellowTheme.TEXT_PRIMARY
                                                            )
                                                        ],
                                                        alignment=MainAxisAlignment.START
                                                    ),
                                                ],
                                                horizontal_alignment=CrossAxisAlignment.START,
                                                spacing=8
                                            ),
                                            padding=20,
                                            margin=0
                                        ),
                                        Container(height=30),
                                        zero_yellow_button(
                                            text="Logout",
                                            on_click=lambda _: self.page.go("/"),
                                            width=200,
                                            height=45,
                                            primary=False
                                        )
                                    ],
                                    horizontal_alignment=CrossAxisAlignment.CENTER,
                                    spacing=20
                                ),
                                width=350,
                                height=400,
                                padding=30
                            )
                        ],
                        alignment=MainAxisAlignment.CENTER
                    )
                ],
                horizontal_alignment=CrossAxisAlignment.START,
                expand=True
            )
        )

        # Main layout combining navigation and content
        layout = Row(
            expand=True,
            controls=[
                navigation_bar,
                content_area,
            ],
        )

        return layout
