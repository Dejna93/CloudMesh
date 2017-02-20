# coding=UTF-8
import subprocess
import os

from sys import version
from math import pi
from shutil import copy2
import Tkinter as tk
import tkFileDialog
from collections import OrderedDict

from tkMessageBox import showerror
from plugin.config import global_vars
from plugin.utils.project import open_project
from plugin.utils.converter import convert_txt_to_pcd, convert_csv_to_pcd
from plugin.utils.inputs import input_validator
from plugin.utils.oso import join , change_ext , get_filename_from_path, get , get_selection

from plugin.utils.params import stlParams

__metaclass__ = type

class Page(tk.Frame, object):
    def __init__(self, parent ):
        tk.Frame.__init__(self,parent)
        self.parent = parent

    def update(self):
        self.after(1000, self.update)

class StartPage(Page):
    def __init__(self, parent, controller):
        Page.__init__(self, parent)
        self.parent = parent
        self.controller = controller

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



    def update(self):

        super(StartPage,self).update()



class ConfigPage(Page):
    def __init__(self, parent, controller):
        Page.__init__(self, parent)
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
        options['filetypes'] = [('text files', '.txt'), ('Csv files', '.csv'), ('Point cloud data', '.pcd'), ('STL files', '.stl')]
        options['initialdir'] = global_vars.current_project if global_vars.current_project !='' and global_vars.current_project != global_vars.workspace_dir else global_vars.workspace_dir
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
        self.entry_1 = tk.Entry(self.labelFrame_1, bd=2, width=70)
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
        self.btn_add = tk.Button(self.labelFrame_3, text="Add STL" , command=self.add_stl)



    def initScrollList(self):

        self.scrollbar = tk.Scrollbar(self.labelFrame_3)
        self.stlList = tk.Listbox(self.labelFrame_3, yscrollcommand=self.scrollbar.set)
        # self.stlList = FileList(self.labelFrame_3, yscrollcommand=self.scrollbar.set, width=50)
        self.stlList.bind("<FocusIn>", self.stl_focused)
        self.stlList.bind("<FocusOut>", self.stl_unfocused)
        self.stlList.bind("<Double-Button-1>", self.select_stl)
        self.scrollbar.config(command=self.stlList.yview)


    def initTxtScrollList(self):

        self.txt_scrollbar = tk.Scrollbar(self.labelFrame_3)
        self.txt_list = tk.Listbox(self.labelFrame_3,listvariable=global_vars.files_opened,
                                   yscrollcommand=self.txt_scrollbar.set
                                   ,width=90)
        self.txt_scrollbar.config(command=self.txt_list.yview)
        self.txt_list.bind("<FocusIn>", self.box_focused)
        self.txt_list.bind("<FocusOut>", self.box_unfocused)
        self.txt_list.bind("<Double-Button-1>", self.select_item)
        if len(global_vars.files_opened) != 0:
            for files in global_vars.files_opened:
                self.txt_list.insert(tk.END,files)


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
        self.btn_del.grid(row=7, column=1, sticky="E", padx=10)
        self.btn_add.grid(row=7,column=0, sticky="E", padx=10)
        # ----------
        self.scrollbar.grid(row=6, column=11, sticky="WE")
      #  self.stlList.columnconfigure(0, weight=1)
        self.stlList.grid(row=6, column=0,columnspan=10, sticky="WE", padx=10, pady=10)

        self.txt_scrollbar.grid(row=5, column=11, sticky="WE")
        self.txt_list.grid(row=5, column=0,columnspan=10, sticky="WE", padx=10, pady=10)
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
            global_vars.del_file_open(self.txt_list.get(self.txt_list.curselection()[0]),0)
            self.txt_list.delete(self.txt_list.curselection()[0])
        if not self.focus_stl:
            pass
        if self.stlList.curselection():
            global_vars.del_file_open(self.stlList.get(self.stlList.curselection()[0]),1)
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
            if add_file != '':
                folder_dst = global_vars.project_points_folder if global_vars.current_filename[-3:] != 'stl' else global_vars.project_stl_folder

                if not os.path.exists(join(folder_dst, os.path.split(add_file)[1])):
                    # print "Coping " + add_file +" to " + global_vars.project_points_folder + "/"+self.get_filename_from_path(add_file)

                    copy2(add_file, global_vars.project_points_folder)
                    add_file = join(folder_dst, self.get_filename_from_path(add_file)).replace("\\", "/")
                else:
                    add_file = join(folder_dst,os.path.split(add_file)[1]).replace("\\", "/")

                if add_file and add_file[-3:] != 'stl' :
                    if not add_file in global_vars.files_opened:
                        global_vars.files_opened.append(add_file)
                        self.set_entry(add_file)
                        self.txt_list.insert(0, add_file)
                else:
                    if not add_file in global_vars.created_stl:
                        global_vars.created_stl.append(add_file)
                        self.set_entry(add_file)
                        #self.stlList.insert(0, self.get_filename_from_path(add_file))

                global_vars.current_filename = add_file if add_file[-3:] != 'stl' else ''
                global_vars.current_stl = add_file if add_file[-3:] =='stl' else ''

                #self.set_entry(global_vars.current_filename)
                #self.txt_list.insert(0, self.get_filename_from_path(global_vars.current_filename))
            else:
                showerror("Nie wybrano pliku", "Prosze wskazać plik do otwarcia")

    def add_stl(self):
        options = {}
        options['defaultextension'] = '.stl'
        options['initialfile'] = ''
        options['parent'] = self
        options['title'] = 'Open file to import'
        options['filetypes'] = [('STL files', '.stl')]
        options['initialdir'] = global_vars.project_stl_folder
        options['title'] = 'Add Stl to project'
        add_file = tkFileDialog.askopenfilename(**options)
        if add_file != '':
            print add_file
            global_vars.add_to_stl(add_file)

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
        self.controller.show_frame("AbaqusPage")


    def update(self):
        self.update_list()
        if self.focus_txt:
            self.txt_list.selection_set(get_selection(self.txt_list.curselection(), 0))
        if self.focus_stl:
            self.stlList.selection_set(get_selection(self.stlList.curselection() ,0))
        super(ConfigPage,self).update()

    def update_list(self):
        if not global_vars.is_same_list(self.txt_list.get(0,tk.END) , global_vars.files_opened):
            print "update list"
            self.txt_list.delete(0,tk.END)
            for item in global_vars.files_opened:
                self.txt_list.insert(tk.END,item)
            #self.txt_list.selection_set(0)

        if not global_vars.is_same_list(self.stlList.get(0, tk.END), global_vars.created_stl):
            self.stlList.delete(0, tk.END)
            print  "update stl"
            for item in global_vars.created_stl:
                self.stlList.insert(tk.END, item)

    def update_title(self):
        self.controller.wm_title(global_vars.title +  '/'.join(global_vars.current_project.split('/')[-4:]))



