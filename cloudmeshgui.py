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


thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)

LARGE_FONT = ("Verdana", 12)
FILEPATH = ''


class Capp(tk.Tk):

    fileOperation = FileOperation()
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.iconbitmap(self,default=os.path.join(thisDir, 'assets\\agh.ico'))


        tk.Tk.wm_title(self,"Import Mesh to Abaqus")

        container = tk.Frame(self)

        container.pack(side="top",fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menu = tk.Menu(self)
        self.config(menu=menu)
        file = tk.Menu(menu)
        file.add_command(label="Open")
        file.add_command(label="Exit")

        help = tk.Menu(menu)
        help.add_command(label="Help")

        menu.add_cascade(label="File", menu=file)
        menu.add_cascade(label="Help", menu=help)

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


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.parent = parent
       # self.initGui()

        about = """
        //PL
            Plugin przeznaczony do stworzenia geometrii w Abaqusie z chmury punktów.
        Plik z chmurą punktów powinien być rozszerzenia .txt
        a punkty xyz powinny być w kolumnach odzielone od siebie 'spacją lub tabulatorem'

        //ENG
            This plugin is for budatest something mesh qform something \n
            xyz with space and tab
        """
        label_1 = ttk.Label(self, text=about,padding=10)
        label_1.grid(row=0, columnspan=4)

        button1 = ttk.Button(self, text="OK" , command = lambda : controller.show_frame("ConfigPage"))
        button1.grid(row=1, column=1)
        button2 = ttk.Button(self, text="Quit" , command= lambda: StartPage.quit(self) )
        button2.grid(row=1  , column=2)


class ConfigPage(tk.Frame):

    def __init__(self, parent , controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        self.fileoper = FileOperation()
        # define options for opening or saving a file
        self.initOptions()

        #labels
        self.labelFramse()
        self.initLabels()
        self.initScrollList()
        self.initEntry()
        self.initButtons()
        self.manageGrid()


    def initOptions(self):
        self.fileopt = options = {}
        options['defaultextension'] = '.txt'
        options['filetypes'] = [('text files', '.txt'),('Point cloud data', '.pcd')]
        options['initialdir'] = thisDir
        options['initialfile'] = ''
        options['parent'] = self
        options['title'] = 'Open file to import'

    def labelFramse(self):
        self.labelFrame_1 = tk.LabelFrame(self, text="Specify Txt File", height=200, padx=10, pady=10)
        self.labelFrame_2 = tk.LabelFrame(self, text="Operations", height=200, padx=10, pady=10)
        self.labelFrame_3 = tk.LabelFrame(self, text="STL file", height=200, padx=10, pady=10)

    def initLabels(self):
        self.label_1 = tk.Label(self.labelFrame_1, text="Txt file name", bg="white")
        self.label_2 = tk.Label(self.labelFrame_2, text="Check file")
        self.label_3 = tk.Label(self.labelFrame_2, text="Create STL")
        self.label_4 = tk.Label(self.labelFrame_2, text="Import Geometry")

    def initEntry(self):
        self.entry_1 = tk.Entry(self.labelFrame_1, bd=2, width=50)

    def initButtons(self):
        im = Image.open(os.path.join(thisDir,"assets\open.png"))
        ph = ImageTk.PhotoImage(im)
        self.btn_1 = tk.Button(self.labelFrame_1, image=ph, command=self.askopenfile)
        self.btn_2 = tk.Button(self.labelFrame_2, text="Valid")
        self.btn_3 = tk.Button(self.labelFrame_2, text="OK", command=lambda: self.check_filepath(self.controller))
        self.btn_4 = tk.Button(self.labelFrame_2, text="Import")
        self.btn_del = tk.Button(self.labelFrame_3, text="Del" , command = self.delete )

        self.btn_1.image = ph

    def initScrollList(self):
        self.focus_box = None
        self.scrollbar = tk.Scrollbar(self.labelFrame_3)
       # self.stlList = tk.Listbox(self.labelFrame_3, yscrollcommand=self.scrollbar.set, width=50)
        self.stlList = FileList(self.labelFrame_3,yscrollcommand=self.scrollbar.set, width=50)
        self.stlList.bind("<FocusIn>", self.box_focused)
        self.stlList.bind("<FocusOut>", self.box_unfocused)
        self.scrollbar.config(command=self.stlList.yview)



    def manageGrid(self):
        self.labelFrame_1.grid(row=0, columnspan=8, sticky='NSWE', padx=10, pady=10)
        self.labelFrame_2.grid(row=2, column=0, sticky="NSWE", padx=10, pady=10)
        self.labelFrame_3.grid(row=4, column=0 , sticky="NSWE", padx=20)
        #----------
        self.label_1.grid(row=1,column=1,sticky="W")
        self.label_2.grid(row=3, column=1, sticky="W", padx=10)
        self.label_3.grid(row=3, column=4 , sticky="W", padx=10)
        self.label_4.grid(row=3, column=6 , sticky="W", padx=10)
        #----------
        self.btn_1.grid(row=1, column=3, sticky="W", padx=10)
        self.btn_2.grid(row=3, column=2, sticky="W", padx=5)
        self.btn_3.grid(row=3, column=5, sticky="W", padx=5)
        self.btn_4.grid(row=3, column=7, sticky="W", padx=20)
        self.btn_del.grid(row=5,column=3, sticky="E", padx=10)
        #----------
        self.scrollbar.grid(rowspan=5, row=5, column=1, sticky="WE")
        self.stlList.columnconfigure(0, weight=1)
        self.stlList.grid(row=5,column=2 ,sticky="WE",padx=10 , pady=10)
        #---------
        self.entry_1.grid(row=1, column=2, sticky="E", padx=10)

    def box_focused(self,event):
        self.focus_box = event.widget

    def box_unfocused(self,event):
        self.focus_box=None


    def delete(self):
        if not self.focus_box: return
        selection = self.stlList.curselection()
        if selection:
            self.focus_box.delete(selection[0])




    def askopenfile(self):
        Capp.fileOperation.filename = tkFileDialog.askopenfilename(**self.fileopt)

        if Capp.fileOperation.filename:

            self.set_entry(Capp.fileOperation.filename)
            self.stlList.insert(0, Capp.fileOperation.filename)
            return open(Capp.fileOperation.filename,'r')

    def set_entry(self, text):
        self.entry_1.delete(0,tk.END)
        self.entry_1.insert(0,text)

    def check_filepath(self,controller):

        if Capp.fileOperation.filename:
            controller.show_frame("STLPage")


    def opennew(self):
        print "opening"

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

        filename = Capp.fileOperation.filename
        if  Capp.fileOperation.filename[-3:] == "txt":
            filename = Capp.fileOperation.txtTopcd(Capp.fileOperation.filename)

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
    app = Capp()
    app.minsize(width=400,height=400)
    app.mainloop()
