import Tkinter as tk
import ttk as ttk
import tkFileDialog

FONT = ("Times New Roman", 8)


class Capp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Output initializer")

        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)
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

        for F in (StartPage, PageOne, ConfigPage):
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
        button1 = ttk.Button(self, text="OK", command=lambda: controller.show_frame("ConfigPage"))
        button1.grid(row=1, column=1)
        button2 = ttk.Button(self, text="Quit", command=lambda: StartPage.quit(self))
        button2.grid(row=1, column=2)


class ConfigPage(tk.Frame):
    filename = ''

    def __init__(self, parent , controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.grid(row=0, column=0, sticky=tk.NSEW)
        self.file_opt = options = {}

        labelFrame_1 = tk.LabelFrame(self, text=u"Specify Output directory", height="200", padx=10, pady=10)
        labelFrame_1.pack(fill="both", padx=5, pady=5)

        label_1 = tk.Label(labelFrame_1, text=u"Text file path", bg="white")
        label_1.pack(side=tk.LEFT, padx=20)

        self.entry_1 = tk.Entry(labelFrame_1, bd=2, width=50)
        self.entry_1.pack(side=tk.LEFT, fill=tk.X, padx=20)

        labelFrame_2 = tk.LabelFrame(self, text="Operations", height=100, padx=10, pady=10)
        labelFrame_2.pack(fill="both", padx=5, pady=5)

        label_2 = tk.Label(labelFrame_2, text="Check file")
        label_2.pack(side=tk.LEFT, padx=20)

        btn_2 = tk.Button(labelFrame_2, text="Valid", command=lambda: self.fileoper.validate(self.filename))
        btn_2.pack(side=tk.LEFT, padx=10)

        label_2 = tk.Label(labelFrame_2, text="Create STL")
        label_2.pack(side=tk.LEFT, padx=10)
        btn_3 = tk.Button(labelFrame_2, text="OK", command=lambda: self.check_filepath(controller))
        btn_3.pack(side=tk.LEFT, padx=10)

        label_3 = tk.Label(labelFrame_2, text="Import Geometry")
        label_3.pack(side=tk.LEFT, padx=10)

        btn_4 = tk.Button(labelFrame_2, text="Import")
        btn_4.pack(side=tk.LEFT, padx=10)


    def askopenfile(self):
        self.filename = tkFileDialog.askopenfilename(**self.file_opt)

        if self.filename:
            print self.filename
            self.set_entry(self.filename)
            return open(self.filename, 'r')

    def set_entry(self, text):
        self.entry_1.delete(0, tk.END)
        self.entry_1.insert(0, text)

    def check_filepath(self,controller):

        if(self.filename):
            controller.show_frame("STLPage")

    def opennew(self):
        print "opening"


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

    def run_gui(self):
        app = Capp()
        app.minsize(width=400,height=400)
        app.mainloop()
