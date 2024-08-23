from pprint import pprint
from flet import *

from under_development import Under

import sqlite3
con = sqlite3.connect('sql.db',check_same_thread=False)
cur = con.cursor()

BG = "#000000"
FW = "#ffffff"
GST = 0.15


# Login page
class Login(UserControl):
    def __init__(self, page: Page):
        super().__init__()

        self.page = page

    name = TextField(
        color=colors.WHITE,
        hint_text="Enter Cashiers Name",
        text_align="center",
        autofocus=True,
        # value=name,
        bgcolor=BG,
        border_color=FW,
    )
    password = TextField(
        color=colors.WHITE,
        hint_text="Enter Your Password",
        text_align="center",
        bgcolor=BG,
        border_color=FW,
    )
    greetings = Column()

    # print(self.name.value)

    def build(self):
        def handleLogin(e):
            con = sqlite3.connect("sql.db")
            cur = con.cursor()
            res = cur.execute(
                f'''SELECT * FROM Cashiers where name = "{self.name.value}" AND password = "{self.password.value}"'''
            )
            users = [i for i in res.fetchall()]
            # print(users)
            if users == []:
                print("Error!")
            else:
                # con.close()
                self.page.go("/Home")

        self.container = Container(
            content=Column(
                controls=[
                    Container(
                        content=Text(
                            value="Welcome to Cashier App", size=25, color="#ffffff"
                        ),
                        alignment=alignment.center,
                    ),
                    Container(
                        content=Text(
                            value="Login to your account",
                            size=20,
                            color="#ffffff",
                        ),
                        alignment=alignment.center_left,
                        margin=margin.symmetric(40),
                    ),
                    Container(content=self.name),
                    Container(content=self.password),
                    Row(
                        alignment="center",
                        controls=[
                            Container(
                                ElevatedButton(
                                    on_click=handleLogin,
                                    text="Login",
                                    bgcolor=FW,
                                    color="black",
                                ),
                            ),
                        ],
                    ),
                    self.greetings,
                ],
            ),
            height=500,
            width=700,
            bgcolor=BG,
            padding=25,
            border_radius=50,
        )

        return self.container


# Menu page
class Menu(UserControl):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        con = sqlite3.connect("sql.db")
        cur = con.cursor()
        res = cur.execute("SELECT * FROM Menu")
        self.menu = [i for i in res.fetchall()]
        # print(self.menu)

    def build(self):
        self.container = ListView(
            # alignment=alignment.center,
            controls=[
                Container(
                    content=Row(
                        [
                            Container(
                                Text(value="Welcome To Menu", color="#FCC8D1", size=50)
                            ),
                            Container(
                                ElevatedButton(
                                    "Back", on_click=lambda _: self.page.go("/Home")
                                )
                            ),
                        ],
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ),
                DataTable(
                    columns=[
                        DataColumn(Text("Name", color=colors.BLUE)),
                        DataColumn(Text("Price", color=colors.BLUE)),
                    ],
                    rows=[
                        DataRow(
                            cells=[
                                DataCell(Text(i[0], color=colors.WHITE)),
                                DataCell(Text(i[1], color=colors.WHITE)),
                            ]
                        )
                        for i in self.menu
                    ],
                ),
            ],
        )
        return self.container


# Home page
class Home(UserControl):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page

    def build(self):
        self.container = Container(
            Column(
                alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    Container(
                        content=Text(value="Welcome To Icecream Alley", color="#FCC8D1", size=50),
                    ),
                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        vertical_alignment=CrossAxisAlignment.CENTER,
                        expand=1,
                        controls=[
                            ElevatedButton(
                                on_click=lambda _: self.page.go("/Menu"),
                                text="Menu",
                                bgcolor="#FAB3A9",
                                color="red",
                                width=200,
                                height=100,
                            ),
                            ElevatedButton(
                                on_click=lambda _: self.page.go("/Billing"),
                                text="Billing",
                                bgcolor="#FAB3A9",
                                color="red",
                                width=200,
                                height=100,
                            ),
                            ElevatedButton(
                                on_click=lambda _: self.page.go("/Setting"),
                                text="Settings",
                                bgcolor="#FAB3A9",
                                color="red",
                                width=200,
                                height=100,
                            ),
                        ],
                    ),
                ],
            ),
            height=600,
            width=700,
            padding=25,
            border_radius=50,
        )
        return self.container


