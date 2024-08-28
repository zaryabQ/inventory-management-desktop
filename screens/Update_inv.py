import flet as ft

class UpdateView(ft.UserControl):
    def __init__(self,page, item_data, on_update):
        super().__init__()
        
        self.item_data = item_data
        self.on_update = on_update

    def build(self):
        # Create a function to handle the update button click
        def update_action(e):
            # Perform update logic here using the updated values from fields
            # print(f"Updating product: {name_field.value}, {quantity_field.value}, {price_field.value}")
            # Update the item in the database or the inventory list
            # (e.g., call to the database or update the data structure)
            # Call the on_update callback to return to the Inventory screen
            if self.page.views:
                self.page.views.pop()  # Remove the update view from the view stack
            self.on_update()  # This should navigate to the inventory screen
            self.page.update()

        # Define the update button
        update_button = ft.ElevatedButton(
            "Update", 
            bgcolor="#2abfbf", 
            color="#000000", 
            width=100, 
            on_click=update_action
        )
        
        # Create fields for the update view
        name_field = ft.Container(
            content=ft.TextField(label="Enter the New Name", width=300, bgcolor=ft.colors.WHITE),
            alignment=ft.alignment.center
        )
        quantity_field = ft.Container(
            content=ft.TextField(label="Enter Quantity", width=300, bgcolor=ft.colors.WHITE),
            alignment=ft.alignment.center
        )
        price_field = ft.Container(
            content=ft.TextField(label="Enter Price", width=300, bgcolor=ft.colors.WHITE),
            alignment=ft.alignment.center
        )
        
        # Create a container for the button to center it
        button_container = ft.Container(
            content=update_button,
            alignment=ft.alignment.center
        )
        
        # Create a container for the input fields and the centered button
        input_container = ft.Container(
            content=ft.Column(
                controls=[
                    name_field,
                    quantity_field,
                    price_field,
                    button_container
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=30
            ),
            padding=20,
            border_radius=20,
            bgcolor="#2b3037",
            height=self.page.height * 0.7,
            width=self.page.width * 0.5,
            margin=ft.margin.only(top=30)
        )

        return ft.View(
            "/update",
            controls=[
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
                                        font_family="Arial",
                                        italic=True
                                    ),
                                    padding=ft.padding.only(top=50),
                                    alignment=ft.alignment.center,
                                    width=self.page.width * 0.5
                                ),
                                input_container
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.alignment.center
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            ]
        )
