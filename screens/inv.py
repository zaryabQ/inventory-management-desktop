import flet as ft
from flet import *
import sqlite3

class InventoryScreen:
    def __init__(self, page: Page):
        self.page = page
        self.inventory = []

    def load_inventory(self):
        try:
            con = sqlite3.connect("db/sql.db")
            cur = con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS Inventory (id INTEGER PRIMARY KEY, product_name TEXT, quantity INTEGER, price REAL)")
            res = cur.execute("SELECT * FROM Inventory")
            self.inventory = [i for i in res.fetchall()]
        except sqlite3.OperationalError as e:
            print(f"Database error: {e}")
            print("Ensure that the 'Inventory' table exists in the database.")
        except Exception as e:
            print(f"General error: {e}")

    def create_menu_button(self, text, route):
        """Helper function to create menu buttons."""
        return Container(
            width=180,
            height=50,
            margin=margin.only(bottom=10),
            content=ElevatedButton(
                text=text,
                on_click=lambda _: self.page.go(route),
                bgcolor="#2C2C2C",
                color="white",
                expand=True,
            ),
        )

    def add_item(self, e):
        print("Add Item clicked")
        # Logic to add item

    def search_item(self, e):
        print(f"Searching for {e.control.value}")
        # Logic to filter table based on search

    def update_item(self, id):
        print(f"Updating item {id}")
        # Logic to update item

    def remove_item(self, id):
        print(f"Removing item {id}")
        # Logic to remove item

    def build(self):
        self.load_inventory()

        # Left side menu bar
        menu_bar = Container(
            width=250,
            bgcolor="#383838",
            padding=10,
            content=Column(
                expand=True,
                controls=[
                    Text("Inventory", color="#00D0FF", size=20, weight="bold"),
                    Container(height=20),
                    self.create_menu_button("Dashboard", "/Home"),
                    Container(height=10),
                    self.create_menu_button("Inventory", "/Inventory"),
                    Container(height=10),
                    self.create_menu_button("Billing", "/Billing"),
                    Container(height=10),
                    self.create_menu_button("Settings", "/Settings"),
                ],
            ),
        )

        # Header with welcome message
        header = Container(
            bgcolor="#2b3037",
            padding=40,
            content=Row(
                controls=[
                    Container(
                        content=Text("Welcome Back", size=40, color="#26A69A"),
                    ),
                ],
                alignment=MainAxisAlignment.CENTER,
                vertical_alignment=CrossAxisAlignment.CENTER,
            ),
        )

        # Search bar with Add Item button
        search_bar_row = Row(
            controls=[
                Container(
                    content=TextField(
                        hint_text="Search Item",
                        on_change=self.search_item,
                        height=50,
                        bgcolor="#ffffff",
                        border_radius=10,
                    ),
                    width=300,
                    padding=10,
                ),
                Container(width=700),  # Space between search bar and button
                Container(
                    content=ElevatedButton(
                        text="Add Item",
                        on_click=self.add_item,
                        bgcolor="#2abfbf",
                        color="#000000",
                    ),
                    border_radius=20,
                    padding=0,
                ),
            ],
            alignment=MainAxisAlignment.START,
        )

        # Inventory data table
        table = DataTable(
            columns=[
                DataColumn(Text("Product Name")),
                DataColumn(Text("Quantity")),
                DataColumn(Text("Price")),
                DataColumn(Text("Actions")),
            ],
            rows=[
                DataRow(
                    cells=[
                        DataCell(Text(i[1]), padding=Padding(left=20, right=20)),
                        DataCell(Text(i[2]), padding=Padding(left=20, right=20)),
                        DataCell(Text(i[3]), padding=Padding(left=20, right=20)),
                        DataCell(
                            Row(
                                controls=[
                                    IconButton(icons.UPDATE, on_click=lambda e, id=i[0]: self.update_item(id)),
                                    Container(width=10),
                                    IconButton(icons.DELETE, on_click=lambda e, id=i[0]: self.remove_item(id)),
                                ],
                                alignment=MainAxisAlignment.CENTER,
                            ),
                            padding=Padding(left=20, right=20),
                        ),
                    ]
                )
                for i in self.inventory
            ],
        )

        # Main layout combining menu bar and content area
        layout = Row(
            expand=True,
            controls=[
                menu_bar,
                Container(
                    bgcolor="#ffffff",
                    content=Column(
                        controls=[
                            Container(header, padding=10),
                            search_bar_row,
                            Container(table, padding=10, expand=True),
                        ],
                        expand=True,
                    ),
                    expand=True,
                ),
            ],
        )

        return layout
