from flet import *
# from screens.login import build_login
# from screens.home import build_home
# from screens.inventory import build_inventory
# from screens.billing import build_billing
# from screens.setting import build_setting
from assets.views import views_handler

def main(page: Page):
    page.title = "INVENTORY SYSTEM"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.bgcolor = "#101010"
    page.update()

   # Add the initial view to the page
    initial_route = "/"
    page.views.append(views_handler(page)[initial_route])
    print(page.views)

    def route_change(route):
        page.views.clear()  # Clear the views to avoid stacking
        page.views.append(views_handler(page)[page.route])

   # Handle route changes
    page.on_route_change = route_change

    # Ensure that the application exits when the window is closed
    def on_window_close(e):
        print("Window is closing...")  # Debugging message
        page.window_close()

    # Attach the window close handler
    page.on_close = on_window_close

    # Navigate to the initial route
    page.go("/Home")
    print(page.route)

app(target=main)
