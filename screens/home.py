import flet as ft
import sqlite3
from flet import *

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


    def build(self):
        # Fetch dynamic values from the database
        total_sales = self.fetch_total_sales()
        total_profit = self.fetch_total_profit()
        total_cost = self.fetch_total_cost()
        total_items, low_stock_items, to_be_received_items = self.fetch_inventory_info()

        # Left side menu bar
        menu_bar = Container(
            width=250,
            bgcolor="#383838",
            padding=10,
            content=Column(
                expand=True,
                controls=[
                    Text("Dashboard", color="#00D0FF", size=20, weight="bold"),
                    Container(height=20),
                    Container(
                        width=180,
                        height=50,
                        margin=margin.only(bottom=30),
                        content=ElevatedButton(
                            on_click=lambda _: self.page.go("/Home"),
                            text="Dashboard",
                            bgcolor="#2C2C2C",
                            color="white",
                            expand=True,
                        ),
                    ),
                    Container(
                        width=180,
                        height=50,
                        margin=margin.only(bottom=30),
                        content=ElevatedButton(
                            on_click=lambda _: self.page.go("/Inventory"),
                            text="Inventory",
                            bgcolor="#2C2C2C",
                            color="white",
                            expand=True,
                        ),
                    ),
                    Container(
                        width=180,
                        height=50,
                        margin=margin.only(bottom=30),
                        content=ElevatedButton(
                            on_click=lambda _: self.page.go("/Billing"),
                            text="Billing",
                            bgcolor="#2C2C2C",
                            color="white",
                            expand=True,
                        ),
                    ),
                    Container(
                        width=180,
                        height=50,
                        margin=margin.only(bottom=30),
                        content=ElevatedButton(
                            on_click=lambda _: self.page.go("/Settings"),
                            text="Settings",
                            bgcolor="#2C2C2C",
                            color="white",
                            expand=True,
                        ),
                    ),
                ],
            ),
        )

        # Right side content
        content_area = Container(
            expand=True,
            bgcolor="#2C2C2C",
            padding=25,
            content=Column(
                horizontal_alignment=CrossAxisAlignment.CENTER,
                alignment=MainAxisAlignment.CENTER,
                expand=True,
                controls=[
                    Text(value="Welcome Back", color="#26A69A", size=40),
                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        expand=True,
                        controls=[
                            Container(
                                expand=True,  # Expand box according to available space
                                bgcolor="white",
                                border_radius=10,
                                padding=10,
                                content=Column(
                                    horizontal_alignment=CrossAxisAlignment.CENTER,
                                    alignment=MainAxisAlignment.CENTER,
                                    expand=True,
                                    controls=[
                                        Text("Overview", size=40, weight="bold"),
                                        Text("Total Sales", size=25,weight="bold"),
                                        Text(f"Rs:{total_sales}", size=16),
                                        Text("Profit", size=25,weight="bold"),
                                        Text(f"Rs:{total_profit}", size=16),
                                        Text("Total Cost", size=25,weight="bold"),
                                        Text(f"Rs:{total_cost}", size=16),
                                    ],
                                ),
                            ),
                            Container(
                                expand=True,  # Expand box according to available space
                                bgcolor="white",
                                border_radius=10,
                                padding=10,
                                content=Column(
                                    horizontal_alignment=CrossAxisAlignment.CENTER,
                                    alignment=MainAxisAlignment.CENTER,
                                    expand=True,
                                    controls=[
                                        Text("Inventory", size=40, weight="bold"),
                                        Text("Total Items", size=25,weight="bold"),
                                        Text(f"{total_items}", size=16),
                                        Text("Low Stock", size=25,weight="bold"),
                                        Text(f"{low_stock_items}", size=16),
                                        Text("To be Received", size=25,weight="bold"),
                                        Text(f"{to_be_received_items}", size=16),
                                    ],
                                ),
                            ),
                        ],
                    ),
                ],
            ),
        )

        # Main layout combining menu bar and content area
        layout = Row(
            expand=True,
            controls=[
                menu_bar,
                content_area,
            ],
        )

        return layout
