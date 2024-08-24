from flet import *
import sqlite3
from assets.styles import FW

class Menu(UserControl):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        con = sqlite3.connect("db/sql.db")
        cur = con.cursor()
        res = cur.execute("SELECT * FROM Menu")
        self.menu = [i for i in res.fetchall()]

    def build(self):
        self.container = ListView(
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
