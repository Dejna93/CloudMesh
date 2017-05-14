# coding=UTF-8

import os
import subprocess
import tkFileDialog
import Tkinter as tk
from shutil import copy2
from sys import platform
from tkMessageBox import showerror, askyesnocancel
from plugin.config import storage
from plugin.utils.oso import join, clean_path, change_ext
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
                    # print "Coping " + add_file +" to " + global_vars.project_points_folder
                    # + "/"+self.get_filename_from_path(add_file)
                    copy2(add_file, storage.project_points_folder)
                    add_file = join(folder_dst, storage.get_filename_from_path(add_file)).replace("\\", "/")
                else:
                    add_file = join(folder_dst, os.path.split(add_file)[1]).replace("\\", "/")

                if add_file and add_file[-3:] != 'stl':
                    if add_file not in storage.files_opened:
                        storage.files_opened.append(add_file)
                        self.set_entry(add_file)
                        self.page.txt_list.insert(0, add_file)
                else:
                    if add_file not in storage.created_stl:
                        storage.created_stl.append(add_file)
                        self.set_entry(add_file)
                        # self.stlList.insert(0, self.get_filename_from_path(add_file))

                storage.current_filename = add_file if add_file[-3:] != 'stl' else ''
                storage.current_stl = add_file if add_file[-3:] == 'stl' else ''

                # self.set_entry(global_vars.current_filename)
                # self.txt_list.insert(0, self.get_filename_from_path(global_vars.current_filename))
            else:
                showerror("Nie wybrano pliku", "Prosze wskazać plik do otwarcia")

    @staticmethod
    def add_file_stl():
        add_file = tkFileDialog.askopenfilename(**storage.dialog_option_stl())
        if add_file != '':
            storage.copy_file(add_file)
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
        if self.page.stl_list.curselection() and not storage.DEBUG:
            for item in self.page.stl_list.curselection():
                from plugin.utils.abaqus import stl_to_abaqus
                stl_to_abaqus(self.page.stl_list.get(item),
                              storage.get_filename_from_path(self.page.stl_list.get(item)[:-4]), "")
        elif storage.current_stl != "":
            self.page.controller.show_frame("AbaqusPage")
        else:
            print "No selected STL files"

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
                pos += 1

    @staticmethod
    def add_file_pcd():
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

    def back_page(self, page="ConfigPage"):
        super(StlController, self).back_page(page)

    def pcd_listbox_focus(self, event):
        self.page.focus = event.widget

    def pcd_listbox_unfocused(self, event):
        self.page.focus = None


class AppController(Controller):
    def __init__(self, page):
        Controller.__init__(self, page)

    def view(self, frame):
        self.page.controller.show_frame(frame)


