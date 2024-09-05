import flet as ft

def bill_gen(page):

    global items, filtered_items
    page.title = "Update Bill"
    page.bgcolor = "#263238"

    heading = ft.Text(
            "Update Bill",
            size=30,
            weight=ft.FontWeight.BOLD,
            color='#26A69A',
            font_family="Arial",
            italic=True
    )

    # Example items
    items = [
        {"id": 1, "name": "Item 1", "quantity": 2, "price": 50.0, "status": "Paid"},
        {"id": 2, "name": "Item 2", "quantity": 1, "price": 75.0, "status": "Unpaid"},
        {"id": 3, "name": "Item 3", "quantity": 3, "price": 20.0, "status": "Return"}
    ]

    filtered_items = items.copy()

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
                ft.Dropdown(
                    label="Payment Status",
                    options=[
                        ft.dropdown.Option("Paid"),
                        ft.dropdown.Option("Unpaid"),
                        ft.dropdown.Option("Return"),
                    ],
                    bgcolor="#FFFFFF",
                    color="#000000",
                ),
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
        status = content.controls[2].value  # Get the value of the dropdown

        # Update the item's data
        item['quantity'] = quantity
        item['price'] = price
        item['status'] = status  # Store the status as well

        # Update the item's container in the list
        item["container"] = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text(item["name"], width=150, color="#000000", text_align=ft.TextAlign.CENTER),
                    ft.Text(str(item["quantity"]), width=50, color="#000000", text_align=ft.TextAlign.CENTER),
                    ft.Text(str(item["price"]), width=100, color="#000000", text_align=ft.TextAlign.CENTER),
                    ft.Text(item["status"], width=100, color="#000000", text_align=ft.TextAlign.CENTER),
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
        for item in filtered_items:
            item["container"] = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Text(item["name"], width=150, color="#000000", text_align=ft.TextAlign.CENTER),
                        ft.Text(str(item["quantity"]), width=50, color="#000000", text_align=ft.TextAlign.CENTER),
                        ft.Text(str(item["price"]), width=100, color="#000000", text_align=ft.TextAlign.CENTER),
                        ft.Text(item["status"], width=100, color="#000000", text_align=ft.TextAlign.CENTER),
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

    def search_items(e):
        global filtered_items
        query = e.control.value.lower()
        filtered_items = [item for item in items if query in item["name"].lower() or query in str(item["id"])]
        update_item_table()

    def save_item(e):
        # Implement save logic here
        page.views.pop()
        page.update()

    def go_back(e):
        page.views.pop()
        page.update()

    search_field = ft.Container(
        width=300,
        height=45,
        content=ft.TextField(
            label="Enter Name/ID",
            bgcolor="#FFFFFF",
            color="#000000",
            border_radius=ft.border_radius.all(8),
            height=50,
            text_align=ft.TextAlign.CENTER,
            on_change=search_items,
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
                search_field,
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
                "/update_bill",
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

    # Update the item table initially
    update_item_table()

    page.update()


def main():
    ft.app(target=bill_gen)

if __name__ == "__main__":
    main()
