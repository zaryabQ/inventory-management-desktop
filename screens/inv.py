import flet as ft
from flet import *
from db.inv_handler import InventoryHandler  # Import the InventoryHandler class from handler.py
from screens.Add_item import add_item_pop_up
from screens.utils import main_inv_upd  # Assuming you have a separate module for update logic
from screens.utils import main_remove  # Assuming you have a separate module for remove logic
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
            # Only refresh table if it's already created
            if hasattr(self, 'table_container') and self.table_container:
                self.refresh_table()
        except Exception as e:
            print(f"Error loading inventory: {e}")

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

    def add_item(self, e):
        """Trigger the add item pop-up."""
        add_item_pop_up(self.page, self.inventory_db ,self.load_inventory)
        self.load_inventory() 
        self.page.update()

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

        self.load_inventory() 
        self.page.update()

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
                                    "Are you sure you want to remove this item?",
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
        """Refresh the table to reflect the current inventory."""
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
        """Build the inventory table with modern styling."""
        columns = [
            DataColumn(Text("ID", color=IOS26Theme.TEXT_PRIMARY, weight=FontWeight.W_600)),
            DataColumn(Text("Name", color=IOS26Theme.TEXT_PRIMARY, weight=FontWeight.W_600)),
            DataColumn(Text("Quantity", color=IOS26Theme.TEXT_PRIMARY, weight=FontWeight.W_600)),
            DataColumn(Text("Cost", color=IOS26Theme.TEXT_PRIMARY, weight=FontWeight.W_600)),
            DataColumn(Text("Date", color=IOS26Theme.TEXT_PRIMARY, weight=FontWeight.W_600)),
            DataColumn(Text("Actions", color=IOS26Theme.TEXT_PRIMARY, weight=FontWeight.W_600)),
        ]
        
        rows = [
            DataRow(
                cells=[
                    DataCell(Text(str(item[0]), color=IOS26Theme.TEXT_PRIMARY)),
                    DataCell(Text(item[1], color=IOS26Theme.TEXT_PRIMARY)),
                    DataCell(Text(str(item[2]), color=IOS26Theme.TEXT_PRIMARY)),
                    DataCell(Text(f"Rs. {item[3]:,.2f}", color=IOS26Theme.TEXT_PRIMARY)),
                    DataCell(Text(item[4], color=IOS26Theme.TEXT_PRIMARY)),
                    DataCell(
                        Row(
                            controls=[
                                Container(
                                    content=modern_icon(
                                        name=Icons.EDIT,
                                        size=20,
                                        color=IOS26Theme.ACCENT_PRIMARY
                                    ),
                                    on_click=lambda e, item_id=item[0]: self.update_item(e, item_id),
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
                                    on_click=lambda e, item_id=item[0]: self.remove_item(e, item_id),
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
            for item in self.inventory
        ]
        
        return modern_data_table(columns, rows)

    def build(self):
        self.load_inventory()

        # Left side navigation with glass effect
        navigation_bar = zero_yellow_container(
            content=Column(
                controls=[
                    Container(height=20),
                    zero_yellow_text(
                        "Inventory",
                        size=24,
                        weight=FontWeight.BOLD,
                        color=ZeroYellowTheme.PURE_BLACK  # Black heading for visibility
                    ),
                    Container(height=30),
                    self.create_navigation_button("Dashboard", "/Home", Icons.DASHBOARD),
                    Container(height=12),
                    self.create_navigation_button("Inventory", "/Inventory", Icons.INVENTORY, True),
                    Container(height=12),
                    self.create_navigation_button("Billing", "/Billing", Icons.RECEIPT),
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
                                        "Inventory Management",
                                        size=36,
                                        color=IOS26Theme.TEXT_PRIMARY
                                    ),
                                    body_text(
                                        f"Manage your inventory items ({len(self.inventory)} items)",
                                        size=16,
                                        color=IOS26Theme.TEXT_SECONDARY
                                    )
                                ],
                                horizontal_alignment=CrossAxisAlignment.START
                            ),
                            Container(expand=True),
                            modern_icon(
                                name=Icons.INVENTORY,
                                size=32,
                                color=IOS26Theme.ACCENT_PRIMARY
                            )
                        ],
                        alignment=MainAxisAlignment.SPACE_BETWEEN
                    ),
                    Container(height=30),
                    
                    # Search and Add Item Bar
                    zero_yellow_container(
                        content=Row(
                            controls=[
                                zero_yellow_text_field(
                                    hint_text="Search items...",
                                    on_change=self.search_item,
                                    width=400,
                                    height=50
                                ),
                                Container(width=20),
                                zero_yellow_button(
                                    text="Add New Item",
                                    on_click=self.add_item,
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
                    
                    # Inventory Table
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
