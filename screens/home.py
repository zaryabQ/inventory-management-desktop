import flet as ft
import sqlite3
from flet import *
from screens.theme import (
    ZeroYellowTheme, 
    zero_yellow_container, 
    zero_yellow_text, 
    zero_yellow_button,
    zero_yellow_icon,
    # Legacy compatibility
    IOS26Theme,
    glass_container,
    modern_card,
    heading_text,
    body_text,
    caption_text,
    modern_nav_bar,
    modern_icon,
    stat_card
)

class HomeScreen:
    def __init__(self, page: Page):
        self.page = page
        self.db_connection = self.connect_to_db()

    def connect_to_db(self):
        # Connect to the SQLite database (or create one if it doesn't exist)
        conn = sqlite3.connect("db/sql.db")
        return conn

    def fetch_total_sales(self):
        cursor = self.db_connection.cursor()
        # Update the query to match the actual column name (total_cost)
        cursor.execute("SELECT SUM(total_cost) FROM billing")
        result = cursor.fetchone()
        return result[0] if result[0] else 0

    def fetch_total_profit(self):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT SUM(profit) FROM billing")
        result = cursor.fetchone()
        return result[0] if result[0] else 0

    def fetch_total_cost(self):
        cursor = self.db_connection.cursor()
        # If cost is represented by total_cost, use the same column
        cursor.execute("SELECT SUM(total_cost) FROM billing")
        result = cursor.fetchone()
        return result[0] if result[0] else 0

    def fetch_inventory_info(self):
        cursor = self.db_connection.cursor()
        
        # Get total items
        cursor.execute("SELECT COUNT(*) FROM inventory")
        total_items = cursor.fetchone()[0]
        print(f"Total items in inventory: {total_items}")

        # Get low stock items (where quantity < 50)
        cursor.execute("SELECT COUNT(*) FROM inventory WHERE quantity < 50")
        low_stock_items = cursor.fetchone()[0]
        print(f"Low stock items: {low_stock_items}")

        # Get items to be received (where status = 'unpaid' or similar)
        cursor.execute("SELECT COUNT(*) FROM billing WHERE LOWER(status) = 'unpaid'")
        to_be_received_items = cursor.fetchone()[0]
        print(f"Unpaid billing items (to be received): {to_be_received_items}")

        return total_items, low_stock_items, to_be_received_items

    def create_stat_card(self, title, value, icon_name, color):
        """Create a sophisticated stat card with monochromatic styling"""
        display_value = f"Rs. {value:,}" if isinstance(value, (int, float)) else str(value)
        return stat_card(
            title=title,
            value=display_value,
            icon_name=icon_name,
            icon_color=color
        )

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

    def build(self):
        # Fetch dynamic values from the database
        total_sales = self.fetch_total_sales()
        total_profit = self.fetch_total_profit()
        total_cost = self.fetch_total_cost()
        total_items, low_stock_items, to_be_received_items = self.fetch_inventory_info()

        # Left side navigation with glass effect
        navigation_bar = zero_yellow_container(
            content=Column(
                controls=[
                    Container(height=20),
                    zero_yellow_text(
                        "Dashboard",
                        size=24,
                        weight=FontWeight.BOLD,
                        color=ZeroYellowTheme.PURE_BLACK  # Black heading for visibility
                    ),
                    Container(height=30),
                    self.create_navigation_button("Dashboard", "/Home", Icons.DASHBOARD, True),
                    Container(height=12),
                    self.create_navigation_button("Inventory", "/Inventory", Icons.INVENTORY),
                    Container(height=12),
                    self.create_navigation_button("Billing", "/Billing", Icons.RECEIPT),
                    Container(height=12),
                    self.create_navigation_button("Settings", "/Settings", Icons.SETTINGS),
                    Container(height=20),
                    # User info section
                    glass_container(
                        content=Column(
                            controls=[
                                zero_yellow_icon(
                                    icon=Icons.ACCOUNT_CIRCLE,
                                    size=48,
                                    color=ZeroYellowTheme.PURE_BLACK  # Black icon for visibility
                                ),
                                Container(height=8),
                                body_text(
                                    "Admin User",
                                    size=16,
                                    color=IOS26Theme.TEXT_PRIMARY,
                                    weight=FontWeight.W_600
                                ),
                                caption_text(
                                    "System Administrator",
                                    size=12,
                                    color=IOS26Theme.TEXT_TERTIARY
                                )
                            ],
                            horizontal_alignment=CrossAxisAlignment.CENTER
                        ),
                        padding=16,
                        margin=0,
                        bgcolor=IOS26Theme.GLASS_BACKGROUND
                    )
                ],
                expand=True,
                horizontal_alignment=CrossAxisAlignment.CENTER
            ),
            width=280,
            height=800,
            padding=20,
            margin=20,
            bgcolor=IOS26Theme.GLASS_BACKGROUND
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
                                    heading_text(
                                        "Welcome Back!",
                                        size=36,
                                        color=IOS26Theme.TEXT_PRIMARY
                                    ),
                                    body_text(
                                        "Here's what's happening with your inventory today",
                                        size=16,
                                        color=IOS26Theme.TEXT_SECONDARY
                                    )
                                ],
                                horizontal_alignment=CrossAxisAlignment.START
                            ),
                            Container(expand=True),
                            modern_icon(
                                name=Icons.NOTIFICATIONS,
                                size=28,
                                color=IOS26Theme.TEXT_SECONDARY
                            )
                        ],
                        alignment=MainAxisAlignment.SPACE_BETWEEN
                    ),
                    Container(height=40),
                    
                    # Stats Grid
                    Row(
                        controls=[
                            self.create_stat_card("Total Sales", total_sales, Icons.TRENDING_UP, IOS26Theme.ACCENT_PRIMARY),
                            Container(width=20),
                            self.create_stat_card("Total Profit", total_profit, Icons.ACCOUNT_BALANCE_WALLET, IOS26Theme.ACCENT_SECONDARY),
                            Container(width=20),
                            self.create_stat_card("Total Cost", total_cost, Icons.PAYMENTS, IOS26Theme.ACCENT_TERTIARY),
                        ],
                        alignment=MainAxisAlignment.START
                    ),
                    Container(height=30),
                    
                    # Inventory Overview
                    Row(
                        controls=[
                            self.create_stat_card("Total Items", total_items, Icons.INVENTORY, IOS26Theme.ACCENT_PRIMARY),
                            Container(width=20),
                            self.create_stat_card("Low Stock", low_stock_items, Icons.WARNING, IOS26Theme.ACCENT_SECONDARY),
                            Container(width=20),
                            self.create_stat_card("To be Received", to_be_received_items, Icons.PENDING, IOS26Theme.ACCENT_TERTIARY),
                        ],
                        alignment=MainAxisAlignment.START
                    ),
                    Container(height=40),
                    
                    # Quick Actions
                    zero_yellow_container(
                        content=Column(
                            controls=[
                                zero_yellow_text(
                                    "Quick Actions",
                                    size=24,
                                    weight=FontWeight.BOLD,
                                    color=ZeroYellowTheme.TEXT_PRIMARY
                                ),
                                Container(height=20),
                                Row(
                                    controls=[
                                        zero_yellow_container(
                                            content=Column(
                                                controls=[
                                                    zero_yellow_icon(
                                                        icon=Icons.ADD,
                                                        size=32,
                                                        color=ZeroYellowTheme.TEXT_PRIMARY
                                                    ),
                                                    Container(height=8),
                                                    zero_yellow_text(
                                                        "Add Item",
                                                        size=14,
                                                        color=ZeroYellowTheme.TEXT_PRIMARY
                                                    )
                                                ],
                                                horizontal_alignment=CrossAxisAlignment.CENTER
                                            ),
                                            on_click=lambda _: self.page.go("/Inventory"),
                                            padding=20,
                                            border_radius=12,
                                            bgcolor=ZeroYellowTheme.BG_TERTIARY
                                        ),
                                        Container(width=20),
                                        zero_yellow_container(
                                            content=Column(
                                                controls=[
                                                    zero_yellow_icon(
                                                        icon=Icons.RECEIPT,
                                                        size=32,
                                                        color=ZeroYellowTheme.TEXT_PRIMARY
                                                    ),
                                                    Container(height=8),
                                                    zero_yellow_text(
                                                        "New Bill",
                                                        size=14,
                                                        color=ZeroYellowTheme.TEXT_PRIMARY
                                                    )
                                                ],
                                                horizontal_alignment=CrossAxisAlignment.CENTER
                                            ),
                                            on_click=lambda _: self.page.go("/Billing"),
                                            padding=20,
                                            border_radius=12,
                                            bgcolor=ZeroYellowTheme.BG_TERTIARY
                                        )
                                    ],
                                    alignment=MainAxisAlignment.START
                                )
                            ],
                            horizontal_alignment=CrossAxisAlignment.START
                        ),
                        padding=24,
                        margin=0
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
