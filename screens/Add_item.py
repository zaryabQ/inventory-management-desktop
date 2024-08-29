import flet as ft

def main(page: ft.Page):

    def add_item(e):
        # Code to add the item to the inventory
        pass

    # Page settings
    page.title = "Inventory Management"
    page.bgcolor = "#383838"  # Dark background

    # Heading
    heading = ft.Text(
        "Add Items to Inventory",
        size=36,
        weight=ft.FontWeight.W_900,
        color="#26A69A",
        text_align=ft.TextAlign.CENTER,
        italic=True
    )

    # Creating the input fields
    item_id = ft.TextField(
        hint_text="Enter the Item's ID",
        bgcolor="white",
        color="black",
        border_radius=10,
        text_align="center",
        width=300
    )

    item_name = ft.TextField(
        hint_text="Enter Item Name",
        bgcolor="white",
        color="black",
        border_radius=10,
        text_align="center",
        width=300
    )

    quantity = ft.TextField(
        hint_text="Enter the Quantity",
        bgcolor="white",
        color="black",
        border_radius=10,
        text_align="center",
        width=300
    )

    buy_price = ft.TextField(
        hint_text="Enter the Buy Price",
        bgcolor="white",
        color="black",
        border_radius=10,
        text_align="center",
        width=300
    )

    sale_price = ft.TextField(
        hint_text="Enter the Sale Price",
        bgcolor="white",
        color="black",
        border_radius=10,
        text_align="center",
        width=300
    )

    # Creating the add button
    add_button = ft.ElevatedButton(
        "Add Item",
        on_click=add_item,
        bgcolor="#26A69A",  # Light teal color
        color="white",
        width=150
    )

    # Container for input fields
    inputs_container = ft.Column(
        [
            item_id,
            item_name,
            quantity,
            buy_price,
            sale_price
        ],
        alignment="center",
        spacing=20
    )

    # Container for the button
    button_container = ft.Container(
        content=add_button,
        alignment=ft.alignment.center,
    )

    # Main container for inputs and button
    inputs_and_button_container = ft.Container(
        content=ft.Column(
            [
                inputs_container,
                button_container
            ],
            alignment="center",
            spacing=20
         ),
        
    )

    # Container for the heading
    heading_container = ft.Container(
        content=heading,
        alignment=ft.alignment.top_center,  # Align the heading at the top center
        padding=ft.Padding(left=0, top=20, right=0, bottom=40)  # Specify padding for all sides
    )

    # Main container to center content and manage responsiveness
    main_container = ft.Container(
        content=ft.Column(
            [
                heading_container,  # Heading at the top
                inputs_and_button_container  # Input fields and button below the heading
            ],
            alignment="start",  # Align the column at the start (top) of the page
            spacing=20
        ),
        alignment=ft.alignment.center,
        expand=True  # Ensure it fills the available space
    )

    # Add the main container to the page
    page.add(main_container)

ft.app(target=main)
