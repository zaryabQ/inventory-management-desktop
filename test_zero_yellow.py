import flet as ft
from screens.theme import ZeroYellowTheme, zero_yellow_container, zero_yellow_button, zero_yellow_text_field, zero_yellow_text, configure_zero_yellow_page

def main(page: ft.Page):
    page.title = "Zero Yellow Test"
    page = configure_zero_yellow_page(page)
    
    # Create a simple form with zero yellow components
    content = zero_yellow_container(
        content=ft.Column([
            zero_yellow_text("Zero Yellow Test", size=20, weight=ft.FontWeight.BOLD),
            zero_yellow_text_field(label="Test Field", hint_text="Enter text"),
            zero_yellow_button("Test Button", on_click=lambda e: print("Button clicked")),
        ])
    )
    
    page.add(content)

if __name__ == "__main__":
    ft.app(target=main) 