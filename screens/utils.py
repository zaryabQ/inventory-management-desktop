from flet import *
from db.inv_handler import InventoryHandler
def main_inv_upd(page, item_data, on_update):
    name_field = TextField(label="Product Name", value=item_data[1])
    quantity_field = TextField(label="Quantity", value=str(item_data[3]))
    price_field = TextField(label="Price", value=str(item_data[4]))

    def update_action(e):
        InventoryHandler.update_item_in_db(item_id=item_data[0], name=name_field.value, quantity=quantity_field.value, price=price_field.value)
        on_update()  # Refresh the inventory screen

    page.views.append(
        View(
            "/update",
            controls=[
                Column(
                    controls=[
                        Container(
                            content=Text(
                                "Update Product",
                                size=24,
                                weight=FontWeight.BOLD,
                                color=colors.WHITE,
                                font_family="Arial",
                                italic=True
                            ),
                            padding=padding.only(top=50),
                            alignment=alignment.center,
                            width=page.width * 0.5
                        ),
                        Container(
                            content=Column(
                                controls=[
                                    name_field,
                                    quantity_field,
                                    price_field,
                                    ElevatedButton(
                                        "Update",
                                        on_click=update_action,
                                        bgcolor="#2abfbf",
                                        color="#000000"
                                    ),
                                ],
                                alignment=MainAxisAlignment.CENTER,
                                spacing=30
                            ),
                            padding=20,
                            border_radius=20,
                            bgcolor="#2b3037",
                            height=page.height * 0.7,
                            width=page.width * 0.5,
                            margin=margin.only(top=30)
                        ),
                    ],
                    alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            ]
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