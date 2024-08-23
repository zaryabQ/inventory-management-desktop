from flet import *



class Under(UserControl):

    def __init__(self,page:Page):
        super().__init__()
        self.page = page


    def build(self):
        self.container = Row(
            controls=[
                ElevatedButton(
                              on_click = lambda _: self.page.go("/") ,
                              text="Back", 
                              bgcolor="#FAB3A9",
                              color = "red",    
                          ),
            ]
        )
        return self.container