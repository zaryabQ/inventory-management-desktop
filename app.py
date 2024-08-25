
from flet import *
from screens.login import Login
from screens.home import Home
from screens.menu import Inventory
from screens.billing import Billing
from screens.setting import Setting

def views_handler(page: Page):
    return {
        "/": View(
            route="/",
            horizontal_alignment="center",
            vertical_alignment="center",
            bgcolor="#101010",
            scroll=True,
            controls=[Login(page)],
        ),
        "/Home": View(
            route="/Home",
            horizontal_alignment="center",
            vertical_alignment="center",
            bgcolor="#101010",
            scroll=False,
            controls=[Home(page)],
        ),
        "/Menu": View(
            route="/Menu",
            horizontal_alignment="center",
            vertical_alignment="center",
            bgcolor="#101010",
            scroll=True,
            controls=[Inventory(page)],
        ),
        "/Billing": View(
            route="/Billing",
            horizontal_alignment="center",
            vertical_alignment="center",
            bgcolor="#101010",
            scroll=True,
            controls=[Billing(page)],
        ),
        "/Setting": View(
            route="/Setting",
            horizontal_alignment="center",
            vertical_alignment="center",
            bgcolor="#101010",
            scroll=True,
            controls=[Setting(page)],
        ),
    }

def main(page: Page):
    page.title = "INVENTORY SYSTEM"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.bgcolor = "#101010"
    page.update()
    page.views.append(views_handler(page)["/"])

    def route_change(route):
        page.views.clear()
        page.views.append(views_handler(page)[page.route])

    page.on_route_change = route_change
    page.go(page.route)

app(target=main)
