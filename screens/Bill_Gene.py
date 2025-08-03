import flet as ft
from flet import *
import sqlite3
from db.billing_handler import BillingHandler
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

def bill_gen(page ,load_bills_callback):
    global items, total_amount, paid_amount, remaining_amount
    
    items = []
    total_amount = 0.0
    paid_amount = 0.0
    remaining_amount = 0.0

    page.title = "Generate Bill"
    page.bgcolor = ZeroYellowTheme.BG_PRIMARY


    items = []

    def calculate_totals():
        global total_amount, remaining_amount
        total_amount = sum(item['quantity'] * item['price'] for item in items)
        remaining_amount = total_amount - paid_amount
        total_amount_text.value = f"Total Amount: {total_amount:.2f}"
        remaining_amount_text.value = f"Remaining Amount: {remaining_amount:.2f}"
        page.update()

    def update_paid_amount(e):
        global paid_amount
        paid_amount = float(paid_input.value) if paid_input.value else 0.0
        calculate_totals()

    def update_item(e, item_id):
        item = next((i for i in items if i["id"] == item_id), None)
        
        if not item:
            return
        

        popup = zero_yellow_alert_dialog(
            modal=True,
            title=zero_yellow_text(f"Update {item['name']}", color=ZeroYellowTheme.TEXT_PRIMARY),
            content=ft.Column([
                zero_yellow_text_field(label="Quantity", value=str(item['quantity'])),
                zero_yellow_text_field(label="Selling Price", value=str(item['price'])),
            ]),
            actions=[
                zero_yellow_button(
                    "Save",
                    on_click=lambda e: [setattr(popup, 'open', False), update_item_details(item, popup.content)],
                    primary=True
                ),
                zero_yellow_button(
                    "Remove",
                    on_click=lambda e: [remove_item(item_id), setattr(popup, 'open', False)],
                    primary=False
                ),
            ],
        )
        page.dialog = popup
        popup.open = True
        page.update()

    def update_item_details(item, content):
        global items
        quantity = int(content.controls[0].value)
        price = float(content.controls[1].value)

        # Update the item's quantity and price in the bill
        item['quantity'] = quantity
        item['price'] = price

        # Update the item's container in the list to reflect new values
        item["container"] = ft.Container(
            content=ft.Row(
                controls=[
                    zero_yellow_text(item["name"], color=ZeroYellowTheme.TEXT_PRIMARY),
                    zero_yellow_text(str(item["quantity"]), color=ZeroYellowTheme.TEXT_PRIMARY),
                    zero_yellow_text(str(item["price"]), color=ZeroYellowTheme.TEXT_PRIMARY),
                    zero_yellow_icon_button(
                        icon=Icons.CHANGE_CIRCLE_OUTLINED,
                        icon_color=ZeroYellowTheme.TEXT_PRIMARY,
                        tooltip="Update",
                        on_click=lambda e, item_id=item["id"]: update_item(e, item["id"])
                    ),
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            bgcolor=ZeroYellowTheme.BG_GLASS,
            padding=ft.padding.all(8),
            border_radius=ft.border_radius.all(12),
            margin=ft.margin.symmetric(vertical=3),
            border=ft.border.all(1, ZeroYellowTheme.GLASS_BORDER),
        )

        # Update the item table to reflect the changes
        update_item_table()


    def remove_item(item_id):
        global items
        items = [item for item in items if item["id"] != item_id]
        update_item_table()

    def update_item_table():
        item_table.content.controls.clear()
        for item in items:
            item_table.content.controls.append(item["container"])
        calculate_totals()  
        page.update()

    def show_search_popup(page: ft.Page, on_item_selected):
        def search_item(e):
            search_query = search_field.value.lower()
            results.controls.clear()

            conn = sqlite3.connect('db/sql.db')
            cursor = conn.cursor()

            # Replace with actual search query
            cursor.execute("SELECT * FROM inventory WHERE name LIKE ?", ('%' + search_query + '%',))
            inventory = cursor.fetchall()

            conn.close()

            for item in inventory:
                item_data = {
                    "id": item[0],  # Assuming ID is at index 0
                    "name": item[1], 
                    "quantity": item[2], # Name at index 1
                    "price": item[3],  # Selling price at index 2
                }
                results.controls.append(
                    ft.ListTile(
                        title=ft.Text(item_data["name"], color=IOS26Theme.TEXT_PRIMARY),
                        subtitle=ft.Text(f"Quantity: {item_data['quantity']}\nPrice: {item_data['price']}", color=IOS26Theme.TEXT_SECONDARY),
                        on_click=lambda e, item=item_data: on_item_selected(item),
                        bgcolor=IOS26Theme.GLASS_BACKGROUND,
                    )
                )

            page.update()

        search_field = modern_text_field(
            label="Search Items",
            on_change=search_item,
            width=300,
        )

        results = ft.Column()

        popup = ft.AlertDialog(
            modal=True,
            title=ft.Text("Search Items", color=IOS26Theme.TEXT_PRIMARY),
            content=ft.Column([
                search_field,
                results
            ]),
            bgcolor=IOS26Theme.BACKGROUND_TERTIARY,  # Override default dialog background
            title_text_style=ft.TextStyle(color=IOS26Theme.TEXT_PRIMARY),
            content_text_style=ft.TextStyle(color=IOS26Theme.TEXT_PRIMARY),
            actions=[
                ft.TextButton(
                    "Close",
                    on_click=lambda e: [setattr(popup, 'open', False), popup.update()],
                    style=ft.ButtonStyle(bgcolor=IOS26Theme.ACCENT_PRIMARY, color=IOS26Theme.BACKGROUND_PRIMARY),
                ),
            ],
        )

        page.dialog = popup
        popup.open = True
        page.update()

    def add_item(e):
        def on_item_selected(item):
            # Use the correct item_id from the database
            item_id = item["id"]  # This is the actual ID from the database

            items.append(
                {
                    "id": item_id,  # Store the correct item_id here
                    "name": item["name"],
                    "quantity": 1,  # Start with quantity 1
                    "price": item["price"],

                    # The container remains the same
                    "container": ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Text(item["name"], width=150, color=ZeroYellowTheme.TEXT_PRIMARY, text_align=ft.TextAlign.CENTER),
                                ft.Text("1", width=50, color=ZeroYellowTheme.TEXT_PRIMARY, text_align=ft.TextAlign.CENTER),
                                ft.Text(str(item["price"]), width=100, color=ZeroYellowTheme.TEXT_PRIMARY, text_align=ft.TextAlign.CENTER),
                                ft.IconButton(
                                    icon=Icons.CHANGE_CIRCLE_OUTLINED,
                                    icon_color=ZeroYellowTheme.TEXT_PRIMARY,
                                    tooltip="Update",
                                    on_click=lambda e, item_id=item_id: update_item(e, item_id)  # Use the correct ID
                                ),
                            ],
                            spacing=10,
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        bgcolor=IOS26Theme.GLASS_BACKGROUND,
                        padding=ft.padding.all(8),
                        border_radius=ft.border_radius.all(12),
                        margin=ft.margin.symmetric(vertical=3),
                        border=ft.border.all(1, IOS26Theme.GLASS_BORDER),
                    ),
                }
            )
            update_item_table()
            
            page.dialog.open = False
            calculate_totals()
            page.update()
        
        show_search_popup(page, on_item_selected)



    def save_item(e):
        global items, total_amount, paid_amount, remaining_amount

        customer_name = input_field.content.value.strip()

        # Same validations as before...

        # Prepare the item list and pass paid and remaining values for saving
        item_list = []
        for item in items:
            item_list.append({
                'id': item['id'],
                'name': item['name'],
                'quantity': item['quantity'],
                'selling_price': item['price'],
            })

        try:
            # Pass paid and remaining values to the BillingHandler
            BillingHandler.add_bill(customer_name, item_list, paid_amount, remaining_amount)

            # Success notification and clearing the form...
            items.clear()
            paid_input.value = "0"
            calculate_totals()
            page.views.pop()
            load_bills_callback()
            page.update()

        except ValueError as ve:
            # Alert the user in case of any validation errors (e.g., insufficient stock)
            page.snack_bar = zero_yellow_snackbar(str(ve))
            page.snack_bar.open = True
            page.update()

        except Exception as e:
            # Handle unexpected errors
            page.snack_bar = zero_yellow_snackbar(f"Error: {str(e)}")
            page.snack_bar.open = True
            page.update()

    def go_back(e):
        page.views.pop()
        page.update()

    total_amount_text = zero_yellow_text(value="Total Amount: 0.00", color=ZeroYellowTheme.TEXT_PRIMARY)
    paid_input = zero_yellow_text_field(label="Paid", value="0", on_change=update_paid_amount)
    remaining_amount_text = zero_yellow_text(value="Remaining Amount: 0.00", color=ZeroYellowTheme.TEXT_PRIMARY)

    input_field = zero_yellow_text_field(
        label="Enter Name/ID",
        width=300,
        height=50,
        text_align=ft.TextAlign.CENTER,
    )

    add_items_button = zero_yellow_button(
        text="Add Items",
        width=150,
        height=45,
        on_click=add_item,
        primary=True
    )

    # Wrap ListView in a glass container to override any default background colors
    item_table_list = ft.ListView(
        controls=[],
        spacing=5,
        padding=10,
        width=480,  # Slightly smaller to fit in glass container
        height=280,
        auto_scroll=True,
    )
    
    item_table = zero_yellow_container(
        content=item_table_list,
        width=500,
        height=300,
        padding=padding.all(10),
        margin=margin.all(0)
    )

    save_button = zero_yellow_button(
        text="Save",
        width=150,
        height=45,
        on_click=save_item,
        primary=True
    )

    go_back_btn = zero_yellow_button(
        text="Back",
        width=150,
        height=45,
        on_click=go_back,
        primary=False
    )

    main_container = zero_yellow_container(
        content=ft.Column(
            controls=[
                input_field,
                Container(height=10),
                add_items_button,
                Container(height=10),
                item_table,
                Container(height=10),
                total_amount_text,
                paid_input,
                remaining_amount_text,
                Container(height=10),
                Row(
                    controls=[
                        save_button,
                        Container(width=20),
                        go_back_btn
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
            ],
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        width=700,  # Wider for better content
        # Remove fixed height to auto-size
        padding=padding.all(40),  # More generous padding
        margin=margin.all(20)
    )

    page.views.append(
        ft.View(
            "/bill",
            bgcolor=ZeroYellowTheme.BG_PRIMARY,
            scroll=ScrollMode.AUTO,  # Make view scrollable
            controls=[
                ft.Column(
                    controls=[
                        ft.Container(
                            content=zero_yellow_text("Generate Bill", size=30, weight=FontWeight.BOLD, color=ZeroYellowTheme.PURE_BLACK), 
                            alignment=ft.alignment.center
                        ),
                        ft.Container(content=main_container, alignment=ft.alignment.center),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=30,
                )
            ]
        )
    )
    page.update()