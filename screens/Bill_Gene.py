import flet as ft

def main(page: ft.Page):
    global items
    # Set the custom scrollbar theme
    page.theme = ft.Theme(
        scrollbar_theme=ft.ScrollbarTheme(
            track_color={
                ft.MaterialState.HOVERED: "#D3D3D3",  
                ft.MaterialState.DEFAULT: "#FFFFFF",  # White background normally
            },
            track_visibility=True,
            track_border_color="#D3D3D3",            # Light grey border for the track
            thumb_visibility=True,
            thumb_color={
                ft.MaterialState.HOVERED: "#A9A9A9",  # Dark grey thumb on hover (hex for dark grey)
                ft.MaterialState.DEFAULT: "#696969",  # Dark grey thumb normally (slightly darker)
            },
            thickness=10,  # Scrollbar width
            radius=10,     # Scrollbar corner radius
            main_axis_margin=50,  # Margin from the main axis
            cross_axis_margin=10,  # Margin from the cross axis
        )
    )



    page.title = "Generate Bill"
    page.bgcolor = "#263238"

    # Stylish Heading
    heading = ft.Text(
        "Generate Bill",
        size=36,
        weight=ft.FontWeight.W_900,
        color="#26A69A",
        text_align=ft.TextAlign.CENTER,
        italic=True,
    )

    # Placeholder for item rows
    items = []

    def add_item(e):
        # When the "Add Items" button is clicked, a new row is added to the item_table
        item_name = ft.Text("New Item", width=150, color="#000000", text_align=ft.TextAlign.CENTER)
        item_price = ft.Text("0", width=100, color="#000000", text_align=ft.TextAlign.CENTER)

        # Create a unique ID for each item
        item_id = len(items)
        # Add new row to items list
        items.append(
            {
                "id": item_id,
                "container": ft.Container(
                    content=ft.Row(
                        controls=[
                            item_name,
                            item_price,
                            ft.IconButton(
                                icon=ft.icons.CHANGE_CIRCLE_OUTLINED,
                                icon_color="#000000",
                                tooltip="Update",
                                on_click=lambda e, item=item_name: update_item(e, item)
                            ),
                            ft.IconButton(
                                icon=ft.icons.DELETE_OUTLINE_ROUNDED,
                                icon_color="#000000",
                                tooltip="Delete",
                                on_click=lambda e, item_id=item_id: remove_item(e, item_id)
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
            }
        )
        # Update the UI
        update_item_table()

    def update_item(e, item):
        print(f"Update item: {item.value}")

    def remove_item(e, item_id):
        global items  # Access the global items list
        # Find and remove the item by its ID
        items = [item for item in items if item["id"] != item_id]
        # Update the UI
        update_item_table()

    def update_item_table():
        item_table.controls.clear()
        for item in items:
            item_table.controls.append(item["container"])
        page.update()

    # Input field
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

    # Add Items button wrapped in Container for border radius
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

    # Table of items using ListView
    item_table = ft.ListView(
        controls=[],  # Initially empty, rows will be added dynamically
        spacing=5,
        padding=10,
        width=500,  # Increased width for scrollbar adjustment
        height=300,  # Increased height to accommodate more items
        auto_scroll=True,
    )

    # Save button wrapped in Container for border radius
    save_button = ft.Container(
        content=ft.ElevatedButton(
            text="Save",
            width=150,
            height=40,
            color="#000000",
            bgcolor="#2abfbf",
        ),
        border_radius=ft.border_radius.all(20),
        alignment=ft.alignment.center,
    )

    # Main container (wider to accommodate scrollbar)
    main_container = ft.Container(
        content=ft.Column(
            controls=[
                input_field,
                add_items_button,
                item_table,  # Use ListView for items with scrolling
                save_button,  # Save button stays at the bottom and moves down with more items
            ],
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        width=550,  # Increased width to provide extra space
        bgcolor="#383838",
        padding=20,
        border_radius=ft.border_radius.all(20),
    )

    # Page layout
    page.add(
        ft.Column(
            controls=[
                ft.Container(content=heading, alignment=ft.alignment.center),
                ft.Container(content=main_container, alignment=ft.alignment.center),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=30,
        )
    )

ft.app(target=main)
