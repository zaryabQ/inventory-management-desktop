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
