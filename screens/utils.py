from flet import *
import flet as ft
from db.inv_handler import InventoryHandler

def main_inv_upd(page, item_data, on_update):
    name_field = ft.TextField(label="Product Name", value=item_data[1], bgcolor=ft.colors.WHITE, width=page.width * 0.4)
    quantity_field = ft.TextField(label="Quantity", value=str(item_data[2]), bgcolor=ft.colors.WHITE, width=page.width * 0.4)
    price_field = ft.TextField(label="Price", value=str(item_data[3]), bgcolor=ft.colors.WHITE, width=page.width * 0.4)

    def update_action(e):
        empty_fields = []
        if not name_field.value.strip():
            empty_fields.append("Name")
        if not quantity_field.value.strip():
            empty_fields.append("Quantity")
        if not price_field.value.strip():
            empty_fields.append("Price")

        if empty_fields:
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Fields missing: {', '.join(empty_fields)}. Please fill at least one field."),
                action="DISMISS"
            )
            page.snack_bar.open = True
            page.update()

            # On second click, proceed with update if at least one field is filled
            if len(empty_fields) < 3:
                update_db_fields = {
                    'name': name_field.value if name_field.value.strip() else item_data[1],
                    'quantity': quantity_field.value if quantity_field.value.strip() else item_data[2],
                    'price': price_field.value if price_field.value.strip() else item_data[3]
                }
                on_update(update_db_fields)
                page.views.pop()
                page.update()
        else:
            # Update the item in the database
            update_db_fields = {
                'name': name_field.value,
                'quantity': quantity_field.value,
                'price': price_field.value
            }
            on_update(update_db_fields)
            page.views.pop()
            page.update()

    def back_action(e):
        page.views.pop()
        page.update()

    page.views.append(
        ft.View(
            "/update",
            bgcolor="#2b3037",
            controls=[
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text(
                                        "Update Product",
                                        size=24,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.colors.WHITE,
                                        font_family="Arial",
                                        italic=True
                                    ),
                                    name_field,
                                    quantity_field,
                                    price_field,
                                    ft.ElevatedButton(
                                        "Update",
                                        on_click=update_action,
                                        bgcolor="#2abfbf",
                                        color="#000000"
                                    ),
                                    ft.ElevatedButton(
                                        "Back",
                                        on_click=back_action,
                                        bgcolor="#2abfbf",
                                        color="#000000"
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=30,
                                expand=True
                            ),
                            padding=20,
                            border_radius=20,
                            bgcolor="#383838",
                            width=page.width * 0.5,
                            alignment=ft.alignment.center,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    expand=True
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
        )
    )
    page.update()




def main_remove(page, item_id, on_remove):
    def cancel_remove(e):
        on_remove()  # Return to the Inventory screen without removing

    def confirm_remove(e):
        InventoryHandler.remove_item_from_db(item_id=item_id)
        on_remove()  # Refresh the inventory screen after removing

    page.views.append(
        View(
            "/remove",
            controls=[
                Column(
                    controls=[
                        Container(
                            content=Text(
                                "Are you sure you want to remove the entry?",
                                color="red",
                                size=24,
                                weight=FontWeight.BOLD,
                                text_align=TextAlign.CENTER
                            ),
                            alignment=alignment.center,
                            padding=padding.only(top=150)
                        ),
                        Row(
                            controls=[
                                IconButton(
                                    icon=icons.CLOSE,
                                    icon_color="white",
                                    bgcolor="teal",
                                    on_click=cancel_remove,
                                    width=70,
                                    height=70,
                                    icon_size=40
                                ),
                                IconButton(
                                    icon=icons.CHECK,
                                    icon_color="white",
                                    bgcolor="teal",
                                    on_click=confirm_remove,
                                    width=70,
                                    height=70,
                                    icon_size=40
                                ),
                            ],
                            alignment=MainAxisAlignment.CENTER,
                            spacing=50,
                        ),
                    ],
                    alignment=MainAxisAlignment.CENTER,
                    spacing=100,
                )
            ]
        )
    )
    page.update()