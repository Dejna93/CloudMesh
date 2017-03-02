# coding=UTF-8

import os
import subprocess
import tkFileDialog
import Tkinter as tk
from shutil import copy2
from sys import platform
from tkMessageBox import showerror
from plugin.config import storage
from plugin.utils.oso import join, clean_path
from plugin.utils.converter import convert_txt_to_pcd, convert_csv_to_pcd
from plugin.utils.params import stlParams


class Controller(object):
    def __init__(self, page):
        self.page = page

    def back_page(self, name):
        self.page.controller.show_frame(name)


class ConfigController(Controller):
    def __init__(self, page):
        Controller.__init__(self, page)

    def select_listbox_txt(self, event):
        if self.page.focus_txt:
            widget = event.widget
            if len(widget.curselection()) != 0:
                storage.update_currentfile(widget.get(widget.curselection()[0]))
                self.set_entry(storage.current_filename)  # global.current

    def select_listbox_stl(self, event):
        if self.page.focus_stl:
            widget = event.widget
            if len(widget.curselection()) != 0:
                storage.update_currentstl(widget.get(widget.curselection()[0]))

    def delete_item(self):
        print "ss"
        if not self.page.focus_txt:
            pass
        if not self.page.focus_stl:
            pass
        if self.page.txt_list.curselection():
            # deletefile
            selected_file = self.page.txt_list.curselection()[0]
            storage.del_file_open(self.page.txt_list.get(selected_file), 0)
            self.page.txt_list.delete(selected_file)

        if self.page.stl_list.curselection():
            for selection in self.page.stl_list.curselection():
                storage.del_file_open(self.page.stl_list.get(selection), 1)
                self.page.stl_list.delete(selection)

    def add_file_txt(self):
        if storage.workspace_dir == storage.current_project or storage.current_project == '':
            showerror("Nie wybrano projektu", "Prosze wybrać projekt w ktorym \n beda zapisywac sie dane")
        else:

            add_file = tkFileDialog.askopenfilename(**storage.dialog_option_txt())
            print "closed"
            if add_file != '':
                folder_dst = storage.project_points_folder if storage.current_filename[
                                                              -3:] != 'stl' else storage.project_stl_folder

                if not os.path.exists(join(folder_dst, os.path.split(add_file)[1])):
                    # print "Coping " + add_file +" to " + global_vars.project_points_folder + "/"+self.get_filename_from_path(add_file)

                    copy2(add_file, storage.project_points_folder)
                    add_file = join(folder_dst, storage.get_filename_from_path(add_file)).replace("\\", "/")
                else:
                    add_file = join(folder_dst, os.path.split(add_file)[1]).replace("\\", "/")

                if add_file and add_file[-3:] != 'stl':
                    if not add_file in storage.files_opened:
                        storage.files_opened.append(add_file)
                        self.set_entry(add_file)
                        self.page.txt_list.insert(0, add_file)
                else:
                    if not add_file in storage.created_stl:
                        storage.created_stl.append(add_file)
                        self.set_entry(add_file)
                        # self.stlList.insert(0, self.get_filename_from_path(add_file))

                storage.current_filename = add_file if add_file[-3:] != 'stl' else ''
                storage.current_stl = add_file if add_file[-3:] == 'stl' else ''

                # self.set_entry(global_vars.current_filename)
                # self.txt_list.insert(0, self.get_filename_from_path(global_vars.current_filename))
            else:
                showerror("Nie wybrano pliku", "Prosze wskazać plik do otwarcia")

    def add_file_stl(self):
        print "asds"
        add_file = tkFileDialog.askopenfilename(**storage.dialog_option_stl())
        if add_file != '':
            storage.add_to_stl(add_file)

    def switch_to_stl_page(self):
        if storage.current_filename:
            if storage.current_filename[-3:] == 'txt':
                storage.created_pcd.append(convert_txt_to_pcd(storage.current_filename))
            if storage.current_filename[-3:] == 'csv':
                convert_csv_to_pcd(storage.current_filename)
            self.page.controller.show_frame("STLPage")
        else:
            print "Select file to convert"

    def switch_to_abaqus_page(self):
        if self.page.stl_list.curselection() and storage.DEBUG == False:
            for item in self.page.stl_list.curselection():
                from plugin.utils.abaqus import stl_to_abaqus
                stl_to_abaqus(self.page.stl_list.get(item),
                              storage.get_filename_from_path(self.page.stl_list.get(item)[:-4]), "")
        else:
            self.page.controller.show_frame("AbaqusPage")

    def txt_listbox_focused(self, event):
        self.page.focus_txt = event.widget

    def txt_listbox_unfocused(self, event):
        self.page.focus_txt = None

    def stl_listbox_focused(self, event):
        self.page.focus_stl = event.widget

    def stl_listbox_unfocused(self, event):
        self.page.focus_stl = None

    def set_entry(self, text):
        self.page.entry_1.delete(0, tk.END)
        self.page.entry_1.insert(0, text)


class StlController(Controller):
    def __init__(self, page):
        Controller.__init__(self, page)

    def delete_item(self):
        if self.page.pcd_list.curselection():
            pos = 0
            for item in self.page.pcd_list.curselection():
                index = item - pos
                storage.del_file_pcd(self.page.pcd_list.get(item))
                self.page.pcd_list.delete(index, index)
                pos = pos + 1

    def add_file_pcd(self):

        add_file = tkFileDialog.askopenfilename(**storage.dialog_option_pcd())
        if add_file != "":
            storage.add_to_pcd(add_file)

    def run_external_exec(self):
        for idx in self.page.pcd_list.curselection():
            program = "mesh.exe"
            if platform == "linux" or platform == "linux2":
                # LINUX
                program = "mesh"
            subprocess.check_call([os.path.join(os.path.split(storage.plugin_dir)[0], program), '-f',
                                   clean_path(storage.created_pcd[int(idx)]), '-p',
                                   clean_path(stlParams.save_params(join(storage.current_project, 'params.ini')))])
            for item in storage.import_stl_from_log():
                storage.add_to_stl(item)

    def back_page(self):
        super(StlController, self).back_page("ConfigPage")

    def pcd_listbox_focus(self, event):
        self.page.focus = event.widget

    def pcd_listbox_unfocused(self, event):
        self.page.focus = None
