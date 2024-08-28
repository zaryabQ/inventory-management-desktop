import flet as ft

def main(page: ft.Page):
    # Set the custom scrollbar theme
    page.theme = ft.Theme(
        scrollbar_theme=ft.ScrollbarTheme(
            track_color={
                ft.MaterialState.HOVERED: ft.colors.AMBER,
                ft.MaterialState.DEFAULT: ft.colors.TRANSPARENT,
            },
            track_visibility=True,
            track_border_color=ft.colors.BLUE,
            thumb_visibility=True,
            thumb_color={
                ft.MaterialState.HOVERED: ft.colors.GREY,
                ft.MaterialState.DEFAULT: ft.colors.GREY_300,
            },
            thickness=10,  # Decreased scrollbar width
            radius=15,
            main_axis_margin=50,  # Increased margin to move scrollbar further right
            cross_axis_margin=10,
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

        # Add new row to items list
        items.append(
            ft.Container(
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
                            on_click=lambda e, id=len(items) - 1: remove_item(e, id)
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
        )
        # Update the UI
        item_table.controls.clear()
        item_table.controls.extend(items)
        page.update()

    def update_item(e, item):
        print(f"Update item: {item.value}")

    def remove_item(e, id):
        # Remove the selected item from the list and update the UI
        items.pop(id)
        item_table.controls.clear()
        item_table.controls.extend(items)
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
        width=420,  # Increased width for scrollbar adjustment
        height=200,  # Set fixed height to enable scrolling
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
        width=520,  # Increased width to provide extra space
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
