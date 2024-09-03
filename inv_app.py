import flet as ft
from flet import *
from view_handler import views_handler


def main(page:Page) ->None:
    page.title = "Flet Inventory App"
    page.horizontal_alignment = MainAxisAlignment.CENTER
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.window.width = page.window.width
    page.window.height = page.window.height
    page.bgcolor = "#101010"
    page.update()

    def route_change(e: RouteChangeEvent) -> None:
        page.views.clear()
        route = views_handler(page)
        #print(route)
        if page.route in route:
            page.views.append(route[page.route])
        page.update()


    page.on_route_change = route_change
    page.views.append(views_handler(page)["/Home"])
    page.update()
    
   

app(target=main)