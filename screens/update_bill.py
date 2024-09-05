import flet as ft
from db.billing_handler import BillingHandler

def bill_updt(page, bill_id):
    global items, filtered_items, items_to_remove

    # Fetch items from the bill_item table using the bill_id
    items = BillingHandler.fetch_bill_items(bill_id)
    bill_detail = BillingHandler.fetch_bill_details(bill_id)
    filtered_items = items.copy()
    bill_name = bill_detail["name"]

    # Track items marked for removal
    items_to_remove = []

    def update_item(e, item_id):
        item = next((i for i in items if i["id"] == item_id), None)
        if not item:
            return

        popup = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Update {item['name']}" ,color="#26A69A"),
            content=ft.Column([
                ft.TextField(label="Quantity", value=str(item['quantity']), bgcolor="#FFFFFF"),
                ft.TextField(label="Selling Price", value=str(item['price']), bgcolor="#FFFFFF"),
            ]),
            actions=[
                ft.TextButton(
                    "Save",
                    on_click=lambda e: [setattr(popup, 'open', False), update_item_details(item, popup.content)],
                    style=ft.ButtonStyle(bgcolor="#2abfbf", color="#000000"),
                ),
                ft.TextButton(
                    "Remove",
                    on_click=lambda e: [mark_item_for_removal(item_id), setattr(popup, 'open', False)],
                    style=ft.ButtonStyle(bgcolor="#ff4d4d", color="#000000"),
                ),
            ],
            bgcolor="#383838",
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
        item_table.controls.clear()
        for item in filtered_items:
            item["container"] = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Text(item["name"], width=150, color="#000000", text_align=ft.TextAlign.CENTER),
                        ft.Text(str(item["quantity"]), width=50, color="#000000", text_align=ft.TextAlign.CENTER),
                        ft.Text(str(item["price"]), width=100, color="#000000", text_align=ft.TextAlign.CENTER),
                        ft.IconButton(
                            icon=ft.icons.CHANGE_CIRCLE_OUTLINED,
                            icon_color="#000000",
                            tooltip="Update",
                            on_click=lambda e, item_id=item["id"]: update_item(e, item["id"])
                        ),
                    ],
                    spacing=10,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                bgcolor="#FFFFFF",
                padding=ft.padding.all(4),
                border_radius=ft.border_radius.all(8),
                margin=ft.margin.symmetric(vertical=3),
            )
            item_table.controls.append(item["container"])
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

        try:
            # Call the function to save changes, including status
            BillingHandler.save_bill_changes(bill_id, updated_items, bill_status)

            # Clear the removal list after saving
            items_to_remove.clear()

            # Go back after saving
            page.views.pop()
            page.update()
            
        except Exception as ex:
            print(f"Failed to save bill changes: {ex}")
            # Handle exceptions or show error messages as needed

    def go_back(e):
        page.views.pop()
        page.update()

        
    # Dropdown for Bill Status (Paid/Unpaid)
    bill_status_dropdown = ft.Dropdown(
        label="Bill Status",
        options=[
            ft.dropdown.Option("Paid"),
            ft.dropdown.Option("Unpaid"),
        ],
        bgcolor="#FFFFFF",
        color="#000000",
    )

    search_field = ft.Container(
        width=300,
        height=45,
        content=ft.TextField(
            label="Enter Name/ID",
            value=bill_name,
            bgcolor="#FFFFFF",
            color="#000000",
            border_radius=ft.border_radius.all(8),
            height=50,
            text_align=ft.TextAlign.CENTER,
        ),
        bgcolor="#000000",
        border_radius=10,
    )

    item_table = ft.ListView(
        controls=[],
        spacing=5,
        padding=10,
        width=500,
        height=300,
        auto_scroll=True,
    )

    save_button = ft.Container(
        content=ft.ElevatedButton(
            text="Save",
            width=150,
            height=40,
            color="#000000",
            bgcolor="#2abfbf",
            on_click=save_bill
        ),
        border_radius=ft.border_radius.all(20),
        alignment=ft.alignment.center,
    )

    back_button = ft.Container(
        content=ft.ElevatedButton(
            text="Back",
            width=150,
            height=40,
            color="#000000",
            bgcolor="#2abfbf",
            on_click=go_back
        ),
        border_radius=ft.border_radius.all(20),
        alignment=ft.alignment.center,
    )

    main_container = ft.Container(
        content=ft.Column(
            controls=[
                search_field,
                item_table,
                bill_status_dropdown,
                save_button,
                back_button,
            ],
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        width=550,
        bgcolor="#383838",
        padding=20,
        border_radius=ft.border_radius.all(20),
    )

    page.views.append(
        ft.View(
            "/update_bill",
            bgcolor="#2b3037",
            controls=[
                ft.Column(
                    controls=[
                        ft.Container(content=ft.Text("Update Bill", size=30, weight=ft.FontWeight.BOLD), alignment=ft.alignment.center),
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
