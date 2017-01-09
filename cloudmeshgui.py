# coding=UTF-8
import Tkinter as tk
import ttk as ttk
import tkFileDialog
from PIL import Image,ImageTk
from stlOper import FileOperation
import subprocess
from FileList import FileList
from tkMessageBox import *

import os

from plugin.config import global_vars
from plugin.gui.tk_elements import GuiMenu

#pages
from plugin.gui.pages import StartPage, ConfigPage, STLPage


class App(tk.Tk):

    fileOperation = FileOperation()
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self,default=global_vars.icon)
        tk.Tk.wm_title(self,global_vars.title)

        container = tk.Frame(self)

        container.pack(side="top",fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.menu_main = GuiMenu(container)

       # menu = tk.Menu(self)
        self.config(menu=self.menu_main.get_main_menu())

        # file = tk.Menu(menu)
        # file.add_command(label="Open")
        # file.add_command(label="Exit")
        #
        # help = tk.Menu(menu)
        # help.add_command(label="Help")
        #
        # menu.add_cascade(label="File", menu=file)
        # menu.add_cascade(label="Help", menu=help)

        self.frames = {}

        for F in (StartPage, ConfigPage, STLPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def quit(self):
        tk.Tk.destroy()




def run_gui():
    app = App()
    app.minsize(width=global_vars.window_width, height=global_vars.window_height)
    app.mainloop()

if __name__ == "__main__":
    print "RUNNING IN DEBUG MODE!"
    global_vars.dump_vars()
    run_gui()