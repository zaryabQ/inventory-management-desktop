import flet as ft
from flet import *
from db.inv_handler import InventoryHandler  # Import the InventoryHandler class from handler.py
from screens.Add_item import add_item_pop_up
from screens.utils import main_inv_upd  # Assuming you have a separate module for update logic
from screens.utils import main_remove  # Assuming you have a separate module for remove logic

class InventoryScreen:
    def __init__(self, page: Page):
        self.page = page
        self.inventory = []
        self.inventory_db = InventoryHandler()  # Instantiate the InventoryHandler class
        self.table_container = None  # Initialize a reference for the table container

    def load_inventory(self):
        """Load inventory data using the handler."""
        try:
            self.inventory = self.inventory_db.load_inventory()
            if self.inventory is None:
                self.inventory = []  # Safeguard against None
            self.refresh_table()
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
        """Trigger the add item pop-up."""
        add_item_pop_up(self.page, self.inventory_db)

    def search_item(self, e):
        """Search for items in the inventory."""
        keyword = e.control.value.strip()
        if keyword:
            self.inventory = self.inventory_db.search_items(keyword)
        else:
            self.inventory = self.inventory_db.load_inventory()  # Load all items if search is empty
        self.refresh_table()

    def update_item(self, e, item_id):
        """Update an item in the inventory."""
        item_data = next((item for item in self.inventory if item[0] == item_id), None)
        if item_data:
            def save_update(updated_data):
                try:
                    self.inventory_db.update_item(item_id, updated_data)
                    self.load_inventory()
                except Exception as ex:
                    print(f"Error updating item: {ex}")
            main_inv_upd(self.page, item_data, save_update)


    def remove_item(self, e, item_id):
        """Remove an item from the inventory."""
        def cancel_remove(e):
            if self.page.views:
                self.page.views.pop()  # Remove the confirmation view
            self.page.update()  # Return to the Inventory screen without removing

        def confirm_remove(e):
            self.inventory_db.remove_item(item_id)
            self.load_inventory() 
            self.page.views.pop()
            self.page.update() # Refresh the inventory after removal

        self.page.views.append(
            View(
                "/remove",
                bgcolor="#383838",
                controls=[
                    Column(
                        controls=[
                            Container(
                                content=Text(
                                    "Are you sure you want to remove the entry?",
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

    def refresh_table(self):
        """Refresh the table to reflect the current inventory."""
        if self.table_container:
            self.table_container.content = self.build_table()
            self.page.update()
        else:
            print("Error: Table container reference not found.")

    def build_table(self):
        """Build the inventory table."""
        return DataTable(
            columns=[
                DataColumn(Text("ID")),
                DataColumn(Text("Name")),
                DataColumn(Text("Quantity")),
                DataColumn(Text("Cost")),
                DataColumn(Text("Date")),
                DataColumn(Text("Edit")),
            ],
            rows=[
                DataRow(
                    cells=[
                        DataCell(Text(str(item[0]))),  # ID
                        DataCell(Text(item[1])),      # Name
                        DataCell(Text(str(item[2]))), # Quantity
                        DataCell(Text(str(item[3]))), # Cost
                        DataCell(Text(item[4])),
                        DataCell(
                            Container(
                                Row(
                                    controls=[
                                        IconButton(ft.icons.UPDATE, on_click=lambda e, item_id=item[0]: self.update_item(e, item_id)),
                                        Container(width=10),
                                        IconButton(ft.icons.DELETE, on_click=lambda e, item_id=item[0]: self.remove_item(e, item_id)),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                                padding=Padding(left=10, right=10, top=0, bottom=0)
                            )
                        ),
                    ]
                )
                for item in self.inventory
            ],
        )

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
        table = self.build_table()
        self.table_container = Container(table, padding=10, expand=True)  # Store reference here

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
                            self.table_container,  # Use the stored reference
                        ],
                        expand=True,
                    ),
                    expand=True,
                ),
            ],
        )

        return layout
