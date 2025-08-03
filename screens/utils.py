from flet import *
import flet as ft
from db.inv_handler import InventoryHandler
from screens.theme import (
    ZeroYellowTheme, 
    zero_yellow_container, 
    zero_yellow_button, 
    zero_yellow_text_field, 
    zero_yellow_text,
    zero_yellow_icon,
    zero_yellow_snackbar,
    # Legacy compatibility
    IOS26Theme,
    glass_container,
    primary_button,
    secondary_button,
    modern_text_field,
    heading_text,
    body_text,
    modern_icon
)

def main_inv_upd(page, item_data, on_update):
    name_field = zero_yellow_text_field(label="Product Name", value=item_data[1], width=400, height=50)
    quantity_field = zero_yellow_text_field(label="Quantity", value=str(item_data[2]), width=400, height=50)
    price_field = zero_yellow_text_field(label="Price", value=str(item_data[3]), width=400, height=50)

    def update_action(e):
        empty_fields = []
        if not name_field.value.strip():
            empty_fields.append("Name")
        if not quantity_field.value.strip():
            empty_fields.append("Quantity")
        if not price_field.value.strip():
            empty_fields.append("Price")

        if empty_fields:
            page.snack_bar = zero_yellow_snackbar(f"Fields missing: {', '.join(empty_fields)}. Please fill at least one field.")
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
            bgcolor=ZeroYellowTheme.BG_PRIMARY,
            scroll=ScrollMode.AUTO,  # Make view scrollable
            controls=[
                ft.Row(
                    controls=[
                        zero_yellow_container(
                            content=ft.Column(
                                controls=[
                                    zero_yellow_text(
                                        "Update Product",
                                        size=24,
                                        weight=FontWeight.BOLD,
                                        color=ZeroYellowTheme.PURE_BLACK  # Black heading
                                    ),
                                    Container(height=30),  # More space after heading
                                    name_field,
                                    Container(height=15),  # Better spacing
                                    quantity_field,
                                    Container(height=15),  # Better spacing
                                    price_field,
                                    Container(height=40),  # More space before buttons
                                    Row(
                                        controls=[
                                            zero_yellow_button(
                                                text="Update",
                                                on_click=update_action,
                                                width=140,  # Slightly wider
                                                height=50,  # Slightly taller
                                                primary=True
                                            ),
                                            Container(width=30),  # More space between buttons
                                            zero_yellow_button(
                                                text="Back",
                                                on_click=back_action,
                                                width=140,  # Slightly wider
                                                height=50,  # Slightly taller
                                                primary=False
                                            )
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        spacing=10  # Add spacing
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=10,
                                expand=True
                            ),
                            width=page.width * 0.6,  # Slightly wider
                            # Remove fixed height to auto-size
                            padding=padding.all(40),  # More generous padding
                            margin=margin.all(20)
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
            bgcolor=ZeroYellowTheme.BG_PRIMARY,
            controls=[
                zero_yellow_container(
                    content=Column(
                        controls=[
                            zero_yellow_text(
                                "Are you sure you want to remove the entry?",
                                size=24,
                                weight=FontWeight.BOLD,
                                color=ZeroYellowTheme.PURE_BLACK,  # Black heading
                                text_align=TextAlign.CENTER
                            ),
                            Container(height=40),
                            Row(
                                controls=[
                                    Container(
                                        content=zero_yellow_icon(
                                        icon=Icons.CLOSE,
                                        size=40,
                                        color=ZeroYellowTheme.TEXT_PRIMARY
                                    ),
                                        on_click=cancel_remove,
                                        padding=20,
                                        border_radius=12,
                                        bgcolor=ZeroYellowTheme.ERROR,
                                        border=border.all(1, ZeroYellowTheme.GLASS_BORDER)
                                    ),
                                    Container(width=30),
                                    Container(
                                        content=zero_yellow_icon(
                                        icon=Icons.CHECK,
                                        size=40,
                                        color=ZeroYellowTheme.TEXT_PRIMARY
                                    ),
                                        on_click=confirm_remove,
                                        padding=20,
                                        border_radius=12,
                                        bgcolor=ZeroYellowTheme.SUCCESS,
                                        border=border.all(1, ZeroYellowTheme.GLASS_BORDER)
                                    ),
                                ],
                                alignment=MainAxisAlignment.CENTER,
                                spacing=20,
                            ),
                        ],
                        alignment=MainAxisAlignment.CENTER,
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        spacing=20,
                    ),
                    width=400,
                    height=300,
                    padding=40,
                    margin=20
                )
            ],
            horizontal_alignment=CrossAxisAlignment.CENTER,
            vertical_alignment=MainAxisAlignment.CENTER,
        )
    )
    page.update()