
import Tkinter as tk

class GuiMenu():
    instance = None

    def __init__(self,parent):

        self.main_menu = tk.Menu(parent)
        self.menus = {}

    def init_menus(self):

        file_menu = tk.Menu(self.main_menu)
        file_menu.add_command(label="Open")
        file_menu.add_command(label="Exit")

        help_menu = tk.Menu(self.main_menu)
        help_menu.add_command(label="Help")

        self.main_menu.add_cascade(label="File" , menu=file_menu)
        self.main_menu.add_cascade(label="Help" , menu=help)



    def get_main_menu(self):
        return self.main_menu

