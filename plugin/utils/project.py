# coding=UTF-8
import os
import tkFileDialog
from ..config import global_vars

def add_project(parent):
    dir_opt = options = {}
    options['initialdir'] = global_vars.workspace_dir
    options['mustexist'] = True
    options['parent'] = parent
    options['title'] = 'Dodaj projekt'
    folder = tkFileDialog.askdirectory(**dir_opt)
    if folder:
        print "dodaj foldery"
        global_vars.current_project = folder
        create_folder(folder+"\\points")
        create_folder(folder+"\\stl")
    if not folder:
        raise ValueError("Wybierz folder")

def create_folder(name):
    try:
        print name
        if not os.path.exists(name):
            os.makedirs(name)
    except OSError:
        if not os.path.isdir(name):
            raise

def open_project(parent):
    dir_opt = options = {}
    options['initialdir'] = global_vars.workspace_dir
    options['mustexist'] = True
    options['parent'] = parent
    options['title'] = 'Otwórz projekt'
    folder = tkFileDialog.askdirectory(**dir_opt)
    if folder:
        global_vars.current_project = folder
    if not folder:
        raise ValueError("Wybierz folder")



