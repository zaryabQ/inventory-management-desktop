import flet as ft
from screens.theme import (
    IOS26Theme, 
    glass_container, 
    primary_button,
    modern_text_field, 
    heading_text, 
    body_text
)

def main(page: ft.Page):
    page.title = "Search Item"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START  # Align content to the top
    page.bgcolor = IOS26Theme.BACKGROUND_PRIMARY

    # Function to navigate to the Billing page
    def go_to_billing(e):
        page.go("/Bill_Gene")

    # Search field
    search_field = modern_text_field(
        hint_text="Search Item",
        width=300,
        height=50,
        text_align=ft.TextAlign.CENTER,
    )

    # Confirm button
    confirm_button = primary_button(
        text="Confirm",
        width=110,
        height=45,
        on_click=go_to_billing  # When clicked, go to the billing page
    )

    # Column containing the search field and confirm button
    content_column = glass_container(
        content=ft.Column(
            controls=[
                heading_text(
                    "Search Items",
                    size=24,
                    color=IOS26Theme.TEXT_PRIMARY
                ),
                Container(height=20),
                search_field,
                Container(height=10),
                confirm_button
            ],
            spacing=15,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        width=400,
        height=300,
        padding=30,
        margin=20
    )

    page.add(content_column)

ft.app(target=main)
