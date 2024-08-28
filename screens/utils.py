import flet as ft
from flet import *

def main_inv_upd(page, item_data, on_update):
    page.bgcolor = "#383838"

    # Create a function to handle the update button click
    def update_action(e):
        # Perform update logic here using the updated values from fields
        # print(f"Updating product: {name_field.value}, {quantity_field.value}, {price_field.value}")
        # Update the item in the database or the inventory list
        # (e.g., call to the database or update the data structure)
        # Call the on_update callback to return to the Inventory screen
        if page.views:
            page.views.pop()  # Remove the update view from the view stack
        on_update()  # This should navigate to the inventory screen
        page.update()


    # Define the update button
    update_button = ft.ElevatedButton(
        "Update", 
        bgcolor="#2abfbf", 
        color="#000000", 
        width=100, 
        on_click=update_action
    )
    name_field = Container(
        content=TextField(label="Enter the New Name", width=300, bgcolor=ft.colors.WHITE),
        alignment=ft.alignment.center,
        # padding=20
    )
    quantity_field = Container(
        content=TextField(label="Enter the New Name", width=300, bgcolor=ft.colors.WHITE),
        alignment=ft.alignment.center,
        # padding=20
    )
    price_field = Container(
        content=TextField(label="Enter the New Name", width=300, bgcolor=ft.colors.WHITE),
        alignment=ft.alignment.center,
        # padding=20
    )
    # Create a container for the button to center it
    button_container = Container(
        content=update_button,
        alignment=ft.alignment.center,
        # padding=20
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
            alignment=MainAxisAlignment.CENTER,
            spacing=30
        ),
        padding=20,
        border_radius=20,
        bgcolor="#2b3037",  # Set the background color to #2b3037
        # alignment=ft.alignment.center,
        height=page.height * 0.7,   # Increase the height of the container
        width=page.width * 0.5,   # Set a fixed width to ensure centering
        margin=ft.margin.only(top=30)
    )
    

    page.views.append(
        View(
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
                                        font_family="Arial",  # Set the font family to Arial (or any other available font)
                                        italic=True  # Make the text italic
                                    ),
                                    padding=ft.padding.only(top=50),
                                    alignment=ft.alignment.center,
                                    width=page.width * 0.5 
                                    # Adjust padding to move the heading down
                                ),
                                input_container
                            ],
                            alignment = MainAxisAlignment.CENTER,
                            horizontal_alignment=alignment.center
                        
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,  # Aligns the Row's content to the center
                )
            ]
        )
    )
    page.go("/update")

def main_remove(page, item_id, on_remove):
    
    def cancel_remove(e):
        print("Entry removal cancelled")
        if page.views:
            page.views.pop()  # Remove the update view from the view stack
        on_remove()  # This should navigate to the inventory screen
        page.update()
          # Return to the Inventory screen without removing

    def confirm_remove(e):
        print(f"Entry {item_id} removed")
        # Logic to remove the item from the database or inventory list
        if page.views:
            page.views.pop()  # Remove the update view from the view stack
        on_remove()  # This should navigate to the inventory screen
        page.update()  # Return to the Inventory screen after removing

    page.views.append(
        View(
            "/remove",
            controls=[
                Column(
                    controls=[
                        Container(
                            content=Text(
                                "Are you sure you want to remove the entry",
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
    page.go("/remove")


# def main_inv_upd(page: Page, item_data, on_update):
#     name_field = TextField(label="Product Name", value=item_data[1])
#     quantity_field = TextField(label="Quantity", value=str(item_data[2]))
#     price_field = TextField(label="Price", value=str(item_data[3]))

#     def update_action(e):
#         # Perform update logic here using the updated values from fields
#         print(f"Updating product: {name_field.value}, {quantity_field.value}, {price_field.value}")
#         # Update the item in the database or the inventory list
#         # (e.g., call to the database or update the data structure)
#         # Call the on_update callback to return to the Inventory screen
#         on_update()

#     page.views.append(
#         View(
#             "/update",
#             controls=[
#                 Column(
#                     controls=[
#                         Container(
#                             content=Text(
#                                 "Update Product",
#                                 size=24,
#                                 weight=ft.FontWeight.BOLD,
#                                 color=ft.colors.WHITE,
#                                 font_family="Arial",  # Set the font family to Arial (or any other available font)
#                                 italic=True  # Make the text italic
#                             ),
#                             padding=ft.padding.only(top=50),
#                             alignment=ft.alignment.center,
#                             width=page.width * 0.5 
#                             # Adjust padding to move the heading down
#                         ),
#                         Container(
#                             content=Column(
#                                 controls=[
#                                     name_field,
#                                     quantity_field,
#                                     price_field,
#                                     ElevatedButton(
#                                         "Update", 
#                                         on_click=update_action, 
#                                         bgcolor="#2abfbf", 
#                                         color="#000000"
#                                     ),
#                                 ],
#                                 alignment=MainAxisAlignment.CENTER,
#                                 spacing=30
#                             ),
#                             padding=20,
#                             border_radius=20,
#                             bgcolor="#2b3037",
#                             height=page.height * 0.7,
#                             width=page.width * 0.5,
#                             margin=ft.margin.only(top=30)
#                         ),
#                     ],
#                     alignment=MainAxisAlignment.CENTER,
#                     horizontal_alignment=CrossAxisAlignment.CENTER,
#                 )
#             ]
#         )
#     )
#     page.go("/update")

# Pagelet for Remove Item Confirmation