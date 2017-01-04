import Tkinter as tk

class FileList(tk.Listbox):

    def __init__(self, master , cnf={}, **kw):
        tk.Widget.__init__(self,master,'listbox',cnf,kw)

