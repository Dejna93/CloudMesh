# coding=UTF-8
import Tkinter as tk
from stlOper import FileOperation

from plugin.utils.project import add_project, open_project
from plugin.config import global_vars

# pages

from plugin.gui.pages import StartPage, ConfigPage, STLPage, AbaqusPage


class App(tk.Tk):
    fileOperation = FileOperation()

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.iconbitmap(self, default=global_vars.icon)
        tk.Tk.wm_title(self, global_vars.title)
        self.protocol("WM_DELETE_WINDOW", self.quit)
        container = tk.Frame(self)
        container.grid(row=0, column=0)
        # container.pack(side="top",fill="both", expand=True)
        # container.grid_rowconfigure(0, weight=1)
        # container.grid_columnconfigure(0, weight=1)
        # global_vars.dump_vars()
        global_vars.setup_images()

        self.menubar = tk.Menu(self)
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label="New Project", command=lambda: add_project(root=self))
        self.file_menu.add_command(label="Open Project", command=lambda: open_project(root=self))
        self.file_menu.add_command(label="Exit")
        self.menubar.add_cascade(label="Project", menu=self.file_menu)

        self.config(menu=self.menubar)

        self.frames = {}

        for F in (StartPage, ConfigPage, STLPage, AbaqusPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        frame.update()
        frame.event_generate("<<ShowFrame>>")

    def quit(self):
        global_vars.dump_last_project()
        self.destroy()


def run_gui(debug=False):
    app = App()
    global_vars.DEBUG = debug
    app.minsize(width=global_vars.window_width, height=global_vars.window_height)
    app.mainloop()


if __name__ == "__main__":
    print "RUNNING IN DEBUG MODE!"
    # global_vars.dump_vars()
    run_gui(True)
