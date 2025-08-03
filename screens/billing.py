import flet as ft
from flet import *
from db.billing_handler import BillingHandler  # Import the BillingDB class
from screens.Bill_Gene import bill_gen
from screens.update_bill import bill_updt
from screens.utils import main_remove  # Assuming you have a remove logic in utils
from screens.theme import (
    ZeroYellowTheme, 
    zero_yellow_container, 
    zero_yellow_text, 
    zero_yellow_button,
    zero_yellow_text_field,
    zero_yellow_icon,
    zero_yellow_data_table,
    # Legacy compatibility
    IOS26Theme,
    glass_container,
    modern_card,
    heading_text,
    body_text,
    caption_text,
    primary_button,
    secondary_button,
    modern_text_field,
    modern_data_table,
    modern_icon
)

class BillingScreen:
    def __init__(self, page: Page):
        self.page = page
        self.bills = []
        self.billing_db = BillingHandler()  # Instantiate the BillingDB class
        self.table_container = None  # Initialize a reference for the table container

    def load_bills(self):
        """Load all bills from the database."""
        try:
            self.bills = self.billing_db.load_billing()
            if self.bills is None:
                self.bills = []  # Safeguard against None
            # Only refresh table if it's already created
            if hasattr(self, 'table_container') and self.table_container:
                self.refresh_table()
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
        bill_gen(self.page,self.load_bills)
        self.load_bills()
        self.page.update()

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

    def update_bill(self, e, bill_id):
        """Placeholder for bill update functionality."""
        bill_updt(self.page , bill_id, self.load_bills)
        self.load_bills()
        self.page.update()
        print(f"Update Bill with ID {bill_id}")

    def remove_bill(self, e, bill_id):
        """Remove a bill."""
        def cancel_remove(e):
            if self.page.views:
                self.page.views.pop()  # Remove the confirmation view
            self.page.update()  # Return to the Billing screen without removing

        def confirm_remove(e):
            def show_snackbar(message):
                """Show a snackbar with the given message."""
                self.page.snack_bar = SnackBar(
                    content=Text(f"{message}", color=IOS26Theme.TEXT_PRIMARY),
                    bgcolor=IOS26Theme.ACCENT_SECONDARY,
                    open=True
                )
                self.page.update()

            # Call remove_bill with show_snackbar function to handle alerts
            self.billing_db.remove_bill(bill_id, show_snackbar)
            self.page.views.pop()
            self.load_bills()
            self.page.update()

        self.page.views.append(
            View(
                "/remove",
                bgcolor=ZeroYellowTheme.BG_PRIMARY,
                controls=[
                    zero_yellow_container(
                        content=Column(
                            controls=[
                                modern_icon(
                                    name=Icons.WARNING,
                                    size=64,
                                    color=IOS26Theme.ACCENT_QUATERNARY
                                ),
                                Container(height=20),
                                heading_text(
                                    "Confirm Deletion",
                                    size=24,
                                    color=IOS26Theme.TEXT_PRIMARY
                                ),
                                body_text(
                                    "Are you sure you want to remove this bill?",
                                    size=16,
                                    color=IOS26Theme.TEXT_SECONDARY
                                ),
                                Container(height=30),
                                Row(
                                    controls=[
                                        secondary_button(
                                            text="Cancel",
                                            on_click=cancel_remove,
                                            width=120,
                                            height=45
                                        ),
                                        Container(width=20),
                                        primary_button(
                                            text="Delete",
                                            on_click=confirm_remove,
                                            width=120,
                                            height=45,
                                            bgcolor=IOS26Theme.ACCENT_QUATERNARY
                                        ),
                                    ],
                                    alignment=MainAxisAlignment.CENTER,
                                ),
                            ],
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                            alignment=MainAxisAlignment.CENTER,
                        ),
                        width=400,
                        height=300,
                        padding=30
                    )
                ]
            )
        )
        self.page.update()

    def refresh_table(self):
        """Refresh the table to reflect the current bills."""
        if hasattr(self, 'table_container') and self.table_container:
            # Update the table content in the scrollable column
            if hasattr(self.table_container, 'content') and hasattr(self.table_container.content, 'content'):
                if hasattr(self.table_container.content.content, 'controls'):
                    self.table_container.content.content.controls = [self.build_table()]
                    self.page.update()
        else:
            # Table container not ready yet, this is normal during initialization
            pass

    def build_table(self):
        """Build the billing table with modern styling."""
        columns = [
            DataColumn(Text("Name/ID", color=IOS26Theme.TEXT_PRIMARY, weight=FontWeight.W_600)),
            DataColumn(Text("Billing Date", color=IOS26Theme.TEXT_PRIMARY, weight=FontWeight.W_600)),
            DataColumn(Text("Items", color=IOS26Theme.TEXT_PRIMARY, weight=FontWeight.W_600)),
            DataColumn(Text("Total Cost", color=IOS26Theme.TEXT_PRIMARY, weight=FontWeight.W_600)),
            DataColumn(Text("Profit", color=IOS26Theme.TEXT_PRIMARY, weight=FontWeight.W_600)),
            DataColumn(Text("Paid", color=IOS26Theme.TEXT_PRIMARY, weight=FontWeight.W_600)),
            DataColumn(Text("Remaining", color=IOS26Theme.TEXT_PRIMARY, weight=FontWeight.W_600)),
            DataColumn(Text("Status", color=IOS26Theme.TEXT_PRIMARY, weight=FontWeight.W_600)),
            DataColumn(Text("Actions", color=IOS26Theme.TEXT_PRIMARY, weight=FontWeight.W_600)),
        ]
        
        rows = [
            DataRow(
                cells=[
                    DataCell(Text(bill[1], color=IOS26Theme.TEXT_PRIMARY)),
                    DataCell(Text(bill[2], color=IOS26Theme.TEXT_PRIMARY)),
                    DataCell(Text(bill[3], color=IOS26Theme.TEXT_PRIMARY)),
                    DataCell(Text(f"Rs. {bill[4]:,.2f}", color=IOS26Theme.TEXT_PRIMARY)),
                    DataCell(Text(f"Rs. {bill[5]:,.2f}", color=IOS26Theme.TEXT_PRIMARY)),
                    DataCell(Text(f"Rs. {bill[7]:,.2f}", color=IOS26Theme.TEXT_PRIMARY)),
                    DataCell(Text(f"Rs. {bill[8]:,.2f}", color=IOS26Theme.TEXT_PRIMARY)),
                    DataCell(
                        Container(
                            content=Text(
                                bill[6],
                                color=IOS26Theme.TEXT_PRIMARY,
                                size=12,
                                weight=FontWeight.W_500
                            ),
                            bgcolor=IOS26Theme.ACCENT_SECONDARY + "20" if bill[6].lower() == "paid" else IOS26Theme.ACCENT_QUATERNARY + "20",
                            padding=8,
                            border_radius=8
                        )
                    ),
                    DataCell(
                        Row(
                            controls=[
                                Container(
                                    content=modern_icon(
                                        name=Icons.EDIT,
                                        size=20,
                                        color=IOS26Theme.ACCENT_PRIMARY
                                    ),
                                    on_click=lambda e, id=bill[0]: self.update_bill(e, id),
                                    padding=8,
                                    border_radius=6,
                                    bgcolor=IOS26Theme.ACCENT_PRIMARY + "20"
                                ),
                                Container(width=8),
                                Container(
                                    content=modern_icon(
                                        name=Icons.DELETE,
                                        size=20,
                                        color=IOS26Theme.ACCENT_QUATERNARY
                                    ),
                                    on_click=lambda e, id=bill[0]: self.remove_bill(e, id),
                                    padding=8,
                                    border_radius=6,
                                    bgcolor=IOS26Theme.ACCENT_QUATERNARY + "20"
                                ),
                            ],
                            alignment=MainAxisAlignment.START,
                            spacing=8,
                        )
                    ),
                ]
            )
            for bill in self.bills
        ]
        
        return modern_data_table(columns, rows)

    def build(self):
        self.load_bills()

        # Left side navigation with glass effect
        navigation_bar = zero_yellow_container(
            content=Column(
                controls=[
                    Container(height=20),
                    zero_yellow_text(
                        "Billing",
                        size=24,
                        weight=FontWeight.BOLD,
                        color=ZeroYellowTheme.PURE_BLACK  # Black heading for visibility
                    ),
                    Container(height=30),
                    self.create_navigation_button("Dashboard", "/Home", Icons.DASHBOARD),
                    Container(height=12),
                    self.create_navigation_button("Inventory", "/Inventory", Icons.INVENTORY),
                    Container(height=12),
                    self.create_navigation_button("Billing", "/Billing", Icons.RECEIPT, True),
                    Container(height=12),
                    self.create_navigation_button("Settings", "/Settings", Icons.SETTINGS),
                    Container(height=20),
                    # User info section
                    zero_yellow_container(
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

        # Create table container first with scrolling
        table_container = zero_yellow_container(
            content=Container(
                content=Column(
                    controls=[self.build_table()],
                    scroll=ScrollMode.AUTO,  # Enable vertical scrolling
                    auto_scroll=True
                ),
                expand=True
            ),
            padding=20,
            margin=0,
            expand=True
        )
        
        # Store reference to table container
        self.table_container = table_container
        
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
                                        "Billing Management",
                                        size=36,
                                        color=IOS26Theme.TEXT_PRIMARY
                                    ),
                                    body_text(
                                        f"Manage your billing records ({len(self.bills)} bills)",
                                        size=16,
                                        color=IOS26Theme.TEXT_SECONDARY
                                    )
                                ],
                                horizontal_alignment=CrossAxisAlignment.START
                            ),
                            Container(expand=True),
                            modern_icon(
                                name=Icons.RECEIPT,
                                size=32,
                                color=IOS26Theme.ACCENT_PRIMARY
                            )
                        ],
                        alignment=MainAxisAlignment.SPACE_BETWEEN
                    ),
                    Container(height=30),
                    
                    # Search and Add Bill Bar
                    zero_yellow_container(
                        content=Row(
                            controls=[
                                zero_yellow_text_field(
                                    hint_text="Search bills...",
                                    on_change=self.search_bills,
                                    width=400,
                                    height=50
                                ),
                                Container(width=20),
                                zero_yellow_button(
                                    text="Add New Bill",
                                    on_click=self.handle_add_bill,
                                    width=150,
                                    height=50,
                                    primary=True
                                )
                            ],
                            alignment=MainAxisAlignment.SPACE_BETWEEN
                        ),
                        padding=20,
                        margin=0
                    ),
                    Container(height=20),
                    
                    # Billing Table
                    table_container
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
