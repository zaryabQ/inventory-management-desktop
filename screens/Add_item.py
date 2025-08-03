import flet as ft
from flet import *
from db.inv_handler import InventoryHandler
from screens.theme import (
    ZeroYellowTheme, 
    zero_yellow_container, 
    zero_yellow_button, 
    zero_yellow_text_field, 
    zero_yellow_heading, 
    zero_yellow_text,
    zero_yellow_icon,
    zero_yellow_snackbar,
    # Legacy compatibility
    IOS26Theme,
    secondary_button
)

def add_item_pop_up(page, inventory_db, load_inv_callback):

    def show_snackbar(message):
        """Helper function to show a snackbar with a message."""
        snackbar = zero_yellow_snackbar(message)
        page.snack_bar = snackbar
        page.snack_bar.open = True
        page.update()

    def add_item(e):
        # Close the pop-up without saving
        page.views.pop()
        page.go('/Inventory')
        page.update()

    def save_item(e):
        name = item_name.value.strip()
        quantity = item_quantity.value.strip()
        cost = buy_price.value.strip()

        # Validate fields
        if not name:
            show_snackbar("Item Name cannot be empty.")
            return
        if not quantity:
            show_snackbar("Quantity cannot be empty.")
            return
        if not cost:
            show_snackbar("Cost cannot be empty.")
            return

        # Validate data types
        try:
            quantity = int(quantity)
        except ValueError:
            show_snackbar("Quantity must be a numeric value.")
            return

        try:
            cost = float(cost)
        except ValueError:
            show_snackbar("Cost must be a numeric value.")
            return

        try:
            # Add item to the inventory
            inventory_db.add_item(name, quantity, cost)
            # Clear the fields
            item_name.value = ""
            item_quantity.value = ""
            buy_price.value = ""
            # Close the pop-up
            page.views.pop()
            load_inv_callback()
            page.update()
        except ValueError as ve:
            show_snackbar(str(ve))

    # Page settings
    page.title = "Inventory Management"
    page.bgcolor = ZeroYellowTheme.BG_PRIMARY

    # Heading
    heading = zero_yellow_heading(
        "Add Items to Inventory"
    )

    item_name = zero_yellow_text_field(
        hint_text="Enter Item Name",
        width=300,
        height=50
    )

    item_quantity = zero_yellow_text_field(
        hint_text="Enter the Quantity",
        width=300,
        height=50
    )

    buy_price = zero_yellow_text_field(
        hint_text="Enter the Price",
        width=300,
        height=50
    )

    # Creating the add button
    add_button = zero_yellow_button(
        text="Add Item",
        on_click=save_item,
        width=150,
        height=45
    )

    back_button = zero_yellow_button(
        text="Back",
        on_click=add_item,
        width=150,
        height=45,
        primary=False
    )

    # Create the column for the input fields and button
    content = zero_yellow_container(
        content=Column(
            controls=[
                heading,  # Heading at the top
                Container(height=30),
                item_name,
                Container(height=10),
                item_quantity,
                Container(height=10),
                buy_price,
                Container(height=30),
                Row(
                    controls=[
                        add_button,
                        Container(width=20),
                        back_button
                    ],
                    alignment=MainAxisAlignment.CENTER
                )
            ],
            horizontal_alignment=CrossAxisAlignment.CENTER,
            spacing=10
        ),
        width=400,
        height=500,
        padding=40,
        margin=20
    )

    # Add the main container to the page
    page.views.append(
        View(
            "/add_item",
            bgcolor=ZeroYellowTheme.BG_PRIMARY,
            controls=[
                Container(
                    content=content,
                    alignment=alignment.center,
                    expand=True
                )
            ]
        )
    )
    page.update()
