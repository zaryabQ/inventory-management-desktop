from flet import *
import sqlite3

def build_billing(page: Page):
    FW = colors.CYAN  # Define FW color manually here

    # def close_add_dlg(e):
    #     add_dlg.open = False
    #     page.update()

    def handle_add_bill(e):
        # Logic to add bill (You can implement SQLite logic here)
        print("Add Bill button clicked")

    def handle_delete_or_update(id):
        print(f"Deleting or updating bill with ID {id}")
        # Logic to delete or update a bill row (You can implement SQLite logic here)

    # Load bills (similar to loading inventory in the provided code)
    bills = []  # This will hold the billing data

    def load_bills():
        nonlocal bills
        try:
            con = sqlite3.connect("db/sql.db")
            cur = con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS Bills (id INTEGER PRIMARY KEY, name_id TEXT, billing_date TEXT, items TEXT, total_cost REAL, profit REAL, status TEXT)")
            res = cur.execute("SELECT * FROM Bills")
            bills = [i for i in res.fetchall()]
        except sqlite3.OperationalError as e:
            print(f"Database error: {e}")
            print("Ensure that the 'Bills' table exists in the database.")
        except Exception as e:
            print(f"General error: {e}")

    load_bills()

    def create_menu_button(text, route):
        """Helper function to create menu buttons."""
        return Container(
            width=180,
            height=50,
            margin=margin.only(bottom=10),
            content=ElevatedButton(
                text=text,
                on_click=lambda _: page.go(route),
                bgcolor="#2C2C2C",
                color="white",
                expand=True,
            ),
        )

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
                create_menu_button("Dashboard", "/Dashboard"),
                Container(height=10),
                create_menu_button("Inventory", "/Inventory"),
                Container(height=10),
                create_menu_button("Billing", "/Billing"),
                Container(height=10),
                create_menu_button("Settings", "/Settings"),
            ],
        ),
    )

    # Header with welcome message
    header = Container(
        bgcolor="#2b3037",  # Set the background color of the header container
        padding=40,  # Optional: Add some padding around the content
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

    # Container above the DataTable with "Invoice" and "Add Bill" button
    invoice_header = Container(
        padding=10,
        content=Row(
            controls=[
                Text("Invoice", size=30, weight="bold", color=colors.BLACK),
                ElevatedButton("Add Bill", on_click=handle_add_bill, bgcolor="#2abfbf",color="#000000"),
            ],
            alignment=MainAxisAlignment.SPACE_BETWEEN,  # Align text and button horizontally
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
            DataColumn(Text("Actions")),  # Use "Actions" as the header
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
                                IconButton(icons.UPDATE, on_click=lambda e, id=bill[0]: handle_delete_or_update(id)),
                                Container(width=10),  # Add space between icons
                                IconButton(icons.DELETE, on_click=lambda e, id=bill[0]: handle_delete_or_update(id)),
                            ],
                            alignment=MainAxisAlignment.CENTER,  # Center the icons vertically
                        ),
                        padding=Padding(left=20, right=20),  # Add padding for spacing
                    ),
                ]
            )
            for bill in bills
        ],
    )

    # Main layout combining menu bar and content area
    layout = Row(
        expand=True,
        controls=[
            menu_bar,  # Ensure menu_bar is included in the Row
            Container(
                bgcolor="#ffffff",  # Set the background color of the container to white
                content=Column(
                    controls=[
                        Container(header, padding=10),
                        invoice_header,  # Add the invoice header here
                        Container(table, padding=10, expand=True),
                    ],
                    expand=True,
                ),
                expand=True,  # Ensure this container expands to take available space
            ),
        ],
    )

    return layout

def main(page: Page):
    page.title = "Billing"
    page.bgcolor = "#2C2C2C"
    page.window.width = 1024  # Adjust as needed
    page.window.height = 768  # Adjust as needed
    page.window.resizable = True  # Allow window resizing

    billing_layout = build_billing(page)
    page.add(billing_layout)

app(target=main)
