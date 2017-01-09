# coding=UTF-8
import os
import tkFileDialog
from ..config import global_vars

def add_project():
    dir_opt = options = {}
    options['initialdir'] = global_vars.workspace_dir
    options['mustexist'] = True
   # options['parent'] = parent
    options['title'] = 'Dodaj projekt'
    folder = tkFileDialog.askdirectory(**dir_opt)
    if folder:
        global_vars.current_project = folder
        create_folder(folder+"/points")
        create_folder(folder+"/stl")
    if not folder:
        raise ValueError("Wybierz folder")

def create_folder(name):
    try:
        if not os.path.exists(name):
            os.makedirs(name)
    except OSError:
        if not os.path.isdir(name):
            raise

def open_project():
    dir_opt = options = {}
    options['initialdir'] = global_vars.workspace_dir
    options['mustexist'] = True
    options['title'] = 'Otwórz projekt'
    folder = tkFileDialog.askdirectory(**dir_opt)
    if folder:
        global_vars.current_project = folder
        global_vars.project_points_folder = folder+"/points"
        global_vars.project_stl_folder = folder + "/stl"
    if not folder:
        raise ValueError("Wybierz folder")



