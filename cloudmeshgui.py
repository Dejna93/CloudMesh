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
from plugin.gui.pages import StartPage, ConfigPage

thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)

LARGE_FONT = ("Verdana", 12)
FILEPATH = ''


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

        for F in (StartPage, PageOne, ConfigPage, STLPage):
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






class STLPage(tk.Frame):

    def __init__(self,parent , controller):
        tk.Frame.__init__(self, parent)

        labelFrame = tk.LabelFrame(self,text="Triangulation options", height=200,padx=10, pady=10)
        labelFrame.grid(row=0 , columnspan=7, sticky='W', padx=5,pady=5, ipadx=5,ipady=5)


        self.maxNearNeigh = tk.DoubleVar()
        self.Mu = tk.DoubleVar()
        self.searchRadius =tk.DoubleVar()
        self.minAngle =tk.DoubleVar()
        self.maxAngle = tk.DoubleVar()
        self.maxSurfAgle = tk.DoubleVar()
        self.normalCons = tk.IntVar()
        #LABELS STL
        label_1 = tk.Label(labelFrame,text="setMaximumNearestNeighbors")
        label_2 = tk.Label(labelFrame, text="setMu")
        label_3 = tk.Label(labelFrame, text="setSearchRadius")
        label_4 = tk.Label(labelFrame, text="setMinimumAngle")
        label_5 = tk.Label(labelFrame, text="setMaximumAngle")
        label_6 = tk.Label(labelFrame, text="setMaximumSurfaceAgle")
        label_7 = tk.Label(labelFrame, text="setNormalConsistency")

        #LOCALISATION
        label_1.grid(row=1,column=0 ,sticky="W")
        label_2.grid(row=2,column=0 ,sticky="W")
        label_3.grid(row=3,column=0 ,sticky="W")
        label_4.grid(row=4, column=0, sticky="W")
        label_5.grid(row=5, column=0, sticky="W")
        label_6.grid(row=6, column=0, sticky="W")
        label_7.grid(row=7, column=0, sticky="W")

        #DEF Entry
        entry_1 = tk.Entry(labelFrame)
        entry_2 = tk.Entry(labelFrame)
        entry_3 = tk.Entry(labelFrame)
        entry_4 = tk.Entry(labelFrame)
        entry_5 = tk.Entry(labelFrame)
        entry_6 = tk.Entry(labelFrame)
        entry_7 = tk.Checkbutton(labelFrame, onvalue=1 , offvalue=1 , variable=self.normalCons)

        entry_1.grid(row=1, column=1, sticky="W")
        entry_2.grid(row=2, column=1, sticky="W")
        entry_3.grid(row=3, column=1, sticky="W")
        entry_4.grid(row=4, column=1, sticky="W")
        entry_5.grid(row=5, column=1, sticky="W")
        entry_6.grid(row=6, column=1, sticky="W")
        entry_7.grid(row=7, column=1, sticky="W")

        #BTN
        button_1 = tk.Button(labelFrame, text="Make STL", command=lambda : self.stl_run())
        button_2 = tk.Button(labelFrame, text="Back" , command=lambda : controller.show_frame("ConfigPage"))
        button_1.grid(row=9 , column=2 , sticky="W")
        button_2.grid(row=9, column=3 , sticky="E")



    def stl_run(self):

        filename = global_vars.current_filename
        if global_vars.current_filename[-3:] == "txt":
            filename = App.fileOperation.txtTopcd(global_vars.current_filename)

        subprocess.check_call([os.path.join(thisDir, 'stl_triangulation.exe'), '--file', filename])
        print "Finish create stl"
        #subprocess.call(['stl_triangulation.exe ', '--file',FILEPATH], shell=False)


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label_1 = ttk.Label(self, text="COS TAM")
        label_2 = ttk.Label(self, text="COS TAM 2")

        entry_1 = ttk.Entry(self)
        entry_2 = ttk.Entry(self)

        label_1.grid(row=0, padx=20, pady=20)
        label_2.grid(row=1)
        entry_1.grid(row=0, column=1)
        entry_2.grid(row=1, column=1)
        #label = ttk.Label(self, text=" Page One", font=LARGE_FONT)
        #label.pack()
       # button1 = ttk.Button(self, text="Visit StartPage", command=lambda: controller.show_frame("StartPage"))
       # button1.pack()





def run_gui():
    app = App()
    app.minsize(width=global_vars.window_width, height=global_vars.window_height)
    app.mainloop()

if __name__ == "__main__":
    print "RUNNING IN DEBUG MODE!"
    global_vars.dump_vars()
    run_gui()