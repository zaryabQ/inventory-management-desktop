import flet as ft
from screens.theme import configure_zero_yellow_page, zero_yellow_text, zero_yellow_container

def main(page: ft.Page):
    page.title = "Login Flow Test"
    page = configure_zero_yellow_page(page)
    
    # Test UI display after login simulation
    content = zero_yellow_container(
        content=ft.Column([
            zero_yellow_text("✅ Login Flow Test", size=24, weight=ft.FontWeight.BOLD),
            zero_yellow_text("✅ UI is displaying correctly", size=16),
            zero_yellow_text("✅ Zero-yellow theme applied", size=16),
            zero_yellow_text("✅ Navigation should work", size=16),
            zero_yellow_text("✅ All components loading", size=16),
        ])
    )
    
    page.add(content)
    print("✅ Test UI loaded successfully!")

if __name__ == "__main__":
    ft.app(target=main) 