from flet import *
import sqlite3

class Inventory(Control):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.inventory = []  # Initialize with an empty list
        self.load_inventory()

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

    def build(self):
        # Left side menu bar
        menu_bar = Container(
            width=200,
            bgcolor="#383838",
            padding=10,
            content=Column(
                expand=True,
                controls=[
                    Text("Inventory", color="#00D0FF", size=20, weight="bold"),
                    Container(height=20),
                    self.create_menu_button("Dashboard", "/Dashboard"),
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
            bgcolor="#383838",  # Set the background color of the header container
            padding=20,  # Optional: Add some padding around the content
            content=Row(
                controls=[
                    Container(
                        content=Text("Welcome Back", size=40, color="#26A69A"),
                    ),
                ],
                alignment=MainAxisAlignment.CENTER,  # Center the content horizontally
                vertical_alignment=CrossAxisAlignment.CENTER,  # Align content vertically centered
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
                        border_radius=10,  # Rounded corners
                    ),
                    width=300,  # Set a fixed width for the search bar
                    padding=10,
                ),
                Container(width=550),  # Space between search bar and button
                Container(
                    content=ElevatedButton(
                        text="Add Item",
                        on_click=self.add_item,
                        bgcolor="#E0E0E0",
                        color="#000000",
                    ),
                    border_radius=20,  # Rounded corners
                    padding=0,
                ),
            ],
            alignment=MainAxisAlignment.START,  # Align items to the start of the row
        )

        # Inventory data table
        table = DataTable(
            columns=[
                DataColumn(Text("Product Name")),
                DataColumn(Text("Quantity")),
                DataColumn(Text("Price")),
                DataColumn(Text("Update")),
                DataColumn(Text("Remove")),
            ],
            rows=[
                DataRow(
                    cells=[
                        DataCell(Text(i[1])),  # i[1] for product_name
                        DataCell(Text(i[2])),  # i[2] for quantity
                        DataCell(Text(i[3])),  # i[3] for price
                        DataCell(IconButton(icons.UPDATE, on_click=lambda e, id=i[0]: self.update_item(id))),
                        DataCell(IconButton(icons.DELETE, on_click=lambda e, id=i[0]: self.remove_item(id))),
                    ]
                )
                for i in self.inventory
            ],
        )

        # Layout
        return Row(
            controls=[
                menu_bar,  # Ensure menu_bar is included in the Row
                Container(
                    content=Column(
                        controls=[
                            Container(header, padding=10),
                            search_bar_row,  # Added search bar and button row
                            Container(table, padding=10, expand=True),
                        ],
                        expand=True,
                    ),
                    expand=True,  # Ensure this container expands to take available space
                ),
            ],
            expand=True,
        )

    def create_menu_button(self, text, route):
        """ Helper function to create menu buttons """
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

def main(page: Page):
    inv = Inventory(page)
    page.add(inv.build())

app(target=main)
