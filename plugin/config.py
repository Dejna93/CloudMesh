from __future__ import with_statement
from collections import Iterable
import os
from shutil import copy2
from sys import version
from plugin.utils.params import stlParams
from plugin.utils.oso import join, clean_path
if version[:3] >= '3':
    from PIL import Image, ImageTk


class Singelton(type):
    def __init__(cls, name, bases, dict):
        super(Singelton, cls).__init__(name, bases, dict)
        cls.instance = None

    def __call__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(Singelton, cls).__call__(*args, **kwargs)
        return cls.instance


class PluginConfig(object):
    __metaclass__ = Singelton

    def __init__(self):

        self.DEBUG = False
        # wersja do ktorej sie pisalo
        self.PYTHON_VERSION = '3'
        self.window_width = 520
        self.window_height = 380

        self.dlab_width = 510
        self.dlab_height = 380

        self.plugin_dir = os.path.dirname(os.path.abspath(__file__))

        self.workspace_dir = join(self.plugin_dir, "workspace")

        self.current_project = join(self.plugin_dir, "workspace")
        self.profile_folder = join(self.workspace_dir, "profiles")
        self.project_points_folder = ""
        self.project_stl_folder = ""

        if version[:3] >= self.PYTHON_VERSION:
            self.icon = os.path.join(self.plugin_dir, 'assets\\agh.ico')
            self.ico_btn_open = os.path.join(self.plugin_dir, "assets\\open.png")
        else:
            self.icon = ''
            self.ico_btn_open = ''
        self.projects_dirs = []

        self.files_opened = []
        self.current_filename = ''
        self.created_stl = []

        self.current_stl = ""

        self.created_pcd = []

        self.stl_param = []

        self.current_profile = ""
        self.profile_saved = []
        self.default_profile = join(os.path.dirname(os.path.abspath(__file__)), "utils/default.pl")
        self.profile_saved.append(self.default_profile)
        self.nodeTolerance = "1E-006"

        self.setup_workspace()
        self.init_project()

        self.title = "Import Mesh to Abaqus - Project -"

        self.can_change_model = 1

    def setup_workspace(self):
        try:
            if not os.path.exists(self.workspace_dir):
                os.makedirs(self.workspace_dir)
        except OSError:
            if not os.path.isdir(self.workspace_dir):
                raise

    def dump_vars(self):
        print "WORKSPACE DIR" + str(self.workspace_dir)
        print "PLUGIN DIR" + str(self.current_project)
        print "POINTS DIR" + str(self.project_points_folder)
        print "STL DIR" + str(self.project_stl_folder)
        print "FILES " + str(self.files_opened)

    def dump_last_project(self):

        with open(os.path.join(self.workspace_dir, "plugin.ini"), "w") as plugin:
            plugin.write("[!ProjectDir]\n")
            plugin.write("dir={0}".format(self.current_project))
            plugin.write("\n")
            plugin.write("dirs=")
            plugin.writelines(';'.join(self.projects_dirs))
            plugin.close()
        with open(join(self.workspace_dir, "profiles.ini"), "w") as profile:
            profile.writelines("\n".join(self.profile_saved))
            profile.close()
        # FIX Dumping project into workspace
        if self.current_project != self.workspace_dir:
            with open(join(self.current_project, "project.ini"), "w") as project:
                print "dumping files" + str(self.files_opened)
                project.write("[!ProjectDir]\n")
                project.write("dir={0}\n".format(self.current_project))
                project.write("[!PointsList]\n")
                project.write("files=")
                project.writelines(';'.join(self.files_opened))
                project.write('\n')
                project.write("[!StlList]\n")
                project.write("stl=")
                project.writelines(';'.join(self.created_stl))
                project.close()
        else:
            print "Project dir is the same as workspace dir!"

    def init_project(self):
        can_continue = True
        print "INITIAL PROJECT\n\n"
        try:
            with open(os.path.join(self.workspace_dir, "plugin.ini"), "r") as plugin:
                for line in plugin.readlines():
                    # print line
                    if line[:4] == 'dir=':
                        if os.path.exists(line[4:]):
                            self.update_project_dir(line[4:].replace("\\", "/"))
                        else:
                            can_continue = False
                    if line[:5] == "dirs=":
                        self.projects_dirs = self.convert_to_list(line[5:].strip().replace("\\", "/").split(';'))
                        plugin.close()
        except EnvironmentError:
            print "Plugin.ini not found"
        try:
            with open(join(self.workspace_dir, "profiles.ini"), "r") as profiles:
                for line in profiles.readlines():
                    print line
                    profile = line.strip().replace("\\", "/")
                    if not profile in self.profile_saved and profile != self.default_profile:
                        self.profile_saved.append(profile)
                profiles.close()
        except EnvironmentError:
            print "Profiles.ini not found"
        try:
            if can_continue:
                with open(os.path.join(self.current_project, "project.ini"), "r") as project:
                    for line in project.readlines():
                        if line[:6] == 'files=' and len(line) >= 6:
                            self.files_opened = self.convert_to_list(line[6:].strip().replace("\\", "/").split(';'))
                            self.current_filename = self.files_opened[0].strip().replace("\\", "/")
                        if line[:4] == 'stl=' and len(line) >= 4:
                            self.current_stl = self.convert_to_list(line[4:].strip().replace("\\", "/").split(';'))
                            self.current_stl = self.current_stl[0].strip()
                            self.created_stl = line[4:].strip().replace("\\", "/").split(';')
                            project.close()
        except EnvironmentError:
            print "Project.ini not found or project dir doesnt exists"

    def load_assets(self):
        print "load_assets"
        print self.current_project
        with open(join(self.current_project, "project.ini"), "r") as project:
            for line in project.readlines():
                line = line.replace("\n", "")
                if line[:4] == 'dir=' and len(line) != 4:
                    self.update_project_dir(line[4:].replace("\\", "/"))
                if line[:6] == 'files=' and len(line) != 6:
                    self.files_opened = self.convert_to_list(line[6:].strip().replace("\\", "/").split(';'))
                    self.current_filename = self.files_opened[0].strip().replace("\\", "/")
                if line[:4] == 'stl=' and len(line) != 4:
                    self.current_stl = self.convert_to_list(line[4:].strip().replace("\\", "/").split(';'))
                    self.current_stl = self.current_stl[0].strip()
                    self.created_stl = line[4:].strip().replace("\\", "/").split(';')
            project.close()

    @staticmethod
    def convert_to_list(value):
        if type(value) is list:
            return value
        elif type(value) is str and value != "":
            return value.split()
        return []

    def del_file_open(self, name, file_type):
        """
        Usuwanie sciezki do pliku z listy plikow gotowych do procesu stla
        ze stringa w tkinterze
        """
        if file_type == 0:
            for file_name in self.files_opened:
                # print file_name[-len(name):] + " " + name
                if file_name[-len(name):] == name:
                    self.files_opened.remove(file_name)
        if file_type == 1:
            for file_name in self.created_stl:
                if file_name[-len(name):] == name:
                    self.created_stl.remove(file_name)

    def del_file_pcd(self, name):
        """
        Usuwanie sciezki do pliku z listy plikow gotowych do procesu stla
        ze stringa w tkinterze
        """
        for file_name in self.created_pcd:
            # print file_name[-len(name):] + " " + name
            if file_name[-len(name):] == name:
                self.created_pcd.remove(file_name)
                # print self.files_opened

    def get_opened_file_by_name(self, name, ext):

        if ext == 'txt':
            for file_name in self.files_opened:
                if file_name[-len(name):] == name:
                    return file_name
        elif ext == 'stl':
            for file_name in self.created_stl:
                if file_name[-len(name):] == name:
                    return file_name
        return ''

    def update_currentfile(self, name):
        if self.current_filename != name:
            self.current_filename = self.get_opened_file_by_name(name, 'txt')

    def update_currentstl(self, name):
        if self.current_stl != name:
            self.current_stl = self.get_opened_file_by_name(name, 'stl')

    def update_project_dir(self, name):
        self.current_project = name
        self.project_points_folder = join(self.current_project, "points")
        self.project_stl_folder = join(self.current_project, "stl")
        # self.project_points_folder = os.path.join(self.current_project, "points").replace("\\","/")
        # self.project_stl_folder = os.path.join(self.current_project, "stl").replace("\\","/")
        print "UPDATE_DIR " + self.current_project
        if os.path.exists(join(self.project_stl_folder, 'output.log')):
            os.remove(join(self.project_stl_folder, 'output.log'))

        stlParams.set_param("points", self.project_points_folder)
        stlParams.set_param("stl", self.project_stl_folder)

    def add_project(self):
        self.current_filename = ''
        self.current_stl = ''
        self.current_stl = ''
        self.created_pcd = []
        self.created_stl = []
        self.files_opened = []

    @staticmethod
    def get_filename_from_path(filepath):
        import ntpath
        head, tail = ntpath.split(filepath)
        return tail

    @staticmethod
    def get_filepath_from_path(filepath):
        import ntpath
        head, tail = ntpath.split(filepath)
        return head

    def is_same_list(self, arr, build_list):
        for item in build_list:
            if not self.contains(item, arr):
                return False
        return True

    # ONLY FOR TRANSLATE LISTBOX TO LIST
    @staticmethod
    def contains(name, arr):
        for item in arr:
            if name == item:
                return True
        return False

    def get_items(self, arr, build_list):
        new_list = []
        for item in build_list:
            if not self.contains(item, arr):
                new_list.append(item)
        return new_list

    def update_project_params(self, project):
        self.current_project = project
        self.project_points_folder = join(self.current_project, "points")
        self.project_stl_folder = join(self.current_project, "stl")

    def update_point_files(self, points_files):
        # nadgraj obecne pliki
        if isinstance(points_files, Iterable):
            self.files_opened = []
            for pcd_file in points_files:
                if not pcd_file[-3:] in ('stl', 'pcd'):
                    self.files_opened.append(pcd_file)
                    # self.files_opened = points_files

    def update_stl_files(self, stl_files):

        if isinstance(stl_files, Iterable):
            print stl_files
            self.created_stl = stl_files

    def import_stl_from_log(self):
        stls = []
        with open(join(self.project_stl_folder, 'output.log')) as stl_file:
            for item in stl_file.readlines():
                stls.append(clean_path(item))
        return stls

    def add_to_stl(self, item):
        self.created_stl.append(clean_path(item))

    def add_to_pcd(self, item):
        self.created_pcd.append(clean_path(item))

    def add_to_profile(self, item):
        print item
        self.profile_saved.append(clean_path(item))

    def copy_file(self, filepath):
        folder_dst = self.project_points_folder if filepath[-3:] != 'stl' else self.project_stl_folder
        if not os.path.exists(join(folder_dst, os.path.split(filepath)[1])):
            copy2(filepath, join(folder_dst, os.path.split(filepath)[1]))
            return True
        return False

    @staticmethod
    def dialog_option_txt():
        options = {'defaultextension': '.txt',
                   'filetypes': [('Text files', '.txt'), ('Csv files', '.csv'), ('Point cloud data', '.pcd'),
                                 ('STL files', '.stl')],
                   'initialdir': storage.current_project if storage.current_project != '' and
                                                            storage.current_project != storage.workspace_dir
                   else storage.workspace_dir,
                   'initialfile': '', 'title': 'Open file to import'}

        return options

    def dialog_option_stl(self):
        options = {'defaultextension': '.stl', 'initialfile': '', 'title': 'Add Stl to project',
                   'filetypes': [('STL files', '.stl')], 'initialdir': self.project_stl_folder}

        return options

    @staticmethod
    def dialog_option_pcd():
        options = {'defaultextension': '.stl', 'initialfile': '', 'title': 'Add PCD to project',
                   'filetypes': [('PCD files', '.pcd')], 'initialdir': storage.project_points_folder}
        return options

    @staticmethod
    def dialog_option_profile():
        options = {'defaultextension': '.pl', 'initialfile': '', 'title': 'Add profile to project',
                   'filetypes': [('Profile files', '.pl')], 'initialdir': storage.profile_folder}
        return options

    def clear_storage(self):
        self.projects_dirs = []
        self.current_project = ''


storage = PluginConfig()