class OptionController(Controller):
    def __init__(self, page):
        Controller.__init__(self, page)

    def add_profile(self):
        add_profile = tk.Toplevel(self.page, width=300, height=300)
        add_profile.wm_geometry("300x100")
        add_profile.title("New profile")
        frame = tk.Frame(add_profile)
        frame.pack()
        bottom = tk.Frame(add_profile)
        bottom.pack(side=tk.BOTTOM)
        label = tk.Label(frame, text="Name profile")
        label.pack(side=tk.LEFT)
        entry = tk.Entry(frame)
        entry.pack(side=tk.LEFT)
        btn = tk.Button(bottom, text="Save", command=lambda: self.save_new_profile(add_profile, entry))
        btn.pack(side=tk.BOTTOM, expand=1, fill=tk.X)
        # add_profile = tkFileDialog.askopenfilename(**storage.dialog_option_profile())
        # if add_profile != "":
        #   print add_profile
        #  storage.add_to_profile(add_profile)

    def save_new_profile(self, window, entry):
        print entry.get()
        new_name = entry.get()
        if new_name != '':
            if new_name[3:] != ".pl":
                new_name = "%s%s" % (new_name, '.pl')
                print new_name
            print storage.default_profile
            print storage.profile_folder
            try:
                copy2(storage.default_profile, storage.profile_folder)
            except EnvironmentError:
                print "Error happended"
            else:
                print "OK"

            old_file = storage.get_filename_from_path(storage.default_profile)
            print old_file
            old_file = join(storage.profile_folder, old_file)
            print old_file
            new_file = join(storage.profile_folder, new_name)
            os.rename(old_file, new_file)
            storage.add_to_profile(new_file)
            print storage.profile_saved

        window.destroy()

    def open_profile(self):
        add_file = tkFileDialog.askopenfilename(**storage.dialog_option_profile())
        if add_file != "":
            print add_file
            storage.add_to_profile(add_file)

    def edit_profile(self):
        self.page.settings.relaod_tree(stlParams.load_param(storage.current_profile))

    def delete_profile(self):
        if storage.current_profile != '':
            if storage.current_profile[-10:] == 'default.pl':
                print "WARING YOU CANNOT REMOVE DEFUALT PROFILE"
            elif askyesnocancel("Remove profile", "Do you want to remove those profile?"):
                try:
                    os.remove(storage.current_profile)
                except OSError, e:
                    print "Error: %s - %s." % (e.filename, e.strerror)

                storage.profile_saved.remove(storage.current_profile)
                print storage.profile_saved
                storage.current_profile = ""

    def default_profile(self):
        self.page.settings.relaod_tree(stlParams.load_param(storage.default_profile))
        storage.current_profile = ""
        self.page.current_profile_entry.delete(0, tk.END)

    def profil_listbox_focused(self, event):
        self.page.focus_profile = event.widget

    def profil_listbox_unfocused(self, event):
        self.page.focus_profile = None

    def select_listbox_profil(self, event):
        if self.page.focus_profile:
            widget = event.widget
            if len(widget.curselection()) != 0:
                # storage.update_currentfile(widget.get(widget.curselection()[0]))
                print widget.get(widget.curselection()[0])
                storage.current_profile = widget.get(widget.curselection()[0])
                self.page.current_profile_entry.delete(0, tk.END)
                self.page.current_profile_entry.insert(0, storage.current_profile)
                # self.set_entry(widget.curselection()[0])  # global.current

    def set_entry(self, text):
        self.page.current_profile_entry.delete(0, tk.END)
        self.page.current_profile_entry.insert(0, text)

    def stl_listbox_focused(self, event):
        self.page.focus_stl = event.widget

    def stl_listbox_unfocused(self, event):
        self.page.focus_stl = None

    def edit_item(self):
        print self.page.tree.item(self.page.tree.selection())

        widget = tk.Toplevel(self.page, width=300, height=300)
        x = (widget.winfo_screenwidth() / 2) - (storage.window_width / 2)
        y = (widget.winfo_screenheight() / 2) - (storage.window_height / 2)
        widget.geometry('%dx%d+%d+%d' % (storage.window_width, storage.window_height, x, y))
        widget.wm_geometry("250x70")
        widget.title("Edit parametr")
        frame = tk.Frame(widget)
        frame.pack()
        bottom = tk.Frame(widget)
        bottom.pack(side=tk.BOTTOM)
        label = tk.Label(frame, text=self.page.tree.item(self.page.tree.selection())["text"])
        label.pack(side=tk.LEFT)
        entry = tk.Entry(frame)
        entry.insert(0, self.page.tree.item(self.page.tree.selection())["values"][0])
        entry.pack(side=tk.LEFT)
        btn = tk.Button(bottom, text="Save", command=lambda: self.save_editable_item(widget, entry))
        btn.pack(side=tk.BOTTOM, expand=1, fill=tk.X)

    def save_editable_item(self, widget, entry):
        id_item = self.page.tree.selection()
        value = entry.get()
        validate = False
        if self.is_int(value):
            value = int(value)
            validate = True
        elif self.is_float(value):
            value = float(value)
            validate = True
        if validate:
            self.page.tree.item(id_item, values=value)
            key = self.page.tree.item(id_item)["text"]
            stlParams.params[key] = value
            # stlParams.params[key] = value
        else:
            print "Wrong type !!!"
        widget.destroy()

    @staticmethod
    def is_int(string):
        try:
            int(string)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_float(string):
        try:
            float(string)
            return True
        except ValueError:
            return False

    def save_profile(self):
        print stlParams.params
        if storage.current_profile != '':
            stlParams.save_profile(storage.current_profile)
