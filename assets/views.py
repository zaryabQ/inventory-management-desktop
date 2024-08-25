from flet import *
from screens.login import build_login
from screens.home import build_home
from screens.inventory import build_inventory
from screens.billing import build_billing
from screens.setting import build_setting

def views_handler(page: Page):
    return {
        "/": View(
            route="/",
            horizontal_alignment="center",
            vertical_alignment="center",
            bgcolor="#101010",
            scroll=True,
            controls=[build_login(page)],
        ),
        "/Home": View(
            route="/Home",
            horizontal_alignment="center",
            vertical_alignment="center",
            bgcolor="#101010",
            scroll=False,
            controls=[build_home(page)],
        ),
        "/Inventory": View(
            route="/Inventory",
            horizontal_alignment="center",
            vertical_alignment="center",
            bgcolor="#101010",
            scroll=True,
            controls=[build_inventory(page)],
        ),
        "/Billing": View(
            route="/Billing",
            horizontal_alignment="center",
            vertical_alignment="center",
            bgcolor="#101010",
            scroll=True,
            controls=[build_billing(page)],
        ),
        "/Setting": View(
            route="/Setting",
            horizontal_alignment="center",
            vertical_alignment="center",
            bgcolor="#101010",
            scroll=True,
            controls=[build_setting(page)],
        ),
    }
