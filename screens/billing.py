import flet as ft
from flet import *
import sqlite3

class BillingScreen:
    def __init__(self, page: Page):
        self.page = page
        self.bills = []

    def load_bills(self):
        try:
            con = sqlite3.connect("db/sql.db")
            cur = con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS Bills (id INTEGER PRIMARY KEY, name_id TEXT, billing_date TEXT, items TEXT, total_cost REAL, profit REAL, status TEXT)")
            res = cur.execute("SELECT * FROM Bills")
            self.bills = [i for i in res.fetchall()]
        except sqlite3.OperationalError as e:
            print(f"Database error: {e}")
            print("Ensure that the 'Bills' table exists in the database.")
        except Exception as e:
            print(f"General error: {e}")

    def handle_add_bill(self, e):
        print("Add Bill button clicked")
        # Logic to add a new bill (you can implement the SQLite logic here)

    def handle_delete_or_update(self, id):
        print(f"Deleting or updating bill with ID {id}")
        # Logic to delete or update a bill (you can implement the SQLite logic here)

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

    def build(self):
        self.load_bills()

        # Left side menu bar
        menu_bar = Container(
            width=250,
            bgcolor="#383838",
            padding=10,
            content=Column(
                expand=True,
                controls=[
                    Text("Billing", color="#00D0FF", size=20, weight="bold"),
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

        # Container above the DataTable with "Invoice" and "Add Bill" button
        invoice_header = Container(
            padding=10,
            content=Row(
                controls=[
                    Text("Invoice", size=30, weight="bold", color=colors.BLACK),
                    ElevatedButton("Add Bill", on_click=self.handle_add_bill, bgcolor="#2abfbf", color="#000000"),
                ],
                alignment=MainAxisAlignment.SPACE_BETWEEN,
            ),
        )

        # Billing data table
        table = DataTable(
            columns=[
                DataColumn(Text("Name/ID")),
                DataColumn(Text("Billing Date")),
                DataColumn(Text("Items")),
                DataColumn(Text("Total Cost")),
                DataColumn(Text("Profit")),
                DataColumn(Text("Status")),
                DataColumn(Text("Actions")),
            ],
            rows=[
                DataRow(
                    cells=[
                        DataCell(Text(bill[1]), padding=Padding(left=20, right=20)),  # Name/ID
                        DataCell(Text(bill[2]), padding=Padding(left=20, right=20)),  # Billing Date
                        DataCell(Text(bill[3]), padding=Padding(left=20, right=20)),  # Items
                        DataCell(Text(f"${bill[4]:.2f}"), padding=Padding(left=20, right=20)),  # Total Cost
                        DataCell(Text(f"${bill[5]:.2f}"), padding=Padding(left=20, right=20)),  # Profit
                        DataCell(Text(bill[6]), padding=Padding(left=20, right=20)),  # Status
                        DataCell(
                            Row(
                                controls=[
                                    IconButton(icons.UPDATE, on_click=lambda e, id=bill[0]: self.handle_delete_or_update(id)),
                                    Container(width=10),
                                    IconButton(icons.DELETE, on_click=lambda e, id=bill[0]: self.handle_delete_or_update(id)),
                                ],
                                alignment=MainAxisAlignment.CENTER,
                            ),
                            padding=Padding(left=20, right=20),
                        ),
                    ]
                )
                for bill in self.bills
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
                            invoice_header,
                            Container(table, padding=10, expand=True),
                        ],
                        expand=True,
                    ),
                    expand=True,
                ),
            ],
        )

        return layout
