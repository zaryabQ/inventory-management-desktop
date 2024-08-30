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
            size=30,
            weight=ft.FontWeight.BOLD,
            color='#26A69A',
            font_family="Arial",  # Set the font family to Arial (or any other available font)
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

    # Create the column for the input fields and button
    content = ft.Column(
        [
            heading,  # Heading at the top
            ft.Container(
                content=ft.Column(
                    [
                        item_id,
                        item_name,
                        quantity,
                        buy_price,
                        sale_price,
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
        expand=True
    )

    # Add the main container to the page
    page.add(main_container)

ft.app(target=main)
