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

    def update_item(self, e, item):
        print(f"Updating item {item}")
        self.page.bgcolor = "#383838"

    # Create a function to handle the update button click
        def update_action(e):
            # Perform update logic here using the updated values from fields
            # print(f"Updating product: {name_field.value}, {quantity_field.value}, {price_field.value}")
            # Update the item in the database or the inventory list
            # (e.g., call to the database or update the data structure)
            # Call the on_update callback to return to the Inventory screen
            if self.page.views:
                self.page.views.pop()  # Remove the update view from the view stack

            self.page.update()


    # Define the update button
        update_button = ft.ElevatedButton(
            "Update", 
            bgcolor="#2abfbf", 
            color="#000000", 
            width=100, 
            on_click=update_action
        )
        name_field = Container(
            content=TextField(label="Enter the New Name", width=300, bgcolor=ft.colors.WHITE),
            alignment=ft.alignment.center,
            # padding=20
        )
        quantity_field = Container(
            content=TextField(label="Enter the New Name", width=300, bgcolor=ft.colors.WHITE),
            alignment=ft.alignment.center,
            # padding=20
        )
        price_field = Container(
            content=TextField(label="Enter the New Name", width=300, bgcolor=ft.colors.WHITE),
            alignment=ft.alignment.center,
            # padding=20
        )
        # Create a container for the button to center it
        button_container = Container(
            content=update_button,
            alignment=ft.alignment.center,
            # padding=20
        )
        
        # Create a container for the input fields and the centered button
        input_container = ft.Container(
            content=ft.Column(
                controls=[
                    name_field,
                    quantity_field,
                    price_field,
                    button_container  # Place the button container inside the column
                ],
                alignment=MainAxisAlignment.CENTER,
                spacing=30
            ),
            padding=20,
            border_radius=20,
            bgcolor="#2b3037",  # Set the background color to #2b3037
            # alignment=ft.alignment.center,
            height=self.page.height * 0.7,   # Increase the height of the container
            width=self.page.width * 0.5,   # Set a fixed width to ensure centering
            margin=ft.margin.only(top=30)
        )
        

        self.page.views.append(
            View(
                "/update",
                controls=[
                    ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Container(
                                        content=ft.Text(
                                            "Update Product",
                                            size=30,
                                            weight=ft.FontWeight.BOLD,
                                            color='#26A69A',
                                            font_family="Arial",  # Set the font family to Arial (or any other available font)
                                            italic=True  # Make the text italic
                                        ),
                                        padding=ft.padding.only(top=50),
                                        alignment=ft.alignment.center,
                                        width=self.page.width * 0.5 
                                        # Adjust padding to move the heading down
                                    ),
                                    input_container
                                ],
                                alignment = MainAxisAlignment.CENTER,
                                horizontal_alignment=alignment.center
                            
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,  # Aligns the Row's content to the center
                    )
                ]
            )
        )
        #main_inv_upd(self.page, item, lambda: self.page.go("/Inventory"))
        # main_inv_upd(self.page)
        self.page.update()

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
        #main_remove(self.page, item_id, lambda: self.page.go("/Inventory"))
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
                DataColumn(Text("Product Name", color="#000000")),
                DataColumn(Text("Quantity", color="#000000")),
                DataColumn(Text("Price", color="#000000")),
                DataColumn(IconButton(
                                icon=ft.icons.CHANGE_CIRCLE_OUTLINED,
                                icon_color="#000000",
                                tooltip="Update",
                                on_click=lambda e, item=5: self.update_item(e, item)
                            )
                ),
                DataColumn(IconButton(
                                icon=ft.icons.DELETE_OUTLINE_ROUNDED,
                                icon_color="#000000",
                                tooltip="Delete",
                                on_click=lambda e, id=0: self.remove_item(e, id)
                            )
                ),
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
                                    IconButton(
                                        icon=ft.icons.CHANGE_CIRCLE_OUTLINED,
                                        icon_color="#000000",
                                        tooltip="Update",
                                        on_click=lambda e, item=i: self.update_item(e, item)
                                    ),
                                    Container(width=10),
                                    IconButton(
                                        icon=ft.icons.DELETE_OUTLINE_ROUNDED,
                                        icon_color="#000000",
                                        tooltip="Remove",
                                        on_click=lambda e, id=i[0]: self.remove_item(e, id)
                                    ),
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
