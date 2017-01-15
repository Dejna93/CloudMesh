# coding=UTF-8
import subprocess
import os
from sys import version
from math import pi
from shutil import copy2
import Tkinter as tk
import tkFileDialog
from tkMessageBox import showerror
from plugin.config import global_vars
from plugin.utils.project import open_project
from plugin.utils.converter import convert_txt_to_pcd, convert_csv_to_pcd
from plugin.utils.inputs import input_validator
from plugin.utils.oso import join , change_ext , get_filename_from_path


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

        if version[:3] >= global_vars.PYTHON_VERSION:
            self.btn_workspace = tk.Button(self.workspace_frame, image=global_vars.tk_img_open,
                                       command=open_project)
            self.btn_workspace.image = global_vars.tk_img_open
        else:
            self.btn_workspace = tk.Button(self.workspace_frame, text="Open",
                                           command=open_project)
        self.btn_workspace.grid(row=0, column=1)


    def update(self):
        print "update"


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
        self.label_4 = tk.Label(self.labelFrame_2, text="STL to Abaqus")

    def initEntry(self):
        self.entry_1 = tk.Entry(self.labelFrame_1, bd=2, width=50)
        if global_vars.current_filename:
            self.entry_1.insert(0, global_vars.current_filename)

    def initButtons(self):
        # im = Image.open(global_vars.ico_btn_open)
        # ph = ImageTk.PhotoImage(im)
        if version[:3] >= global_vars.PYTHON_VERSION:
            self.btn_1 = tk.Button(self.labelFrame_1, image=global_vars.tk_img_open, command=self.askopenfile)
            self.btn_1.image = global_vars.img_open_btn
        else:
            self.btn_1 = tk.Button(self.labelFrame_1, text="Open", command=self.askopenfile)
        self.btn_3 = tk.Button(self.labelFrame_2, text="OK", command=lambda: self.pre_converting(
            self.controller))  # self.check_filepath(self.controller))
        self.btn_4 = tk.Button(self.labelFrame_2, text="Import" , command = self.to_abaqus)
        self.btn_del = tk.Button(self.labelFrame_3, text="Del", command=self.delete)



    def initScrollList(self):

        self.scrollbar = tk.Scrollbar(self.labelFrame_3)
        self.stlList = tk.Listbox(self.labelFrame_3, yscrollcommand=self.scrollbar.set, width=30)
        # self.stlList = FileList(self.labelFrame_3, yscrollcommand=self.scrollbar.set, width=50)
        self.stlList.bind("<FocusIn>", self.stl_focused)
        self.stlList.bind("<FocusOut>", self.stl_unfocused)
        self.stlList.bind("<Double-Button-1>", self.select_stl)
        self.scrollbar.config(command=self.stlList.yview)


    def initTxtScrollList(self):

        self.txt_scrollbar = tk.Scrollbar(self.labelFrame_3)
        self.txt_list = tk.Listbox(self.labelFrame_3, yscrollcommand=self.txt_scrollbar.set,
                                   width=30)
        self.txt_scrollbar.config(command=self.txt_list.yview)
        self.txt_list.bind("<FocusIn>", self.box_focused)
        self.txt_list.bind("<FocusOut>", self.box_unfocused)
        self.txt_list.bind("<Double-Button-1>", self.select_item)
        if global_vars.files_opened:
            for files in global_vars.files_opened:
                self.txt_list.insert(0, self.get_filename_from_path(files))

    def manageGrid(self):
        self.labelFrame_1.grid(row=0, columnspan=8, sticky='WE', padx=10, pady=10)
        self.labelFrame_2.grid(row=2, column=0, sticky="WE", padx=10, pady=10)
        self.labelFrame_3.grid(row=4, column=0, sticky="WE", padx=10, pady=10)
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
        self.focus_txt = event.widget

    def box_unfocused(self, event):
        self.focus_txt = None

    def stl_focused(self, event):
        self.focus_stl = event.widget

    def stl_unfocused(self, event):
        self.focus_stl = None

    def select_item(self, event):
        if self.focus_txt:
            widget = event.widget
            if widget.curselection():
                global_vars.update_currentfile(widget.get(widget.curselection()[0]))
                self.set_entry(global_vars.current_filename)

    def select_stl(self, event):
        if self.focus_stl:
            widget = event.widget
            if len(widget.curselection()) != 0:
                print "selection "+widget.get(widget.curselection()[0])
                global_vars.update_currentstl(widget.get(widget.curselection()[0]))
                print "current_stl"+ global_vars.current_stl
        else:
            print "NIE MA STLA"
    def delete(self):
        if not self.focus_txt:
            pass
        if self.txt_list.curselection():
            global_vars.del_file_open(self.txt_list.get(self.txt_list.curselection()[0]))
            self.txt_list.delete(self.txt_list.curselection()[0])
        if not self.focus_stl:
            pass
        if self.stlList.curselection():
            global_vars.del_file_open(self.txt_list.get(self.stlList.curselection()[0]))
            self.stlList.delete(self.stlList.curselection()[0])

    """  if not self.focus_stl:
          pass
      selection = self.stlList.curselection()
      if selection:
          self.focus_stl.delete(selection[0])"""

    def askopenfile(self):
        ##TODO dodaj obsluge kopiowania do katalogu projektu
        # global_vars.dump_vars()
        if global_vars.workspace_dir == global_vars.current_project or global_vars.current_project == '':
            showerror("Nie wybrano projektu", "Prosze wybrać projekt w ktorym \n beda zapisywac sie dane")
        else:
            add_file = tkFileDialog.askopenfilename(**self.fileopt)
            print "OPEN FILE" + add_file
            if not os.path.exists(join(global_vars.project_points_folder, os.path.split(add_file)[1])):
                # print "Coping " + add_file +" to " + global_vars.project_points_folder + "/"+self.get_filename_from_path(add_file)
                copy2(add_file, global_vars.project_points_folder)
                global_vars.current_filename = join(global_vars.project_points_folder,
                                                    self.get_filename_from_path(add_file)).replace("\\", "/")
            else:
                print global_vars.project_points_folder
                #global_vars.current_filename = join(global_vars.project_points_folder,
                                                   # os.path.split(add_file)[1]).replace("\\", "/")

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
        if global_vars.current_filename:
            if global_vars.current_filename[-3:] == 'txt':
                global_vars.created_pcd.append(convert_txt_to_pcd(global_vars.current_filename))
            if global_vars.current_filename[-3:] == 'csv':
                convert_csv_to_pcd(global_vars.current_filename)
            controller.show_frame("STLPage")

    def to_abaqus(self):
        print global_vars.current_stl

        self.controller.show_frame("AbaqusPage")


    def opennew(self):
        print "opening"

    def update(self):
        self.stlList.delete(0,tk.END)
        self.txt_list.delete(0,tk.END)
        for item in global_vars.files_opened:
            self.txt_list.insert(tk.END,self.get_filename_from_path(item))
        for item in global_vars.created_stl:
            print "update "+self.get_filename_from_path(item)
            self.stlList.insert(tk.END,self.get_filename_from_path(item))



class STLPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        labelFrame = tk.LabelFrame(self, text="Triangulation options", width=global_vars.dlab_width,
                                   height=global_vars.dlab_height, padx=10, pady=10)
        labelFrame.grid(row=0, column=0, sticky='W', padx=10, pady=10, ipadx=5, ipady=5)
        self.pcdFrame = tk.LabelFrame(self, text="PCD Files", width=global_vars.dlab_width, padx=10, pady=10)
        self.pcdFrame.grid(row=1, column=0, sticky="WE", padx=10, pady=10)
        # LABELS STL
        label_1 = tk.Label(labelFrame, text="setMaximumNearestNeighbors")
        label_2 = tk.Label(labelFrame, text="setMu")
        label_3 = tk.Label(labelFrame, text="setSearchRadius")
        label_4 = tk.Label(labelFrame, text="setMinimumAngle")
        label_5 = tk.Label(labelFrame, text="setMaximumAngle")
        label_6 = tk.Label(labelFrame, text="setMaximumSurfaceAgle")
        label_7 = tk.Label(labelFrame, text="setNormalConsistency")

        initialVars = (0.025, 2.5, 100, pi / 4, pi / 18, 2 * pi / 3, 0)
        self.checkInt = tk.IntVar()
        self.checkInt.set(0)

        label_pcd = tk.Label(self.pcdFrame, text="PCD list")

        pcd_scrollbar = tk.Scrollbar(self.pcdFrame)
        self.pcd_list = tk.Listbox(self.pcdFrame, yscrollcommand=pcd_scrollbar.set,
                                   width=40, selectmode=tk.EXTENDED)
        pcd_scrollbar.config(command=self.pcd_list.yview)
        self.update_list()
        self.pcd_list.grid(row=1, column=0, sticky="W")
        pcd_scrollbar.grid(row=1, column=1, sticky="E")

        # GRID
        label_1.grid(row=1, column=0, sticky="W")
        label_2.grid(row=2, column=0, sticky="W")
        label_3.grid(row=3, column=0, sticky="W")
        label_4.grid(row=4, column=0, sticky="W")
        label_5.grid(row=5, column=0, sticky="W")
        label_6.grid(row=6, column=0, sticky="W")
        label_7.grid(row=7, column=0, sticky="W")

        label_pcd.grid(row=0, column=0, sticky="W")
        # DEF Entry
        self.entires = []
        for i in range(0, 7):
            print i
            if i <= 5:
                self.entires.append(tk.Entry(labelFrame))
                self.entires[i].insert(tk.END, initialVars[i])
                self.entires[i].bind("<KeyPress>", input_validator)
            else:
                self.entires.append(tk.Checkbutton(labelFrame, variable=self.checkInt))

        for i in range(0, 7):
            self.entires[i].grid(row=i + 1, column=1, sticky="W")


        # BTN
        button_1 = tk.Button(labelFrame, text="Make STL", command=lambda: self.stl_run())
        button_2 = tk.Button(labelFrame, text="Back", command=lambda: controller.show_frame("ConfigPage"))

        del_btn = tk.Button(self.pcdFrame, text="Del", command=self.delete)
        del_btn.grid(row=0, column=2, sticky="E")

        button_1.grid(row=9, column=2, sticky="W")
        button_2.grid(row=9, column=3, sticky="E")

    def delete(self):
        if self.pcd_list.curselection():
            print self.pcd_list.curselection()
            pos = 0
            for item in self.pcd_list.curselection():
                ind = item - pos
                global_vars.del_file_pcd(self.pcd_list.get(item))
                self.pcd_list.delete(ind, ind)
                pos = pos + 1

    def update_list(self):
        self.pcd_list.delete(0 , tk.END)
        print global_vars.created_pcd
        if global_vars.created_pcd:
            for item in global_vars.created_pcd:
                self.pcd_list.insert(tk.END, '/'.join(item.split('/')[-4:]))

    def update(self):
        self.update_list()

    def stl_run(self):
        # file_list = self.pcd_list.curselection()
        params = []
        for item in self.entires[:-1]:
            params.append(item.get())
        params.append(self.entires[-1])
        # dodawanie parametow do triangulizacji
        print global_vars.created_pcd

        for idx in self.pcd_list.curselection():
            print idx
            print os.path.join(os.path.split(global_vars.plugin_dir)[0], 'stl_triangulation.exe')
            subprocess.check_call(
                [os.path.join(os.path.split(global_vars.plugin_dir)[0], 'stl_triangulation.exe'), '--file',
                 global_vars.created_pcd[int(idx)]])
            copy2(change_ext( global_vars.created_pcd[int(idx)], '.stl'), global_vars.project_stl_folder)

            global_vars.created_stl.append(change_ext( global_vars.created_pcd[int(idx)], '.stl'))

class AbaqusPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.labelFrame = tk.LabelFrame(self, text="STL settings for import" , width=global_vars.dlab_width , height = global_vars.dlab_height , padx=10 , pady=10)
        self.labelFrame.grid(row=0 , column=0, sticky="NWSE", padx=10, pady=10, ipadx=5, ipady=5)

        self.nameLabel = tk.Label(self.labelFrame , text="File")
        self.modelLabel = tk.Label(self.labelFrame, text="Model name")
        self.nodeLabel = tk.Label(self.labelFrame, text="Merge tolerance")

        self.nameLabel.grid(row=0,column=0 , sticky="E" , padx=10)
        self.modelLabel.grid(row=1,column=0,sticky="E",  padx=10)
        self.nodeLabel.grid(row=2,column=0 , sticky="E",  padx=10)

        self.enties = []
        for i in range(0,3):
            self.enties.append(tk.Entry(self.labelFrame))
            self.enties[i].grid(row=i , column=1,sticky="W")

        self.enties[0].insert(0,global_vars.current_stl)
        self.enties[1].insert(0,get_filename_from_path(global_vars.current_stl))
        self.enties[2].insert(0,global_vars.nodeTolerance)

        self.run_abaqus_stl = tk.Button(self.labelFrame, text="To Abaqus" , command =  self.stl_abaqus )
        self.run_abaqus_stl.grid(row=3,column=1,sticky="EW", padx=10,pady=10)

        self.back_btn = tk.Button(self.labelFrame, text="Back", command=lambda: controller.show_frame("ConfigPage"))
        self.back_btn.grid(row=3,column=0, sticky="E", padx=10,pady=10)

    def stl_abaqus(self):
        params = []

        for item in self.enties:
            params.append(item.get())
        print params

        if global_vars.DEBUG==False :
            from plugin.utils.abaqus import stl_to_abaqus
            stl_to_abaqus(params[0],params[1],params[2])








