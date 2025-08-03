import flet as ft
from flet import *
from db.billing_handler import BillingHandler
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

def bill_updt(page, bill_id, load_bill_callback):
    global items, filtered_items, items_to_remove ,total_amount,remaining_amount,paid_amount

    # Fetch items from the bill_item table using the bill_id
    items = BillingHandler.fetch_bill_items(bill_id)
    bill_detail = BillingHandler.fetch_bill_details(bill_id)
    filtered_items = items.copy()
    bill_name = bill_detail["name"]
    total_amount = bill_detail["total"]
    paid_amount = bill_detail["paid_amt"]
    remaining_amount = bill_detail["rem_amt"]

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
    # Track items marked for removal
    items_to_remove = []

    def update_item(e, item_id):
        item = next((i for i in items if i["id"] == item_id), None)
        if not item:
            return

        popup = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Update {item['name']}" ,color=IOS26Theme.TEXT_PRIMARY),
            content=ft.Column([
                modern_text_field(label="Quantity", value=str(item['quantity'])),
                modern_text_field(label="Selling Price", value=str(item['price'])),
            ]),
            bgcolor=IOS26Theme.BACKGROUND_TERTIARY,  # Override default dialog background
            title_text_style=ft.TextStyle(color=IOS26Theme.TEXT_PRIMARY),
            content_text_style=ft.TextStyle(color=IOS26Theme.TEXT_PRIMARY),
            actions=[
                ft.TextButton(
                    "Save",
                    on_click=lambda e: [setattr(popup, 'open', False), update_item_details(item, popup.content)],
                    style=ft.ButtonStyle(bgcolor=IOS26Theme.ACCENT_PRIMARY, color=IOS26Theme.BACKGROUND_PRIMARY),
                ),
                ft.TextButton(
                    "Remove",
                    on_click=lambda e: [mark_item_for_removal(item_id), setattr(popup, 'open', False)],
                    style=ft.ButtonStyle(bgcolor=IOS26Theme.ACCENT_QUATERNARY, color=IOS26Theme.TEXT_PRIMARY),
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

        # Update the item's data
        item['quantity'] = quantity
        item['price'] = price

        # Reflect the changes visually in the UI (no DB changes yet)
        update_item_table()

    def mark_item_for_removal(item_id):
        global items_to_remove, filtered_items
        item = next((i for i in filtered_items if i["id"] == item_id), None)
        if item:
            # Mark item for removal and remove it from the filtered_items (UI)
            items_to_remove.append(item_id)
            filtered_items = [i for i in filtered_items if i["id"] != item_id]

        # Update the item table to reflect the changes in the UI
        update_item_table()

    def update_item_table():
        item_table.content.controls.clear()
        for item in filtered_items:
            item["container"] = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Text(item["name"], width=150, color=IOS26Theme.TEXT_PRIMARY, text_align=ft.TextAlign.CENTER),
                        ft.Text(str(item["quantity"]), width=50, color=IOS26Theme.TEXT_PRIMARY, text_align=ft.TextAlign.CENTER),
                        ft.Text(str(item["price"]), width=100, color=IOS26Theme.TEXT_PRIMARY, text_align=ft.TextAlign.CENTER),
                        ft.IconButton(
                            icon=Icons.CHANGE_CIRCLE_OUTLINED,
                            icon_color=IOS26Theme.ACCENT_PRIMARY,
                            tooltip="Update",
                            on_click=lambda e, item_id=item["id"]: update_item(e, item["id"])
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
            )
            item_table.content.controls.append(item["container"])
        calculate_totals()
        page.update()

    def save_bill(e):
    # Collect updated items from the UI
        updated_items = []
        for item in filtered_items:
            # Check if the item is marked for removal
            if item.get('removed', False):
                continue
            
            # Prepare updated item details
            updated_item = {
                'id': item['id'],
                'name': item['name'],
                'quantity': item['quantity'],
                'price': item['price'],
                'removed': False
            }
            updated_items.append(updated_item)

        # Add items to be removed
        for item_name in items_to_remove:
            updated_items.append({
                'id': None,  # ID will be determined in the function
                'name': item_name,
                'quantity': 0,
                'price': 0,
                'removed': True
            })

        # Retrieve selected status from the dropdown
        bill_status = bill_status_dropdown.value
        name = name_field.value
        


        try:
            # Call the function to save changes, including status
            BillingHandler.save_bill_changes(bill_id, updated_items, bill_status, name, paid_amount, remaining_amount)

            # Clear the removal list after saving
            items_to_remove.clear()

            # Go back after saving
            page.views.pop()
            load_bill_callback()
            page.update()
            
        except ValueError as ve:
            # Alert the user in case of any validation errors (e.g., insufficient stock)
            page.snack_bar = ft.SnackBar(
                content=ft.Text(str(ve), color=IOS26Theme.TEXT_PRIMARY),
                bgcolor=IOS26Theme.ACCENT_QUATERNARY
            )
            page.snack_bar.open = True
            page.update()

        except Exception as e:
            # Handle unexpected errors
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Error: {str(e)}", color=IOS26Theme.TEXT_PRIMARY),
                bgcolor=IOS26Theme.ACCENT_QUATERNARY
            )
            page.snack_bar.open = True
            page.update()

    def go_back(e):
        page.views.pop()
        page.update()



    total_amount_text = ft.Text(value=f"Total Amount: {total_amount:.2f}", color=IOS26Theme.TEXT_PRIMARY)
    paid_input = modern_text_field(label=f"Paid Amount", value=paid_amount, on_change=update_paid_amount)
    remaining_amount_text = ft.Text(value=f"Remaining Amount: {remaining_amount:.2f}", color=IOS26Theme.TEXT_PRIMARY)

    # Dropdown for Bill Status (Paid/Unpaid) - Override any yellow colors
    bill_status_dropdown = ft.Dropdown(
        label="Bill Status",
        options=[
            ft.dropdown.Option("Paid"),
            ft.dropdown.Option("Unpaid"),
        ],
        bgcolor=IOS26Theme.GLASS_BACKGROUND,
        color=IOS26Theme.TEXT_PRIMARY,
        border_color=IOS26Theme.GLASS_BORDER,
        focused_border_color=IOS26Theme.ACCENT_PRIMARY,
        label_style=ft.TextStyle(color=IOS26Theme.TEXT_SECONDARY),
        text_style=ft.TextStyle(color=IOS26Theme.TEXT_PRIMARY),
    )

    name_field = modern_text_field(
            label="Enter Name/ID",
            value=bill_name,
            width=300,
            height=50,
            text_align=ft.TextAlign.CENTER,
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
        on_click=save_bill,
        primary=True
    )

    back_button = zero_yellow_button(
        text="Back",
        width=150,
        height=45,
        on_click=go_back,
        primary=False
    )

    main_container = zero_yellow_container(
        content=ft.Column(
            controls=[
                name_field,
                Container(height=10),
                item_table,
                Container(height=10),
                total_amount_text,
                paid_input,
                remaining_amount_text,
                bill_status_dropdown,
                Container(height=10),
                Row(
                    controls=[
                        save_button,
                        Container(width=20),
                        back_button
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
            "/update_bill",
            bgcolor=ZeroYellowTheme.BG_PRIMARY,
            scroll=ScrollMode.AUTO,  # Make view scrollable
            controls=[
                ft.Column(
                    controls=[
                        ft.Container(
                            content=zero_yellow_text("Update Bill", size=30, weight=FontWeight.BOLD, color=ZeroYellowTheme.PURE_BLACK), 
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

    update_item_table()
    page.update()
