import flet as ft
from flet import *
from screens.inv import InventoryScreen
from screens.login import LoginScreen
from screens.home import HomeScreen
from screens.billing import BillingScreen
from screens.settings import SettingsScreen


def views_handler(page: Page):
    return {
        "/": View(
            route="/",
            horizontal_alignment=MainAxisAlignment.CENTER,
            vertical_alignment=MainAxisAlignment.CENTER,
            bgcolor="#101010",
            scroll=False,
            controls=[LoginScreen(page).build()],
        ),
        "/Home": View(
            route="/Home",
            horizontal_alignment=MainAxisAlignment.CENTER,
            vertical_alignment=MainAxisAlignment.CENTER,
            bgcolor="#101010",
            scroll=False,
            controls=[HomeScreen(page).build()],
        ),
        "/Inventory": View(
            route="/Inventory",
            horizontal_alignment=MainAxisAlignment.CENTER,
            vertical_alignment=MainAxisAlignment.CENTER,
            bgcolor="#101010",
            scroll=False,
            controls=[InventoryScreen(page).build()],
        ),
        "/Billing": View(
            route="/Billing",
            horizontal_alignment="center",
            vertical_alignment="center",
            bgcolor="#101010",
            scroll=False,
            controls=[BillingScreen(page).build()],
        ),
        "/Settings": View(
            route="/Settings",
            horizontal_alignment="center",
            vertical_alignment="center",
            bgcolor="#101010",
            scroll=False,
            controls=[SettingsScreen(page).build()],
        )   
    }