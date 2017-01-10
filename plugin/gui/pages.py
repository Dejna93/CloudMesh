# coding=UTF-8
import subprocess
import os
from shutil import copy2
import Tkinter as tk
import tkFileDialog
from PIL import Image, ImageTk
from FileList import FileList
from tkMessageBox import *
from tkMessageBox import showerror
from plugin.config import global_vars
from plugin.utils.project import open_project


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

        self.workspace_frame = tk.LabelFrame(self, text="Choice workspace", height=global_vars.dlab_height, padx=10,
                                             pady=10)
        self.workspace_frame.grid(row=2, column=0, sticky="WE")

        self.label_work = tk.Label(self.workspace_frame, text="Set workscape")
        self.label_work.grid(row=0, column=0)

        self.btn_workspace = tk.Button(self.workspace_frame, image=global_vars.tk_img_open,
                                       command=open_project)
        self.btn_workspace.grid(row=0, column=1)
        self.btn_workspace.image = global_vars.tk_img_open


class ConfigPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        # global_vars.dump_vars()

        self.focus_stl = None
        self.focus_txt = None

        # self.fileoper = FileOperation()
        # define options for opening or saving a file
        self.initOptions()

        # labels
        self.labelFramse()
        self.initLabels()
        self.initScrollList()
        self.initTxtScrollList()
        self.initEntry()
        self.initButtons()
        self.manageGrid()

    def initOptions(self):
        self.fileopt = options = {}
        options['defaultextension'] = '.txt'
        options['filetypes'] = [('text files', '.txt'), ('Csv files', '.csv'), ('Point cloud data', '.pcd')]
        options['initialdir'] = global_vars.plugin_dir
        options['initialfile'] = ''
        options['parent'] = self
        options['title'] = 'Open file to import'

    def labelFramse(self):
        self.labelFrame_1 = tk.LabelFrame(self, text="Specify Txt File", height=global_vars.dlab_height, padx=10,
                                          pady=10)
        self.labelFrame_2 = tk.LabelFrame(self, text="Operations", height=global_vars.dlab_height, padx=10, pady=10)
        self.labelFrame_3 = tk.LabelFrame(self, text="STL file", height=global_vars.dlab_height, padx=10, pady=10)

    def initLabels(self):
        self.label_1 = tk.Label(self.labelFrame_1, text="Txt file name", bg="white")
        self.label_3 = tk.Label(self.labelFrame_2, text="Create STL")
        self.label_4 = tk.Label(self.labelFrame_2, text="Import Geometry")

    def initEntry(self):
        self.entry_1 = tk.Entry(self.labelFrame_1, bd=2, width=50)

    def initButtons(self):
        # im = Image.open(global_vars.ico_btn_open)
        # ph = ImageTk.PhotoImage(im)

        self.btn_1 = tk.Button(self.labelFrame_1, image=global_vars.tk_img_open, command=self.askopenfile)
        self.btn_3 = tk.Button(self.labelFrame_2, text="OK", command=lambda: self.pre_converting(
            self.controller))  # self.check_filepath(self.controller))
        self.btn_4 = tk.Button(self.labelFrame_2, text="Import")
        self.btn_del = tk.Button(self.labelFrame_3, text="Del", command=self.delete)

        self.btn_1.image = global_vars.img_open_btn

    def initScrollList(self):

        self.scrollbar = tk.Scrollbar(self.labelFrame_3)
        self.stlList = tk.Listbox(self.labelFrame_3, yscrollcommand=self.scrollbar.set, width=30)
        # self.stlList = FileList(self.labelFrame_3, yscrollcommand=self.scrollbar.set, width=50)
        self.stlList.bind("<FocusIn>", self.stl_focused)
        self.stlList.bind("<FocusOut>", self.stl_unfocused)
        self.scrollbar.config(command=self.stlList.yview)

    def initTxtScrollList(self):

        self.txt_scrollbar = tk.Scrollbar(self.labelFrame_3)
        self.txt_list = tk.Listbox(self.labelFrame_3, selectmode='multiple', yscrollcommand=self.txt_scrollbar.set,
                                   width=30)
        self.txt_scrollbar.config(command=self.txt_list.yview)
        self.txt_list.bind("<FocusIn>", self.box_focused)
        self.txt_list.bind("<FocusOut>", self.box_unfocused)
        if global_vars.files_opened:
            for files in global_vars.files_opened:
                self.txt_list.insert(0, self.get_filename_from_path(files))

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
        self.btn_del.grid(row=5, column=5, sticky="E", padx=10)
        # ----------
        self.scrollbar.grid(rowspan=2, row=5, column=4, sticky="WE")
        self.stlList.columnconfigure(0, weight=1)
        self.stlList.grid(row=5, column=3, sticky="WE", padx=10, pady=10)

        self.txt_scrollbar.grid(row=5, column=1, sticky="WE")
        self.txt_list.grid(row=5, column=2, sticky="WE", padx=10, pady=10)
        # ---------
        self.entry_1.grid(row=1, column=2, sticky="E", padx=10)

    def box_focused(self, event):
        self.focus_stl = event.widget

    def box_unfocused(self, event):
        self.focus_stl = None

    def stl_focused(self, event):
        print event.widget
        self.focus_txt = event.widget

    def stl_unfocused(self, event):
        self.focus_txt = None

    def delete(self):
        if not self.focus_txt:
            pass
        if self.txt_list.curselection():
            global_vars.del_file_open(self.txt_list.get(self.txt_list.curselection()[0]))
            self.txt_list.delete(self.txt_list.curselection()[0])
        if not self.focus_stl:
            pass
        if self.stlList.curselection():
            global_vars.del_file_open(self.focus_stl.get(self.stlList.curselection()[0]))
            self.stlList.delete(self.stlList.curselection()[0])

    """  if not self.focus_stl:
          pass
      selection = self.stlList.curselection()
      if selection:
          self.focus_stl.delete(selection[0])"""

    def multi_select(self, event):
        # print self.txt_list.curselection()
        global_vars.files_selected = self.txt_list.curselection()
        # print global_vars.files_selected

    def askopenfile(self):
        ##TODO dodaj obsluge kopiowania do katalogu projektu
        # global_vars.dump_vars()
        if global_vars.workspace_dir == global_vars.current_project or global_vars.current_project == '':
            showerror("Nie wybrano projektu", "Prosze wybrać projekt w ktorym \n beda zapisywac sie dane")
        add_file = tkFileDialog.askopenfilename(**self.fileopt)

        if not os.path.exists(os.path.join(global_vars.project_points_folder, self.get_filename_from_path(add_file))):
            # print "Coping " + add_file +" to " + global_vars.project_points_folder + "/"+self.get_filename_from_path(add_file)
            copy2(add_file, global_vars.project_points_folder)
            global_vars.current_filename = os.path.join(global_vars.project_points_folder,
                                                        self.get_filename_from_path(add_file))
        else:
            global_vars.current_filename = add_file

        if global_vars.current_filename:
            if not global_vars.current_filename in global_vars.files_opened:
                global_vars.files_opened.append(global_vars.current_filename)

        self.set_entry(global_vars.current_filename)
        self.txt_list.insert(0, self.get_filename_from_path(global_vars.current_filename))


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

    def pre_converting(self, controller):
        print "controller"

    def opennew(self):
        print "opening"


class STLPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        labelFrame = tk.LabelFrame(self, text="Triangulation options", height=200, padx=10, pady=10)
        labelFrame.grid(row=0, columnspan=7, sticky='W', padx=5, pady=5, ipadx=5, ipady=5)

        self.maxNearNeigh = tk.DoubleVar()
        self.Mu = tk.DoubleVar()
        self.searchRadius = tk.DoubleVar()
        self.minAngle = tk.DoubleVar()
        self.maxAngle = tk.DoubleVar()
        self.maxSurfAgle = tk.DoubleVar()
        self.normalCons = tk.IntVar()
        # LABELS STL
        label_1 = tk.Label(labelFrame, text="setMaximumNearestNeighbors")
        label_2 = tk.Label(labelFrame, text="setMu")
        label_3 = tk.Label(labelFrame, text="setSearchRadius")
        label_4 = tk.Label(labelFrame, text="setMinimumAngle")
        label_5 = tk.Label(labelFrame, text="setMaximumAngle")
        label_6 = tk.Label(labelFrame, text="setMaximumSurfaceAgle")
        label_7 = tk.Label(labelFrame, text="setNormalConsistency")

        # LOCALISATION
        label_1.grid(row=1, column=0, sticky="W")
        label_2.grid(row=2, column=0, sticky="W")
        label_3.grid(row=3, column=0, sticky="W")
        label_4.grid(row=4, column=0, sticky="W")
        label_5.grid(row=5, column=0, sticky="W")
        label_6.grid(row=6, column=0, sticky="W")
        label_7.grid(row=7, column=0, sticky="W")

        # DEF Entry
        entry_1 = tk.Entry(labelFrame)
        entry_2 = tk.Entry(labelFrame)
        entry_3 = tk.Entry(labelFrame)
        entry_4 = tk.Entry(labelFrame)
        entry_5 = tk.Entry(labelFrame)
        entry_6 = tk.Entry(labelFrame)
        entry_7 = tk.Checkbutton(labelFrame, onvalue=1, offvalue=1, variable=self.normalCons)

        entry_1.grid(row=1, column=1, sticky="W")
        entry_2.grid(row=2, column=1, sticky="W")
        entry_3.grid(row=3, column=1, sticky="W")
        entry_4.grid(row=4, column=1, sticky="W")
        entry_5.grid(row=5, column=1, sticky="W")
        entry_6.grid(row=6, column=1, sticky="W")
        entry_7.grid(row=7, column=1, sticky="W")

        # BTN
        button_1 = tk.Button(labelFrame, text="Make STL", command=lambda: self.stl_run())
        button_2 = tk.Button(labelFrame, text="Back", command=lambda: controller.show_frame("ConfigPage"))
        button_1.grid(row=9, column=2, sticky="W")
        button_2.grid(row=9, column=3, sticky="E")

    def stl_run(self):
        if global_vars.current_filename[-3:] == "txt":
            #   filename = App.fileOperation.txtTopcd(global_vars.current_filename)
            # subprocess.check_call([os.path.join(, 'stl_triangulation.exe'), '--file', filename])
            print "Finish create stl"
            # subprocess.call(['stl_triangulation.exe ', '--file',FILEPATH], shell=False)