# Billing page
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
            # self.cart_items = []
            self.cart_items.pop()
            self.cart_items.pop()
            self.cart_items.pop()
            gen_dlg.open = False
            self.page.go('/Home')
            self.page.update()

        def handleAddItem(e):
            print("add")
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
            title=Text("Add A Item"),
            content=Column([Text(self.error), self.Prod]),
            actions=[
                TextButton("Add", on_click=lambda _:handleAddItem(_)),
                TextButton("Close", on_click=close_add_dlg),
            ],
            actions_alignment=MainAxisAlignment.END,
        )
        gen_dlg = AlertDialog(
            modal=True,
            title=Text("Bill"),
            content=ListView(self.cart_items),
            actions=[
                TextButton("Close", on_click=close_gen_dlg),
            ],
            actions_alignment=MainAxisAlignment.END,
            # on_dismiss=lambda e: print(e),
        )

        self.billingpage = Column(
            [
                Container(
                    content=Text(value="Billing", color="#FCC8D1", size=50),
                ),
                Row(
                    [
                        Row(
                            [
                                ElevatedButton("Add Item", on_click=open_add_dlg_modal),
                                Container(
                                    ElevatedButton(
                                        "Generate Bill",
                                        on_click=open_gen_dlg_modal,
                                    ),
                                ),
                            ]
                        ),
                        Container(
                            ElevatedButton(
                                "Back", on_click=lambda _: self.page.go("/Home")
                            ),
                        ),
                    ],
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    spacing=20,
                ),
                Container(self.listview,width=900),
            ],
            alignment=MainAxisAlignment.START,
            horizontal_alignment=CrossAxisAlignment.START
        )
        return self.billingpage


# Setting page
class Setting(UserControl):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.error = ""

    def build(self):
        t = Text()
        c = Column(
            [],
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER,
        )
        price = TextField(
            hint_text="Enter Price",
            text_align="center",
            autofocus=True,
            bgcolor=BG,
            border_color=FW,
        )
        name = TextField(
            hint_text="Enter Product Name",
            text_align="center",
            autofocus=True,
            bgcolor=BG,
            border_color=FW,
        )
        gst = TextField(
            hint_text="Enter New GST rate without %",
            text_align="center",
            autofocus=True,
            bgcolor=BG,
            border_color=FW,
        )

        def Add_Item():
            cur.execute(f"Insert into Menu values ('{name.value}',{price.value})")  
            con.commit()

        add_item = [
            name,
            price,
            ElevatedButton(
                "Add Item",
                on_click=lambda _: Add_Item(),
            ),
            
        ]

        def Delete_Item():
            cur.execute(f'''
                Delete from Menu   
                WHERE name= "{name.value}"
                ''')

            con.commit()

        delete_item = [
            name,
            ElevatedButton(
                "Delete Item",
                on_click=lambda _: Delete_Item(),
            ),
        ]

        def Update_Item():
            cur.execute(f'''
                UPDATE Menu   
                SET price = {price.value}
                WHERE name= "{name.value}"
                ''')

            con.commit()
                                                                   
        update_item = [
            name,
            price,
            ElevatedButton(
                "Update Item",
                on_click=lambda _: Update_Item(),
            ),
        ]

        def GST_Update():
            global GST
            GST = float(gst.value)
            print(GST)
            

        gst_update = [
            gst,
            ElevatedButton(
                "Update GST",
                on_click=lambda _: GST_Update(),
            ),
        ]

        def radiogroup_changed(e):
            screens = {
                "updateProd": update_item,
                "deleteProd": delete_item,
                "addProd": add_item,
                "updateGST": gst_update,
            }
            c.controls = screens[e.control.value]
            c.update()

        self.settings = Column(
            [
                ElevatedButton(
                                "Back", on_click=lambda _: self.page.go("/Home")
                            ),
                RadioGroup(
                    content=Column(
                        [
                            Radio(value="updateProd", label="Update Product Price"),
                            Radio(value="deleteProd", label="Delete A Product"),
                            Radio(value="addProd", label="Add A Product"),
                            Radio(value="updateGST", label="Update GST"),
                        ]
                    ),
                    on_change=radiogroup_changed,
                ),
                Container(c, padding=90),
            ]
            
        )
        # self.page.add(Text("Select your favorite color:"), cg, t)
        return self.settings


# Receipt page
class Receipt(UserControl):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        pprint(page.data)
        self.error = ""

    def build(self):
        self.billingpage = Row(
            [
                Container(
                    content=Text(value="Receipt", color="#FCC8D1", size=50),
                ),
                ElevatedButton("Back", on_click=lambda _: self.page.go("/Billing")),
            ],
            alignment=MainAxisAlignment.SPACE_BETWEEN,
        )
        return self.billingpage


# All pages handler
def views_handler(page):
    return {
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
            controls=[Menu(page)],
        ),
        "/": View(
            route="/",
            horizontal_alignment="center",
            vertical_alignment="center",
            bgcolor="#101010",
            scroll=True,
            controls=[Login(page)],
        ),
        "/under": View(
            route="/under",
            horizontal_alignment="center",
            vertical_alignment="center",
            bgcolor="#101010",
            scroll=True,
            controls=[Under(page)],
        ),
        "/Billing": View(
            route="/Billing",
            horizontal_alignment="center",
            vertical_alignment="center",
            bgcolor="#101010",
            scroll=True,
            controls=[Billing(page)],
        ),
        "/Receipt": View(
            route="/Receipt",
            horizontal_alignment="center",
            vertical_alignment="center",
            bgcolor="#101010",
            scroll=True,
            controls=[Receipt(page)],
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
