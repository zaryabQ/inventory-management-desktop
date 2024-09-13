import flet as ft
from flet import *
from view_handler import views_handler
from screens.user import User
import asyncio

def main(page:Page) ->None:
    page.title = "Flet Inventory App"
    page.horizontal_alignment = MainAxisAlignment.CENTER
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.window.width = page.window.width
    page.window.height = page.window.height
    page.bgcolor = "#101010"
    page.update()

    async def show_splash_screen():
        # Create the splash screen image container
        splash_screen = Container(
            content=Image(
                src="png/SKYLINK.png",
                fit=ImageFit.CONTAIN,
                expand=True  # Expands to fill the available space
            ),
            alignment=alignment.center,
            expand=True,  # Expands the container to the available window space
            bgcolor=colors.BLACK,  # Set the background color of the splash screen
        )

        # Add the splash screen to the page
        page.add(splash_screen)
        page.update()

        # Adjust the width and height of the image based on the window size
        def resize_image(e):
            splash_screen.content.width = page.window_width * 0.7  # 60% of window width
            splash_screen.content.height = page.window_height * 0.7  # 60% of window height
            page.update()

        # Bind the resize event to dynamically adjust the image size
        page.on_resize = resize_image

        # Call resize function initially to set the image size on page load
        resize_image(None)


        # Asynchronously wait for 3 seconds before transitioning to the login screen
        await asyncio.sleep(3)
        page.controls.clear()  # Clear the splash screen
        route_change(None)  # Call route_change to load the initial view
        page.update()

    def route_change(e: RouteChangeEvent) -> None:
        page.views.clear()
        route = views_handler(page)
        if page.route in route:
            page.views.append(route[page.route])
        page.update()

    page.on_route_change = route_change

    # Start with splash screen and then move to the initial view
    asyncio.run(show_splash_screen())

ft.app(target=main)
