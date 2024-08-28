import flet as ft

def main(page: ft.Page):
    page.title = "Search Item"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START  # Align content to the top
    page.bgcolor = "#383838"  # Dark background color

    # Function to navigate to the Billing page
    def go_to_billing(e):
        page.go("/Bill_Gene")

    # Search field
    search_field = ft.TextField(
        hint_text="Search Item",
        width=300,
        height=50,
        bgcolor=ft.colors.WHITE,
        text_align=ft.TextAlign.CENTER,
        border_radius=ft.border_radius.all(25),  # Rounded corners
    )

    # Confirm button
    confirm_button = ft.ElevatedButton(
        text="Confirm",
        width=110,
        bgcolor="#2abfbf",
        color="#000000",
        on_click=go_to_billing  # When clicked, go to the billing page
    )

    # Column containing the search field and confirm button
    content_column = ft.Column(
        controls=[
            search_field,
            confirm_button
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    # Container to add padding from the top
    search_field_container = ft.Container(
        content=content_column,
        padding=ft.padding.only(top=100)
    )

    page.add(search_field_container)

ft.app(target=main)
