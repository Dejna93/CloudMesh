# coding=UTF-8
import subprocess
import os
import Tkinter as tk
import tkFileDialog
from PIL import Image,ImageTk
from FileList import FileList
from tkMessageBox import *

from plugin.config import global_vars


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        about = """
        //PL
            Plugin przeznaczony do stworzenia geometrii w Abaqusie z chmury punktów.
        Plik z chmurą punktów powinien być rozszerzenia .txt lub .csv
        a punkty xyz powinny być w kolumnach odzielone od siebie 'spacją lub tabulatorem' w przypadku
        pliku txt

        //ENG
            TODO
        """
        self.start_labelframe = tk.LabelFrame(self, text="About", height=global_vars.dlab_height, padx=10, pady=10)
        self.start_labelframe.grid(row=0, column=0, sticky="NS")

        self.label_about = tk.Label(self.start_labelframe, text=about)
        self.label_about.grid(row=0, column=0, columnspan=4)

        button1 = tk.Button(self.start_labelframe, text="OK", command=lambda: controller.show_frame("ConfigPage"))
        button1.grid(row=1, column=1)
        button2 = tk.Button(self.start_labelframe, text="Quit", command=lambda: StartPage.quit(self))
        button2.grid(row=1, column=2)


class ConfigPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        #self.fileoper = FileOperation()
        # define options for opening or saving a file
        self.initOptions()

        # labels
        self.labelFramse()
        self.initLabels()
        self.initScrollList()
        self.initEntry()
        self.initButtons()
        self.manageGrid()

    def initOptions(self):
        self.fileopt = options = {}
        options['defaultextension'] = '.txt'
        options['filetypes'] = [('text files', '.txt'), ('Csv files','.csv'),('Point cloud data', '.pcd')]
        options['initialdir'] = global_vars.plugin_dir
        options['initialfile'] = ''
        options['parent'] = self
        options['title'] = 'Open file to import'

    def labelFramse(self):
        self.labelFrame_1 = tk.LabelFrame(self, text="Specify Txt File", height=global_vars.dlab_height, padx=10, pady=10)
        self.labelFrame_2 = tk.LabelFrame(self, text="Operations", height=global_vars.dlab_height, padx=10, pady=10)
        self.labelFrame_3 = tk.LabelFrame(self, text="STL file", height=global_vars.dlab_height, padx=10, pady=10)

    def initLabels(self):
        self.label_1 = tk.Label(self.labelFrame_1, text="Txt file name", bg="white")
        self.label_3 = tk.Label(self.labelFrame_2, text="Create STL")
        self.label_4 = tk.Label(self.labelFrame_2, text="Import Geometry")

    def initEntry(self):
        self.entry_1 = tk.Entry(self.labelFrame_1, bd=2, width=50)

    def initButtons(self):
        im = Image.open(global_vars.ico_btn_open)
        ph = ImageTk.PhotoImage(im)

        self.btn_1 = tk.Button(self.labelFrame_1, image=ph, command=self.askopenfile)
        self.btn_3 = tk.Button(self.labelFrame_2, text="OK", command=lambda: self.check_filepath(self.controller))
        self.btn_4 = tk.Button(self.labelFrame_2, text="Import")
        self.btn_del = tk.Button(self.labelFrame_3, text="Del", command=self.delete)

        self.btn_1.image = ph

    def initScrollList(self):
        self.focus_box = None
        self.scrollbar = tk.Scrollbar(self.labelFrame_3)
        # self.stlList = tk.Listbox(self.labelFrame_3, yscrollcommand=self.scrollbar.set, width=50)
        self.stlList = FileList(self.labelFrame_3, yscrollcommand=self.scrollbar.set, width=50)
        self.stlList.bind("<FocusIn>", self.box_focused)
        self.stlList.bind("<FocusOut>", self.box_unfocused)
        self.scrollbar.config(command=self.stlList.yview)

    def manageGrid(self):
        self.labelFrame_1.grid(row=0, columnspan=8, sticky='WE', padx=10, pady=10)
        self.labelFrame_2.grid(row=2, column=0, sticky="WE", padx=10, pady=10)
        self.labelFrame_3.grid(row=4, column=0, sticky="WE", padx=20)
        # ----------
        self.label_1.grid(row=1, column=1, sticky="W")
        self.label_3.grid(row=3, column=4, sticky="W", padx=10)
        self.label_4.grid(row=3, column=6, sticky="W", padx=10)
        # ----------
        self.btn_1.grid(row=1, column=3, sticky="W", padx=10)
        self.btn_3.grid(row=3, column=5, sticky="W", padx=5)
        self.btn_4.grid(row=3, column=7, sticky="W", padx=20)
        self.btn_del.grid(row=5, column=3, sticky="E", padx=10)
        # ----------
        self.scrollbar.grid(rowspan=5, row=5, column=1, sticky="WE")
        self.stlList.columnconfigure(0, weight=1)
        self.stlList.grid(row=5, column=2, sticky="WE", padx=10, pady=10)
        # ---------
        self.entry_1.grid(row=1, column=2, sticky="E", padx=10)

    def box_focused(self, event):
        self.focus_box = event.widget

    def box_unfocused(self, event):
        self.focus_box = None

    def delete(self):
        if not self.focus_box:
            pass
        selection = self.stlList.curselection()
        if selection:
            self.focus_box.delete(selection[0])

    def askopenfile(self):
        global_vars.current_filename = tkFileDialog.askopenfilename(**self.fileopt)

        if global_vars.current_filename:
            if not global_vars.current_filename in global_vars.files_selecteced:
                global_vars.files_selecteced.append(global_vars.current_filename)

            self.set_entry(global_vars.current_filename)
            self.stlList.insert(0, self.get_filename_from_path(global_vars.current_filename))
            return open(global_vars.current_filename, 'r')


    def get_filename_from_path(self, filepath):
        import ntpath
        head, tail = ntpath.split(filepath)
        return tail
    def set_entry(self, text):
        self.entry_1.delete(0, tk.END)
        self.entry_1.insert(0, text)

    def check_filepath(self, controller):
        if global_vars.current_filename:
            controller.show_frame("STLPage")

    def opennew(self):
        print "opening"
