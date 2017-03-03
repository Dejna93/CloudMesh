# coding=UTF-8

from math import pi
import Tkinter as tk
from plugin.config import storage
from plugin.utils.inputs import input_validator
from plugin.utils.oso import get_selection

from plugin.gui.controllers import ConfigController, StlController
from plugin.utils.params import stlParams
from plugin.utils.translation import Translation

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
            Plugin przeznaczony do generowanie PART`ów z podanego pliku tekstowego, struktura pliku dostępna w dokumentacji.
            Autor  Damian Hołuj.

        """
        self.start_labelframe = tk.LabelFrame(self, text="About", height=storage.dlab_height, padx=10, pady=10)
        self.start_labelframe.grid(row=0, column=0, sticky="NS", padx=10, pady=10)

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
        self.cls = ConfigController(self)

        self.focus_stl = None
        self.focus_txt = None

        # labels
        self.labelFramse()
        self.initLabels()

        self.initTxtScrollList()
        self.initSTLList()
        self.initEntry()
        self.initButtons()
        self.manageGrid()


    def labelFramse(self):
        self.labelFrame_1 = tk.LabelFrame(self, text="Specify Txt File", padx=10, pady=10)
        self.labelFrame_2 = tk.LabelFrame(self, text="Operations", padx=10, pady=10)
        self.labelFrame_3 = tk.LabelFrame(self, text="STL file", padx=10, pady=10)

    def initLabels(self):
        self.label_1 = tk.Label(self.labelFrame_1, text="Txt file name", bg="white")
        self.label_3 = tk.Label(self.labelFrame_2, text="Create STL")
        self.label_4 = tk.Label(self.labelFrame_2, text="STL to Abaqus")

    def initEntry(self):
        self.entry_1 = tk.Entry(self.labelFrame_1, bd=2, width=70)
        if storage.current_filename:
            self.entry_1.insert(0, storage.current_filename)

    def initButtons(self):
        self.btn_1 = tk.Button(self.labelFrame_1, text="Open", command=self.cls.add_file_txt)
        self.btn_3 = tk.Button(self.labelFrame_2, text="Convert",
                               command=self.cls.switch_to_stl_page)  # self.check_filepath(self.controller))
        self.btn_4 = tk.Button(self.labelFrame_2, text="Import to Abaqus", command=self.cls.switch_to_abaqus_page)
        self.btn_del = tk.Button(self.labelFrame_3, text="Del", command=self.cls.delete_item)
        self.btn_add = tk.Button(self.labelFrame_3, text="Add STL", command=self.cls.add_file_stl)


    def initTxtScrollList(self):

        self.txt_scrollbar = tk.Scrollbar(self.labelFrame_3)
        self.txt_list = tk.Listbox(self.labelFrame_3, listvariable=storage.files_opened,
                                   yscrollcommand=self.txt_scrollbar.set, width=90)
        self.txt_scrollbar.config(command=self.txt_list.yview)
        self.txt_list.bind("<FocusIn>", self.cls.txt_listbox_focused)
        self.txt_list.bind("<FocusOut>", self.cls.txt_listbox_unfocused)
        self.txt_list.bind("<Double-Button-1>", self.cls.select_listbox_txt)

        self.fill_listbox(self.txt_list, storage.files_opened)

    def initSTLList(self):
        self.stl_scrollbar = tk.Scrollbar(self.labelFrame_3)
        self.stl_list = tk.Listbox(self.labelFrame_3, yscrollcommand=self.txt_scrollbar.set, width=90,
                                   selectmode=tk.EXTENDED)
        self.stl_scrollbar.config(command=self.stl_list.yview)
        self.stl_list.bind("<FocusIn>", self.cls.stl_listbox_focused)
        self.stl_list.bind("<FocusOut>", self.cls.stl_listbox_unfocused)
        self.stl_list.bind("<Double-Button-1>", self.cls.select_listbox_stl)

        self.fill_listbox(self.stl_list, storage.created_stl)

    def fill_listbox(self, listbox, list):
        if list:
            for files in list:
                listbox.insert(tk.END, files)

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
        self.btn_del.grid(row=8, column=1, sticky="E", padx=10)
        self.btn_add.grid(row=8, column=0, sticky="E", padx=10)
        # ----------
        self.txt_scrollbar.grid(row=5, column=11, sticky="WE")
        self.txt_list.grid(row=5, column=0,columnspan=10, sticky="WE", padx=10, pady=10)

        self.stl_scrollbar.grid(row=7, column=11, sticky="WE")
        self.stl_list.grid(row=7, column=0, columnspan=10, sticky="WE", padx=10, pady=10)
        # ---------
        self.entry_1.grid(row=1, column=2, sticky="E", padx=10)



    def update(self):
        if not storage.is_same_list(self.txt_list.get(0, tk.END), storage.files_opened):
            self.txt_list.delete(0, tk.END)
            for item in sorted(storage.files_opened):
                self.txt_list.insert(tk.END, item)

        if not storage.is_same_list(self.stl_list.get(0, tk.END), storage.created_stl):
            self.stl_list.delete(0, tk.END)
            for item in sorted(storage.created_stl):
                self.stl_list.insert(tk.END, item)

        if self.focus_txt:
            self.txt_list.selection_set(get_selection(self.txt_list.curselection(), 0))
        if self.focus_stl:
            self.stl_list.selection_set(get_selection(self.stl_list.curselection(), 0))
        super(ConfigPage,self).update()


class STLPage(Page):
    def __init__(self, parent, controller):
        Page.__init__(self, parent)
        self.controller = controller
        self.cls = StlController(self)

        labelFrame = tk.LabelFrame(self, text="Triangulation options", width=storage.dlab_width,
                                   height=storage.dlab_height, padx=10, pady=10)
        labelFrame.grid(row=0, column=2, sticky='W', padx=10, pady=10, ipadx=5, ipady=5)
        self.pcdFrame = tk.LabelFrame(self, text="PCD Files", width=storage.dlab_width, padx=10, pady=10)
        self.pcdFrame.grid(row=1, column=0, columnspan=4, sticky="WE", padx=10, pady=10)

        self.buttons = []

        # self.labels.append(tk.Label(labelFrame, text="Greedy Triangulation"))

        self.buttons.append(tk.Button(labelFrame, text="General", width=35, command=lambda: self.change_option(0)))
        self.buttons.append(
            tk.Button(labelFrame, text="Laplacian Triangulation", width=35, command=lambda: self.change_option(1)))
        self.buttons.append(
            tk.Button(labelFrame, text="Poisson Triangulation", width=35, command=lambda: self.change_option(2)))
        #  self.buttons.append(tk.Button(labelFrame, text="Option", command=lambda: self.change_option(3)))

        for i in range(0, len(self.buttons)):
            # self.labels[i].grid(row = i + 1 , column=0, sticky="W")
            self.buttons[i].grid(row=i + 1, column=0, columnspan=2, sticky="W")

        initialVars = (0.025, 2.5, 100, pi / 4, pi / 18, 2 * pi / 3, 0)
        self.checkInt = tk.IntVar()
        self.checkInt.set(0)

        label_pcd = tk.Label(self.pcdFrame, text="PCD list")

        pcd_scrollbar = tk.Scrollbar(self.pcdFrame)
        self.pcd_list = tk.Listbox(self.pcdFrame, listvariable=[], yscrollcommand=pcd_scrollbar.set,
                                   width=90, selectmode=tk.EXTENDED)
        self.pcd_list.bind("<FocusIn>", self.cls.pcd_listbox_focus)
        self.pcd_list.bind("<FocusOut>", self.cls.pcd_listbox_unfocused)

        pcd_scrollbar.config(command=self.pcd_list.yview)
        self.update_list()
        self.pcd_list.grid(row=1, column=0, columnspan=5, sticky="W")
        pcd_scrollbar.grid(row=1, column=1, sticky="E")

        # GRID
        label_pcd.grid(row=0, column=0, sticky="W")
        # DEF Entry
        self.focus = None

        # BTN
        button_1 = tk.Button(labelFrame, text="Make STL", width=15, command=self.cls.run_external_exec)
        button_2 = tk.Button(labelFrame, text="Back", width=15, command=self.cls.back_page)

        del_btn = tk.Button(self.pcdFrame, text="Delete", width=15, command=self.cls.delete_item)
        del_btn.grid(row=2, column=1, sticky="E")
        add_btn = tk.Button(self.pcdFrame, text="Add", width=15, command=self.cls.add_file_pcd)
        add_btn.grid(row=2, column=2, sticky="E")
        button_1.grid(row=10, column=0, sticky="W")
        button_2.grid(row=10, column=1, sticky="E")

        self.update()


    def update_list(self):
        if (storage.current_filename[-3:] == 'pcd') & (storage.current_filename not in storage.created_pcd):
            self.pcd_list.delete(0, tk.END)
            self.pcd_list.insert(tk.END, storage.current_filename)
            storage.created_pcd.append(storage.current_filename)
        if not storage.is_same_list(self.pcd_list.get(0, tk.END), storage.created_pcd):
            self.pcd_list.delete(0 , tk.END)
            if storage.created_pcd:
                for item in storage.created_pcd:
                    self.pcd_list.insert(tk.END, item)

    def update(self):
        selected = self.pcd_list.curselection()
        self.update_list()
        if self.focus and len(selected) != 0:
            self.pcd_list.selection_set(selected[0])
        # if len(self.pcd_list.get(0,tk.END)):
        #self.pcd_list.selection_set(get_selection(self.pcd_list.curselection() ,0))
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


class OptionPage(Page):

    def __init__(self, parent , controller):
        Page.__init__(self, parent)
        self.controller = controller
        self.labelFrame = tk.LabelFrame(self, text="Main options for cpp", width=storage.dlab_width,
                                        height=storage.dlab_height, padx=10, pady=10)
        self.labelFrame.grid(row=0, column=0, sticky="NWSE", padx=10, pady=10, ipadx=5, ipady=5)

        self.option_dict = Translation().getDictByCategory("OptionPage")
        self.options = {}

        for key, value in self.option_dict.items():
            self.options[key] = [tk.Label(self.labelFrame, text=value), tk.Entry(self.labelFrame)]

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


class LaplacianPage(Page):
    def __init__(self, parent , controller):
        Page.__init__(self, parent)
        self.controller = controller
        self.labelFrame = tk.LabelFrame(self, text="Laplacian VTK params", width=storage.dlab_width,
                                        height=storage.dlab_height, padx=10, pady=10)
        self.labelFrame.grid(row=0, column=0, sticky="NWSE", padx=10, pady=10, ipadx=5, ipady=5)

        self.options = {}

        self.laplacian_dict = Translation().getDictByCategory("PoissonPage")

        for key, value in self.laplacian_dict.items():
            self.options[key] = [tk.Label(self.labelFrame, text=value), tk.Entry(self.labelFrame)]

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
        self.controller.show_frame("STLPage")


class PoissonPage(Page):
    def __init__(self, parent , controller):
        Page.__init__(self, parent)
        self.controller = controller
        self.labelFrame = tk.LabelFrame(self, text="Poisson params", width=storage.dlab_width,
                                        height=storage.dlab_height, padx=10, pady=10)
        self.labelFrame.grid(row=0, column=0, sticky="NWSE", padx=10, pady=10, ipadx=5, ipady=5)

        self.poisson_dict = Translation().getDictByCategory("PoissonPage")

        self.options = {}
        for key, value in self.poisson_dict.items():
            self.options[key] = [tk.Label(self.labelFrame, text=value), tk.Entry(self.labelFrame)]

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
            self.controller.show_frame("STLPage")


class GreedyPage(Page):
    def __init__(self, parent , controller):
        Page.__init__(self, parent)


class AbaqusPage(Page):
    def __init__(self, parent, controller):
        Page.__init__(self, parent)
        self.labelFrame = tk.LabelFrame(self, text="STL settings for import", width=storage.dlab_width,
                                        height=storage.dlab_height, padx=10, pady=10)
        self.labelFrame.grid(row=0 , column=0, sticky="NWSE", padx=10, pady=10, ipadx=5, ipady=5)

        self.nameLabel = tk.Label(self.labelFrame , text="File")
        self.modelLabel = tk.Label(self.labelFrame, text="Model name")
        self.nodeLabel = tk.Label(self.labelFrame, text="Merge tolerance")

        self.nameLabel.grid(row=0,column=0 , sticky="E" , padx=10)
        self.modelLabel.grid(row=1,column=0,sticky="E",  padx=10)
        self.nodeLabel.grid(row=2,column=0 , sticky="E",  padx=10)

        self.enties = []
        for i in range(0,3):
            self.enties.append(tk.Entry(self.labelFrame, width=90))
            self.enties[i].grid(row=i, column=1, sticky="W")
        #print "stl --"+ global_vars.current_stl

        self.enties[0].insert(0, storage.current_stl)
        self.enties[1].insert(0, "")
        self.enties[2].insert(0, storage.nodeTolerance)

        self.run_abaqus_stl = tk.Button(self.labelFrame, text="To Abaqus" , command =  self.stl_abaqus )
        self.run_abaqus_stl.grid(row=3,column=1,sticky="EW", padx=10,pady=10)

        self.back_btn = tk.Button(self.labelFrame, text="Back", command=lambda: controller.show_frame("ConfigPage"))
        self.back_btn.grid(row=3,column=0, sticky="E", padx=10,pady=10)

    def update_enties(self):
        self.enties[0].delete(0, tk.END)
        self.enties[0].insert(0, storage.current_stl)

    def update(self):
        self.update_enties()
        super(AbaqusPage, self).update()

    def stl_abaqus(self):
        params = []

        for item in self.enties:
            params.append(item.get())
            #  print params

        if storage.DEBUG == False :
            from plugin.utils.abaqus import stl_to_abaqus
            stl_to_abaqus(params[0],params[1],params[2])

