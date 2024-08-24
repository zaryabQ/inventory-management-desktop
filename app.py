from flet import *
import flet as ft
from views import views_handler


def main(page: Page):
    def route_change(route):
        page.views.clear()
        page.views.append(views_handler(page)[page.route])

    page.title = "My Cashier App"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.on_route_change = route_change
    page.bgcolor = "#101010"
    page.scroll = True

    page.go("/")


if __name__ == "__main__":
    ft.app(target=main)