class STLPage(Page):
    def __init__(self, parent, controller):
        Page.__init__(self, parent)
        self.controller = controller

        labelFrame = tk.LabelFrame(self, text="Triangulation options", width=global_vars.dlab_width,
                                   height=global_vars.dlab_height, padx=10, pady=10)
        labelFrame.grid(row=0, column=0, sticky='W', padx=10, pady=10, ipadx=5, ipady=5)
        self.pcdFrame = tk.LabelFrame(self, text="PCD Files", width=global_vars.dlab_width, padx=10, pady=10)
        self.pcdFrame.grid(row=1, column=0, sticky="WE", padx=10, pady=10)


        # LABELS STL
        text_labels = [
            "setMaximumNearestNeighbors",
            "setMu",
            "setSearchRadius",
            "setMinimumAngle",
            "setMaximumAngle",
            "setMaximumSurfaceAgle",
            "setNormalConsistency"
        ]
        self.labels = []
        self.buttons = []

        self.labels.append(tk.Label(labelFrame, text="Option" ))
        self.labels.append(tk.Label(labelFrame, text="Laplacian Triangulation"))
        self.labels.append(tk.Label(labelFrame, text="Poisson Triangulation"))
        self.labels.append(tk.Label(labelFrame, text="Greedy Triangulation"))

        self.buttons.append(tk.Button(labelFrame, text="Option", command=lambda: self.change_option(0)))
        self.buttons.append(tk.Button(labelFrame, text="Option", command=lambda: self.change_option(1)))
        self.buttons.append(tk.Button(labelFrame, text="Option", command=lambda: self.change_option(2)))
        self.buttons.append(tk.Button(labelFrame, text="Option", command=lambda: self.change_option(3)))

        for i in range(0,len(self.labels)):
            self.labels[i].grid(row = i + 1 , column=0, sticky="W")
            self.buttons[i].grid(row=i +1 , column=1, sticky="W")

        initialVars = (0.025, 2.5, 100, pi / 4, pi / 18, 2 * pi / 3, 0)
        self.checkInt = tk.IntVar()
        self.checkInt.set(0)

        label_pcd = tk.Label(self.pcdFrame, text="PCD list")

        pcd_scrollbar = tk.Scrollbar(self.pcdFrame)
        self.pcd_list = tk.Listbox(self.pcdFrame,listvariable=[], yscrollcommand=pcd_scrollbar.set,
                                   width=40, selectmode=tk.EXTENDED)
        pcd_scrollbar.config(command=self.pcd_list.yview)
        self.update_list()
        self.pcd_list.grid(row=1, column=0, sticky="W")
        pcd_scrollbar.grid(row=1, column=1, sticky="E")

        # GRID
        label_pcd.grid(row=0, column=0, sticky="W")
        # DEF Entry


        # BTN
        button_1 = tk.Button(labelFrame, text="Make STL", command=lambda: self.stl_run())
        button_2 = tk.Button(labelFrame, text="Back", command=lambda: controller.show_frame("ConfigPage"))

        del_btn = tk.Button(self.pcdFrame, text="Del", command=self.delete)
        del_btn.grid(row=0, column=2, sticky="E")

        button_1.grid(row=9, column=2, sticky="W")
        button_2.grid(row=9, column=3, sticky="E")

        self.update()

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
        if not global_vars.is_same_list(self.pcd_list.get(0, tk.END) , global_vars.created_pcd):
            print "update list"
            self.pcd_list.delete(0 , tk.END)
            if global_vars.created_pcd:
                for item in global_vars.created_pcd:
                    self.pcd_list.insert(tk.END, item)

    def update(self):
        self.update_list()
        if len(self.pcd_list.get(0,tk.END)):
           # print "select"
            #print get_selection(self.pcd_list.curselection() ,0)
            new_selection = get_selection(self.pcd_list.curselection() ,0)
            if new_selection >= 0:
                self.pcd_list.selection_set(new_selection)
        super(STLPage, self).update()

        #self.after(1000,self.update)

    def change_option(self, id):
        print "change " + str(id)
        if (id == 0):
            self.controller.show_frame("OptionPage")
        if (id == 1):
            self.controller.show_frame("LaplacianPage")
        if (id == 2):
            self.controller.show_frame("PoissonPage")
        if (id == 3):
            self.controller.show_frame("GreedyPage")

    def stl_run(self):
        # file_list = self.pcd_list.curselection()
        # dodawanie parametow do triangulizacji

        for idx in self.pcd_list.curselection():
            print idx
           # print [os.path.join(os.path.split(global_vars.plugin_dir)[0], 'mesh.exe'), '-f',
             #   global_vars.created_pcd[int(idx)] ,'-p' ,stlParams.save_params(join(global_vars.current_project, 'params.ini' )) ]
            #subprocess.check_call(
              #  [os.path.join(os.path.split(global_vars.plugin_dir)[0], 'mesh.exe'), '-f',
              #   global_vars.created_pcd[int(idx)], '-p',
               #  stlParams.save_params(join(global_vars.current_project, 'params.ini'))])
            # '-p' ,'/home/dejna/PycharmProjects/CloudMesh/plugin/workspace/project/params.ini'
            subprocess.check_call( [os.path.join(os.path.split(global_vars.plugin_dir)[0], 'mesh'), '-f',  global_vars.created_pcd[int(idx)] ,'-p' ,stlParams.save_params(join(global_vars.current_project,'params.ini'))] )
            for item in global_vars.import_stl_from_log():
                print item
                global_vars.add_to_stl(item)
                #global_vars.created_stl.append(item)
            #copy2(change_ext( global_vars.created_pcd[int(idx)], '.stl'), global_vars.project_stl_folder)

           # global_vars.created_stl.append(change_ext( global_vars.created_pcd[int(idx)], '.stl'))

