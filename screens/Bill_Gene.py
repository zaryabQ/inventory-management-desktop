import flet as ft

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
        size=36,
        weight=ft.FontWeight.W_900,
        color="#26A69A",
        text_align=ft.TextAlign.CENTER,
        italic=True,
    )

    items = []

    def update_item(e, item):
        print(f"Update item: {item.value}")

    def remove_item(e, item_id):
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
            
            # Simulated search in a list of items (Replace with your actual inventory)
            inventory = [
                {"id": 1, "name": "Item 1", "price": 100},
                {"id": 2, "name": "Item 2", "price": 200},
                {"id": 3, "name": "Item 3", "price": 300},
            ]
            
            for item in inventory:
                if search_query in item["name"].lower():
                    results.controls.append(
                        ft.ListTile(
                            title=ft.Text(item["name"]),
                            subtitle=ft.Text(f"Price: {item['price']}"),
                            on_click=lambda e, item=item: on_item_selected(item),
                        )
                    )
            
            page.update()
        
        search_field = ft.TextField(
            label="Search Items",
            on_change=search_item,
            width=300,
        )
        
        results = ft.Column()
        
        popup = ft.AlertDialog(
        modal=True,
        title=ft.Text("Search Items", color="#26A69A"),  # Heading color
        content=ft.Column([
            ft.TextField(
                # Assuming this is your search_field
                label="Search",
                bgcolor="white",  # Background color of the TextField
                color="black",    # Text color inside the TextField
            ),
            results
        ]),
        actions=[
            ft.TextButton(
                "Close",
                on_click=lambda e: [setattr(popup, 'open', False), popup.update()],
                style=ft.ButtonStyle(
                    bgcolor="#2abfbf",
                    color="#000000",
                ),
            )
        ],
        bgcolor="#383838",  # Background color of the AlertDialog
    )

     
        page.dialog = popup
        popup.open = True
        page.update()

    def add_item(e):
        def on_item_selected(item):
            item_name = ft.Text(item["name"], width=150, color="#000000", text_align=ft.TextAlign.CENTER)
            item_price = ft.Text(str(item["price"]), width=100, color="#000000", text_align=ft.TextAlign.CENTER)

            item_id = len(items)
            
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
            update_item_table()
            page.dialog.open = False
            page.update()

        show_search_popup(page, on_item_selected)

    def save_item(e):
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

    main_container = ft.Container(
        content=ft.Column(
            controls=[
                input_field,
                add_items_button,
                item_table,
                save_button,
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

