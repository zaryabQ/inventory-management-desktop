import flet as ft

def main(page: ft.Page):
    # Set the page background color
    page.bgcolor = "#383838"

    # Create a function to handle the update button click
    def update_inventory(e):
        # Logic for updating the inventory
        print("Update button clicked")

    # Define the text fields with white background color
    name_field = ft.TextField(label="Enter the New Name", width=300, bgcolor=ft.colors.WHITE)
    quantity_field = ft.TextField(label="Enter the New Quantity", width=300, bgcolor=ft.colors.WHITE)
    price_field = ft.TextField(label="Enter the New Price", width=300, bgcolor=ft.colors.WHITE)

    # Define the update button
    update_button = ft.ElevatedButton(
        "Update", 
        bgcolor="#2abfbf", 
        color="#000000", 
        width=100, 
        on_click=update_inventory
    )
    
    # Create a container for the button to center it
    button_container = ft.Container(
        content=update_button,
        alignment=ft.alignment.center,
        padding=20
    )
    
    # Create a container for the input fields and the centered button
    input_container = ft.Container(
        content=ft.Column(
            controls=[
                name_field,
                quantity_field,
                price_field,
                button_container  # Place the button container inside the column
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=30
        ),
        padding=20,
        border_radius=20,
        bgcolor="#2b3037",  # Set the background color to #2b3037
        alignment=ft.alignment.center,
        height=500,  # Increase the height of the container
        width=600,   # Set a fixed width to ensure centering
        margin=ft.margin.only(left=100, top=30)
    )

    # Center the input container within the page
    page.add(
        ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Container(
                            content=ft.Text(
                                "Update Product",
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                color=ft.colors.WHITE,
                                font_family="Arial",  # Set the font family to Arial (or any other available font)
                                italic=True,  # Make the text italic
                            ),
                            padding=ft.padding.only(top=50)  # Adjust padding to move the heading down
                        ),
                        input_container
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=30
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,  # Aligns the Row's content to the center
            vertical_alignment=ft.CrossAxisAlignment.CENTER,  # Ensures vertical centering
        )
    )

# Start the Flet app
ft.app(target=main)