class OptionPage(tk.Frame):

    def __init__(self, parent , controller):
        tk.Frame.__init__(self,parent)

        self.controller = controller
        self.labelFrame = tk.LabelFrame(self, text="Main options for cpp", width=global_vars.dlab_width,
                                        height=global_vars.dlab_height, padx=10, pady=10)
        self.labelFrame.grid(row=0, column=0, sticky="NWSE", padx=10, pady=10, ipadx=5, ipady=5)


        self.options = {
            "type_triangulation" : [tk.Label(self.labelFrame , text="Type triangulation"), tk.Entry(self.labelFrame) ],
            "show_clustered" : [tk.Label(self.labelFrame , text="Show clusters" ), tk.Entry(self.labelFrame) ],
            "show_loaded" : [tk.Label(self.labelFrame , text="Show loaded cloud"), tk.Entry(self.labelFrame) ],
            "thread_num" :[tk.Label(self.labelFrame , text="Thread number"), tk.Entry(self.labelFrame) ],
            "visualisation" :[tk.Label(self.labelFrame , text="Visualization"), tk.Entry(self.labelFrame)],
            "normal_radius" :[tk.Label(self.labelFrame , text="Radius for search normals" ), tk.Entry(self.labelFrame) ],
            "normal_centroid" : [tk.Label(self.labelFrame , text="Calculate from centroid" ), tk.Entry(self.labelFrame) ],
            "normal_minus" : [tk.Label(self.labelFrame , text="Recalucate normals with minus"), tk.Entry(self.labelFrame) ],
        }
        i = 0
        for key,value in self.options.items():
            self.options[key][0].grid(row = i + 1 , column = 0 , sticky="W")
            self.options[key][1].grid(row = i + 1 , column = 1 , sticky="W")
            self.options[key][1].insert(tk.END, stlParams.getParamByKey(key))
            self.options[key][1].bind("<KeyPress>", input_validator)

            i = i + 1


        # BTN
        button_1 = tk.Button(self.labelFrame, text="Done", command = self.save_inputs)
        button_2 = tk.Button(self.labelFrame, text="Back", command=lambda: controller.show_frame("STLPage"))

        button_1.grid(row=len(self.options) + 1,column = 1 , sticky="W")
        button_2.grid(row=len(self.options) + 1,column = 0 , sticky="W")

    def save_inputs(self):
        for key, value in self.options.items():
            stlParams.set_param(key,value[1].get())

        self.show_correct_triangulation(stlParams.getParamByKey("type_triangulation"))

    def show_correct_triangulation(self, id):
        print id
        if (id == "0" ):
            self.controller.show_frame("LaplacianPage")
        elif (id == "1"):
            self.controller.show_frame("PoissonPage")
        elif (id == "2"):
            self.controller.show_frame("GreedyPage")
        else:
            print "Wrong type triangulation [0-2]!"


