from flet import *
import sqlite3
from assets.styles import FW, GST

class Billing(UserControl):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.listview = ListView()
        self.error = ""
        self.cart_items = []
        self.cart = []

    Prod = TextField(
        hint_text="Enter Product Name",
        text_align="center",
        autofocus=True,
        bgcolor=colors.BLACK,
        border_color=FW,
    )

    def build(self):
        def close_add_dlg(e):
            add_dlg.open = False
            self.page.update()

        def close_gen_dlg(e):
            self.cart_items.pop()
            self.cart_items.pop()
            self.cart_items.pop()
            gen_dlg.open = False
            self.page.go('/Home')
            self.page.update()

        def handleAddItem(e):
            con = sqlite3.connect("sql.db")
            cur = con.cursor()
            res = cur.execute(
                f"""SELECT name,price FROM Menu where name = "{self.Prod.value}" """
            )
            prod = res.fetchone()
            if prod:
                self.listview.controls.append(
                    ListTile(title=Text(prod[0], color=FW), trailing=Text(prod[1]))
                )
                self.cart_items.append(
                    ListTile(title=Text(prod[0], color=FW), trailing=Text(prod[1]))
                )
                self.cart.append(prod)
                self.listview.update()
                close_add_dlg(e)
            else:
                self.error = "No Item Found Try again"
                add_dlg.content.controls[0].update()
                self.page.update()

        def open_add_dlg_modal(e):
            self.Prod.value=''
            self.page.dialog = add_dlg
            add_dlg.open = True
            self.page.update()

        def open_gen_dlg_modal(e):
            global GST
            
            bill = 0
            for i in self.cart:
                bill += int(i[1])
            gst_bill = bill + (bill * GST)

            self.cart_items.append(Text(f"Total bill: {bill}"))
            self.cart_items.append(Text(f"GST: {GST}"))
            self.cart_items.append(Text(f"Total bill After GST: {gst_bill}"))
            
            self.page.dialog = gen_dlg
            gen_dlg.open = True
            self.page.update()

        add_dlg = AlertDialog(
            modal=True,
            title=Text("Enter Name Of Item", color=FW),
            content=Column([Text(self.error, color='red'), self.Prod]),
            actions=[
                ElevatedButton("Add", on_click=handleAddItem, color=FW),
                ElevatedButton("Cancel", on_click=close_add_dlg),
            ],
            actions_alignment=MainAxisAlignment.END,
        )

        gen_dlg = AlertDialog(
            modal=True,
            title=Text("Bill generated", color=FW),
            content=Column(self.cart_items),
            actions=[
                ElevatedButton("Back", on_click=close_gen_dlg),
            ],
            actions_alignment=MainAxisAlignment.END,
        )

        self.container = Container(
            Column(
                alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    Row(
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ElevatedButton(
                                on_click=open_add_dlg_modal,
                                text="Add Item",
                                bgcolor=FW,
                                color="black",
                            ),
                            ElevatedButton(
                                on_click=open_gen_dlg_modal,
                                text="Generate Bill",
                                bgcolor=FW,
                                color="black",
                            ),
                        ],
                    ),
                    self.listview,
                    ElevatedButton("Home", on_click=lambda _: self.page.go("/Home")),
                ],
            ),
        )
        return self.container
