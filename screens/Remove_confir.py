import flet as ft

def main(page: ft.Page):
    # Setting the background color for the entire page
    page.bgcolor = "#383838"

    # Creating the text at the center
    confirmation_text = ft.Text(
        "Are you sure you want to remove the Item",
        color="red",
        size=24,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER
    )

    # Wrapping the text inside a container to center it
    text_container = ft.Container(
        content=confirmation_text,
        alignment=ft.alignment.center,
        padding=ft.padding.only(top=150)
    )

    # Creating the confirmation buttons
    remove_button = ft.IconButton(
        icon=ft.icons.CLOSE,
        icon_color="white",
        bgcolor="teal",
        on_click=lambda e: print("Item removal cancelled"),
        width=70,
        height=70,
        icon_size=40
    )

    confirm_button = ft.IconButton(
        icon=ft.icons.CHECK,
        icon_color="white",
        bgcolor="teal",
        on_click=lambda e: print("Item removed"),
        width=70,
        height=70,
        icon_size=40
    )

    # Aligning the buttons in a row and using a container for padding
    buttons_row = ft.Row(
        [remove_button, confirm_button],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=50  # Increase spacing between the buttons
    )

    # Wrapping the buttons row in a container to add padding to move it down
    buttons_container = ft.Container(
        content=buttons_row,
        alignment=ft.alignment.center,
        padding=ft.padding.only(top=100)  # Move the buttons down
    )

    # Aligning all components in a vertical column
    content_column = ft.Column(
        [text_container, buttons_container],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=100
    )

    # Adding the content to the page
    page.add(ft.Container(content_column, alignment=ft.alignment.center))

# Running the Flet app
ft.app(target=main)
