import flet as ft
from flet import *
from db.inv_handler import InventoryHandler

def add_item_pop_up(page, inventory_db, load_inv_callback):

    def show_snackbar(message):
        """Helper function to show a snackbar with a message."""
        snackbar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=ft.colors.RED_800,
            duration=2000  # Duration in milliseconds
        )
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
    page.bgcolor = "#383838"  # Dark background

    # Heading
    heading = ft.Text(
        "Add Items to Inventory",
        size=30,
        weight=ft.FontWeight.BOLD,
        color='#26A69A',
        font_family="Arial",  # Set the font family to Arial (or any other available font)
        italic=True
    )

    item_name = ft.TextField(
        hint_text="Enter Item Name",
        bgcolor="white",
        color="black",
        border_radius=10,
        text_align="center",
        width=300
    )

    item_quantity = ft.TextField(
        hint_text="Enter the Quantity",
        bgcolor="white",
        color="black",
        border_radius=10,
        text_align="center",
        width=300
    )

    buy_price = ft.TextField(
        hint_text="Enter the Price",
        bgcolor="white",
        color="black",
        border_radius=10,
        text_align="center",
        width=300
    )

    # Creating the add button
    add_button = ft.ElevatedButton(
        "Add Item",
        on_click=save_item,
        bgcolor="#26A69A",  # Light teal color
        color="white",
        width=150
    )

    back_button = ft.ElevatedButton(
        "Back",
        on_click=add_item,
        bgcolor="#26A69A",  # Light teal color
        color="white",
        width=150
    )

    # Create the column for the input fields and button
    content = ft.Column(
        [
            heading,  # Heading at the top
            ft.Container(
                content=ft.Column(
                    [
                        item_name,
                        item_quantity,
                        buy_price,
                    ],
                    spacing=20,
                    alignment="center"
                ),
                alignment=ft.alignment.center,
                padding=ft.padding.Padding(left=0, top=20, right=0, bottom=0)
            ),
            ft.Container(
                content=add_button,
                alignment=ft.alignment.center,
                padding=ft.padding.Padding(left=0, top=20, right=0, bottom=0)
            ),
            ft.Container(
                content=back_button,
                alignment=ft.alignment.center,
                padding=ft.padding.Padding(left=0, top=20, right=0, bottom=0)
            )
        ],
        alignment="start",  # Start alignment for top-center positioning
        horizontal_alignment="center",
        spacing=20
    )

    # Main container to keep everything top-centered
    main_container = ft.Container(
        content=content,
        alignment=ft.alignment.top_center,
        padding=ft.Padding(left=0, right=0, top=30, bottom=0),
        bgcolor="#2b3037",
        expand=True
    )

    # Add the main container to the page
    page.views.append(
        ft.View(
            "/add_item",
            controls=[main_container]
        )
    )
    page.update()
