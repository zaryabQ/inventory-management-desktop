import flet as ft
import sqlite3
from db.billing_handler import BillingHandler
from db.inv_handler import InventoryHandler  # Assuming this is the correct import for database operations

def bill_gen(page):
    global items
    page.theme = ft.Theme(
        scrollbar_theme=ft.ScrollbarTheme(
            track_color={
                ft.MaterialState.HOVERED: "#D3D3D3",
                ft.MaterialState.DEFAULT: "#FFFFFF",
            },
            track_visibility=True,
            track_border_color="#D3D3D3",
            thumb_visibility=True,
            thumb_color={
                ft.MaterialState.HOVERED: "#A9A9A9",
                ft.MaterialState.DEFAULT: "#696969",
            },
            thickness=10,
            radius=10,
            main_axis_margin=50,
            cross_axis_margin=10,
        )
    )
    page.title = "Generate Bill"
    page.bgcolor = "#263238"

    heading = ft.Text(
        "Generate Bill",
        size=30,
        weight=ft.FontWeight.BOLD,
        color='#26A69A',
        font_family="Arial",
        italic=True
    )

    items = []

    def update_item(e, item_id):
        item = next((i for i in items if i["id"] == item_id), None)
        if not item:
            return

        popup = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Update {item['name']}", color="#26A69A"),
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
                    on_click=lambda e: [remove_item(item_id), setattr(popup, 'open', False)],
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

        # Update the item's quantity and price in the bill
        item['quantity'] = quantity
        item['price'] = price

        # Update the item's container in the list to reflect new values
        item["container"] = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text(item["name"], width=150, color="#000000", text_align=ft.TextAlign.CENTER),
                    ft.Text(str(item["quantity"]), width=50, color="#000000", text_align=ft.TextAlign.CENTER),  # Updated quantity
                    ft.Text(str(item["price"]), width=100, color="#000000", text_align=ft.TextAlign.CENTER),    # Updated price
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

        # Update the item table to reflect the changes
        update_item_table()


    def remove_item(item_id):
        global items
        items = [item for item in items if item["id"] != item_id]
        update_item_table()

    def update_item_table():
        item_table.controls.clear()
        for item in items:
            item_table.controls.append(item["container"])
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
                        title=ft.Text(item_data["name"]),
                        subtitle=ft.Text(f"Quantity: {item_data['quantity']}\nPrice: {item_data['price']}"),
                        on_click=lambda e, item=item_data: on_item_selected(item),
                        bgcolor="#FFFFFF",
                    )
                )

            page.update()

        search_field = ft.TextField(
            label="Search Items",
            on_change=search_item,
            width=300,
            bgcolor="#FFFFFF",
        )

        results = ft.Column()

        popup = ft.AlertDialog(
            modal=True,
            title=ft.Text("Search Items", color="#26A69A"),
            content=ft.Column([
                search_field,
                results
            ]),
            actions=[
                ft.TextButton(
                    "Close",
                    on_click=lambda e: [setattr(popup, 'open', False), popup.update()],
                    style=ft.ButtonStyle(bgcolor="#2abfbf", color="#000000"),
                ),
            ],
            bgcolor="#383838",
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
                                ft.Text(item["name"], width=150, color="#000000", text_align=ft.TextAlign.CENTER),
                                ft.Text("1", width=50, color="#000000", text_align=ft.TextAlign.CENTER),
                                ft.Text(str(item["price"]), width=100, color="#000000", text_align=ft.TextAlign.CENTER),
                                ft.IconButton(
                                    icon=ft.icons.CHANGE_CIRCLE_OUTLINED,
                                    icon_color="#000000",
                                    tooltip="Update",
                                    on_click=lambda e, item_id=item_id: update_item(e, item_id)  # Use the correct ID
                                ),
                            ],
                            spacing=10,
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        bgcolor="#FFFFFF",
                        padding=ft.padding.all(4),
                        border_radius=ft.border_radius.all(8),
                        margin=ft.margin.symmetric(vertical=3),
                    ),
                }
            )
            update_item_table()
            page.dialog.open = False
            page.update()

        show_search_popup(page, on_item_selected)



    def save_item(e):
        global items

        customer_name = input_field.content.value.strip()

        if not customer_name:
            # Alert the user that the name field is empty
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Name field cannot be empty!"),
                bgcolor="#FF0000"
            )
            page.snack_bar.open = True
            page.update()
            return

        if not items:
            # Alert the user that no items have been added
            page.snack_bar = ft.SnackBar(
                content=ft.Text("No items to bill!"),
                bgcolor="#FF0000"
            )
            page.snack_bar.open = True
            page.update()
            return

        # Prepare the item list for saving (only keep relevant fields: id, name, quantity, price)
        item_list = []
        for item in items:
            # Make sure to include only the required fields, ignoring 'container'
            item_list.append({
                'id': item['id'],          # Assuming each item has an ID
                'name': item['name'],       # Item name
                'quantity': item['quantity'],  # Quantity selected in the UI
                'selling_price': item['price'],  # Selling price set in the UI
            })

        try:
            # Call the add_bill function to save the bill to the database
            BillingHandler.add_bill(customer_name, item_list)

            # Alert the user that the bill was saved successfully
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Bill saved successfully!"),
                bgcolor="#00FF00"
            )
            page.snack_bar.open = True

            # Clear the form for the next bill
            items.clear()
            update_item_table()
            input_field.content.value = "" 
            page.views.pop() # Clear the customer name input
            page.update()

        except ValueError as ve:
            # Alert the user in case of any validation errors (e.g., insufficient stock)
            page.snack_bar = ft.SnackBar(
                content=ft.Text(str(ve)),
                bgcolor="#FF0000"
            )
            page.snack_bar.open = True
            page.update()

        except Exception as e:
            # Handle unexpected errors
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Error: {str(e)}"),
                bgcolor="#FF0000"
            )
            page.snack_bar.open = True
            page.update()

    def go_back(e):
        page.views.pop()
        page.update()

    input_field = ft.Container(
        width=300,
        height=45,
        content=ft.TextField(
            label="Enter Name/ID",
            bgcolor="#FFFFFF",
            color="#000000",
            border_radius=ft.border_radius.all(8),
            height=50,
            text_align=ft.TextAlign.CENTER,
        ),
        bgcolor="#000000",
        border_radius=10,
    )

    add_items_button = ft.Container(
        content=ft.ElevatedButton(
            text="Add Items",
            width=150,
            height=40,
            color="#000000",
            bgcolor="#2abfbf",
            on_click=add_item,
        ),
        border_radius=ft.border_radius.all(20),
        alignment=ft.alignment.center,
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
            on_click=save_item
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
                input_field,
                add_items_button,
                item_table,
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
            "/bill",
            bgcolor="#2b3037",
            controls=[
                ft.Column(
                    controls=[
                        ft.Container(content=heading, alignment=ft.alignment.center),
                        ft.Container(content=main_container, alignment=ft.alignment.center),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=30,
                )
            ]
        )
    )
    page.update()
