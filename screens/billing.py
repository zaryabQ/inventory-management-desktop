import flet as ft
from flet import *
from db.billing_handler import BillingHandler  # Import the BillingDB class
from screens.Bill_Gene import bill_gen
from screens.update_bill import bill_updt
from screens.utils import main_remove  # Assuming you have a remove logic in utils

class BillingScreen:
    def __init__(self, page: Page):
        self.page = page
        self.bills = []
        self.billing_db = BillingHandler()  # Instantiate the BillingDB class
        self.table_container = None  # Initialize a reference for the table container

        # Set the custom scrollbar theme
        self.page.theme = ft.Theme(
            scrollbar_theme=ft.ScrollbarTheme(
                track_color={
                    ft.MaterialState.HOVERED: "#D3D3D3",
                    ft.MaterialState.DEFAULT: "#FFFFFF",
                },
                track_visibility=True,
                track_border_color="#D3D3D3",
                thumb_visibility=True,
                thumb_color={
                    ft.MaterialState.HOVERED: "#A9A9A9",
                    ft.MaterialState.DEFAULT: "#696969",
                },
                thickness=10,
                radius=10,
                main_axis_margin=50,
                cross_axis_margin=10,
            )
        )

    def load_bills(self):
        """Load all bills from the database."""
        try:
            self.bills = self.billing_db.load_billing()
            if self.bills is None:
                self.bills = []  # Safeguard against None
            self.refresh_table()  # Refresh the table after loading
        except Exception as e:
            print(f"Error loading bills: {e}")


    def search_bills(self, e):
        """Search for bills in the database."""
        keyword = e.control.value.strip()
        if keyword:
            self.bills = self.billing_db.search_bills(keyword)
        else:
            self.bills = self.billing_db.load_billing()  # Load all bills if search is empty
        self.refresh_table()

    def handle_add_bill(self, e):
        """Handle the 'Add Bill' button click."""
        bill_gen(self.page)
        self.load_bills()
        self.page.update()

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

    def update_bill(self, e, bill_id):
        """Placeholder for bill update functionality."""
        bill_updt(self.page , bill_id)
        self.load_bills()
        self.page.update()
        print(f"Update Bill with ID {bill_id}")
        # You can later add logic to open the update screen

    def remove_bill(self, e, bill_id):
        """Remove a bill."""
        def cancel_remove(e):
            if self.page.views:
                self.page.views.pop()  # Remove the confirmation view
            self.page.update()  # Return to the Billing screen without removing

        def confirm_remove(e):
            def show_snackbar(message):
                """Show a snackbar with the given message."""
                # Assuming `page` is your Flet page object
                
                self.page.snack_bar = SnackBar(Text(f"{message}"), open=True)
                self.page.update()

            # Call remove_bill with show_snackbar function to handle alerts
            self.billing_db.remove_bill(bill_id, show_snackbar)
             # Assuming this refreshes the list of bills
            self.page.views.pop()
            self.page.update()
 # Refresh the billing table after removal

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
        """Refresh the table to reflect the current bills."""
        if self.table_container:
            self.table_container.content.controls.clear()  # Clear current controls
            self.table_container.content.controls.append(self.build_table())  # Rebuild the table
            self.page.update()  # Update the page to reflect changes
        else:
            print("Error: Table container reference not found.")


    def build_table(self):
        """Build the billing table."""
        return DataTable(
            expand=True,
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
                        DataCell(Container(Text(bill[1]), padding=10)),  # Name/ID
                        DataCell(Container(Text(bill[2]), padding=10)),  # Billing Date
                        DataCell(Container(Text(bill[3]), padding=10)),  # Items
                        DataCell(Container(Text(f"Rs: {bill[4]:.2f}"), padding=10)),  # Total Cost
                        DataCell(Container(Text(f"Rs: {bill[5]:.2f}"), padding=10)),  # Profit
                        DataCell(Container(Text(bill[6]), padding=10)),  # Status
                        DataCell(
                            Row(
                                controls=[
                                    IconButton(icons.UPDATE, on_click=lambda e, id=bill[0]: self.update_bill(e, id)),
                                    IconButton(icons.DELETE, on_click=lambda e, id=bill[0]: self.remove_bill(e, id)),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                            ),
                        ),  # Actions
                    ]
                )
                for bill in self.bills
            ],
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

        # Search bar with Add Bill button
        search_bar_row = Row(
            controls=[
                Container(
                    content=TextField(
                        hint_text="Search Bill",
                        on_change=self.search_bills,
                        height=50,
                        bgcolor="#ffffff",
                        border_radius=10,
                    ),
                    width=300,
                    height=50,
                ),
                ElevatedButton("Add Bill", on_click=self.handle_add_bill, bgcolor="#2abfbf", color="#000000"),
            ],
            alignment=MainAxisAlignment.SPACE_BETWEEN,
        )

        # Billing data table with scroll support
        table = self.build_table()
        scrollable_table = Container(
            content=ListView(controls=[table], expand=True),
            padding=10,
            expand=True
        )
        self.table_container = scrollable_table  # Store reference here

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
