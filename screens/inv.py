import flet as ft
from flet import *
from db.db_handler import InventoryDB  # Import the InventoryDB class from the inventory_db.py file
from screens.Add_item import add_item_pop_up

class InventoryScreen:
    def __init__(self, page: Page):
        self.page = page
        self.inventory = []
        #self.inventory_db = InventoryDB()  # Instantiate the InventoryDB class

    def load_inventory(self):
        try:
            self.inventory = self.inventory_db.get_all_inventory()
        except Exception as e:
            print(f"Error loading inventory: {e}")

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
        add_item_pop_up(self.page)
        # Logic to add item

    def search_item(self, e):
        print(f"Searching for {e.control.value}")
        # Logic to filter table based on search

    def update_item(self, e, item):
        print(f"Updating item {item}")
        self.page.bgcolor = "#383838"

    def remove_item(self, e, item_id):
        print(f"Removing item {item_id}")

        def cancel_remove(e):
            print("Entry removal cancelled")
            if self.page.views:
                self.page.views.pop()  # Remove the update view from the view stack

            self.page.update()  # Return to the Inventory screen without removing

        def confirm_remove(e):
            print(f"Entry {item_id} removed")
            # Logic to remove the item from the database or inventory list
            if self.page.views:
                self.page.views.pop()  # Remove the update view from the view stack

            self.page.update()  # Return to the Inventory screen after removing

        self.page.views.append(
            View(
                "/remove",
                bgcolor="#383838",
                controls=[
                    Column(
                        controls=[
                            Container(
                                content=Text(
                                    "Are you sure you want to remove the entry",
                                    color="red",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                alignment=ft.alignment.center,
                                padding=ft.padding.only(top=150)
                            ),
                            Row(
                                controls=[
                                    IconButton(
                                        icon=ft.icons.CLOSE,
                                        icon_color="white",
                                        bgcolor="teal",
                                        on_click=cancel_remove,
                                        width=70,
                                        height=70,
                                        icon_size=40
                                    ),
                                    IconButton(
                                        icon=ft.icons.CHECK,
                                        icon_color="white",
                                        bgcolor="teal",
                                        on_click=confirm_remove,
                                        width=70,
                                        height=70,
                                        icon_size=40
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=50,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=100,
                    )
                ]
            )
        )
        self.page.update()

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
                    height=50,
                ),
                ElevatedButton("Add Item", on_click=self.add_item, bgcolor="#2abfbf", color="#000000"),
            ],
            alignment=MainAxisAlignment.SPACE_BETWEEN,
        )

        # Inventory data table
        table = DataTable(
            columns=[
                DataColumn(Text("Name/ID")),
                DataColumn(Text("Category")),
                DataColumn(Text("Quantity")),
                DataColumn(Text("Unit Cost")),
                DataColumn(Text("Selling Price")),
                DataColumn(Text("Profit")),
                DataColumn(Text("Actions")),
            ],
            rows=[
                DataRow(
                    cells=[
                        DataCell(Text(item[1]), padding=Padding(left=20, right=20)),  # Name/ID
                        DataCell(Text(item[2]), padding=Padding(left=20, right=20)),  # Category
                        DataCell(Text(f"{item[3]}"), padding=Padding(left=20, right=20)),  # Quantity
                        DataCell(Text(f"${item[4]:.2f}"), padding=Padding(left=20, right=20)),  # Unit Cost
                        DataCell(Text(f"${item[5]:.2f}"), padding=Padding(left=20, right=20)),  # Selling Price
                        DataCell(Text(f"${item[6]:.2f}"), padding=Padding(left=20, right=20)),  # Profit
                        DataCell(
                            Row(
                                controls=[
                                    IconButton(icons.UPDATE, on_click=lambda e, item=item[0]: self.update_item(e, item)),
                                    Container(width=10),
                                    IconButton(icons.DELETE, on_click=lambda e, item_id=item[0]: self.remove_item(e, item_id)),
                                ],
                                alignment=MainAxisAlignment.CENTER,
                            ),
                            padding=Padding(left=20, right=20),
                        ),
                    ]
                )
                for item in self.inventory
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
