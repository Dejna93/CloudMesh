# coding=UTF-8
import os

import tkFileDialog
from ..config import global_vars
from plugin.utils.oso import is_exists

def add_project(root):
    dir_opt = options = {}
    options['initialdir'] = global_vars.workspace_dir
    options['mustexist'] = True
   # options['parent'] = parent
    options['title'] = 'Dodaj projekt'
    folder = tkFileDialog.askdirectory(**dir_opt)
    root.wm_title('')
    root.wm_title(global_vars.title + " - Project -" + '/'.join(folder.split('/')[-4:]))

    if folder:
        global_vars.update_project_dir(folder)
    if not folder:
        raise ValueError("Wybierz folder")

def create_folder(name):
    try:
        if not os.path.exists(name):
            os.makedirs(name)
    except OSError:
        if not os.path.isdir(name):
            raise

def open_project(root):
    dir_opt = options = {}
    options['initialdir'] = global_vars.workspace_dir
    options['mustexist'] = True
    options['title'] = 'Otwórz projekt'
    folder = tkFileDialog.askdirectory(**dir_opt)
    root.wm_title('')
    root.wm_title(global_vars.title + " - Project -" + '/'.join(folder.split('/')[-4:]))

    if folder:
        global_vars.update_project_dir(folder)
    if not folder:
        raise ValueError("Wybierz folder")


def is_added(file):
    if is_exists(global_vars.project_points_folder, file):
        if file in global_vars.files_opened:
            return True
    return False


def is_project_open():
    if global_vars.workspace_dir == global_vars.current_project or global_vars.current_project == '':
        return False
    return True