class LaplacianPage(tk.Frame):
    def __init__(self, parent , controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.labelFrame = tk.LabelFrame(self, text="Laplacian VTK params", width=global_vars.dlab_width,
                                        height=global_vars.dlab_height, padx=10, pady=10)
        self.labelFrame.grid(row=0, column=0, sticky="NWSE", padx=10, pady=10, ipadx=5, ipady=5)

        self.options = {
            "lap_max_iter": [tk.Label(self.labelFrame, text="Number max iteration"), tk.Entry(self.labelFrame)],
            "lap_convergence": [tk.Label(self.labelFrame, text="Specify a convergence criterion for the iteration process"), tk.Entry(self.labelFrame)],
            "lap_relaxation_factor": [tk.Label(self.labelFrame, text="Specify the relaxation factor for Laplacian smoothing."), tk.Entry(self.labelFrame)],
            "lap_edge_smoothing": [tk.Label(self.labelFrame, text="Specify the edge angle to control smoothing along edges "), tk.Entry(self.labelFrame)],
            "lap_boundary_smoothing": [tk.Label(self.labelFrame, text="Turn on/off the smoothing of vertices on the boundary of the mesh."), tk.Entry(self.labelFrame)],
        }
        i = 0
        for key, value in self.options.items():
            self.options[key][0].grid(row=i + 1, column=0, sticky="W")
            self.options[key][1].grid(row=i + 1, column=1, sticky="W")
            self.options[key][1].insert(tk.END, stlParams.getParamByKey(key))
            self.options[key][1].bind("<KeyPress>", input_validator)
            i = i + 1

        # BTN
        button_1 = tk.Button(self.labelFrame, text="Done", command=self.save_inputs)
        button_2 = tk.Button(self.labelFrame, text="Back", command=lambda: controller.show_frame("STLPage"))

        button_1.grid(row=len(self.options) + 1, column=1, sticky="W")
        button_2.grid(row=len(self.options) + 1, column=0, sticky="W")

    def save_inputs(self):
        for key, value in self.options.items():
            stlParams.set_param(key, value[1].get())


class PoissonPage(tk.Frame):
    def __init__(self, parent , controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.labelFrame = tk.LabelFrame(self, text="Poisson params", width=global_vars.dlab_width,
                                        height=global_vars.dlab_height, padx=10, pady=10)
        self.labelFrame.grid(row=0, column=0, sticky="NWSE", padx=10, pady=10, ipadx=5, ipady=5)

        self.options = {
            "poisson_confidence": [tk.Label(self.labelFrame, text="Number max iteration"), tk.Entry(self.labelFrame)],
            "poisson_depth": [
                tk.Label(self.labelFrame, text="Set the maximum depth of the tree that will be used for surface reconstruction"),
                tk.Entry(self.labelFrame)],
            "poisson_iso_divide": [
                tk.Label(self.labelFrame, text="Set the depth at which a block iso-surface extractor should be used to extract the iso-surface. ."),
                tk.Entry(self.labelFrame)],
            "poisson_radius": [
                tk.Label(self.labelFrame, text="Radius for search normals"),
                tk.Entry(self.labelFrame)],
            "poisson_samples_per_node": [
                tk.Label(self.labelFrame, text="Get the minimum number of sample points that should fall within an octree node \nas the octree construction is adapted to sampling density"),
                tk.Entry(self.labelFrame)],
            "poisson_solver_divide": [
                tk.Label(self.labelFrame, text="Set the the depth at which a block Gauss-Seidel solver is used to solve the Laplacian equation"),
                tk.Entry(self.labelFrame)],
        }
        i = 0
        for key, value in self.options.items():
            self.options[key][0].grid(row=i + 1, column=0, sticky="W")
            self.options[key][1].grid(row=i + 1, column=1, sticky="W")
            self.options[key][1].insert(tk.END, stlParams.getParamByKey(key))
            self.options[key][1].bind("<KeyPress>", input_validator)
            i = i + 1

        # BTN
        button_1 = tk.Button(self.labelFrame, text="Done", command=self.save_inputs)
        button_2 = tk.Button(self.labelFrame, text="Back", command=lambda: controller.show_frame("STLPage"))

        button_1.grid(row=len(self.options) + 1, column=1, sticky="W")
        button_2.grid(row=len(self.options) + 1, column=0, sticky="W")

    def save_inputs(self):
        for key, value in self.options.items():
            stlParams.set_param(key, value[1].get())

class GreedyPage(tk.Frame):
    def __init__(self, parent , controller):
        tk.Frame.__init__(self,parent)


class AbaqusPage(Page):
    def __init__(self, parent, controller):
        Page.__init__(self, parent)
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
            self.enties.append(tk.Entry(self.labelFrame , width=60))
            self.enties[i].grid(row=i , column=1,sticky="W")
        print "stl --"+ global_vars.current_stl
        self.enties[0].insert(0,global_vars.current_stl)
        self.enties[1].insert(0,get_filename_from_path(global_vars.current_stl))
        self.enties[2].insert(0,global_vars.nodeTolerance)

        self.run_abaqus_stl = tk.Button(self.labelFrame, text="To Abaqus" , command =  self.stl_abaqus )
        self.run_abaqus_stl.grid(row=3,column=1,sticky="EW", padx=10,pady=10)

        self.back_btn = tk.Button(self.labelFrame, text="Back", command=lambda: controller.show_frame("ConfigPage"))
        self.back_btn.grid(row=3,column=0, sticky="E", padx=10,pady=10)

    def update_enties(self):
        self.enties[0].delete(0,tk.END)
        self.enties[0].insert(0,global_vars.current_stl)

    def update(self):
        self.update_enties()
        super(AbaqusPage, self).update()

    def stl_abaqus(self):
        params = []

        for item in self.enties:
            params.append(item.get())
        print params

        if global_vars.DEBUG==False :
            from plugin.utils.abaqus import stl_to_abaqus
            stl_to_abaqus(params[0],params[1],params[2])








