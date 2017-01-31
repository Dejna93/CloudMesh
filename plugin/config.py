from __future__ import with_statement
from collections import Iterable
import os
from sys import version

if version[:3] >= '2.7':
    from PIL import Image, ImageTk
from plugin.utils.oso import join

class Singelton(type):
    def __init__(cls , name , bases , dict):
        super(Singelton, cls).__init__(name,bases,dict)
        cls.instance = None
    def __call__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(Singelton, cls).__call__(*args,**kwargs)
        return cls.instance


class PluginConfig(object):

    __metaclass__ = Singelton

    def __init__(self,*args, **kwargs):


        for key, value in kwargs.iteritems():
            self.__dict__[key] = value

        self.DEBUG = False
        #wersja do ktorej sie pisalo
        self.PYTHON_VERSION ='2.7'
        self.window_width = 520
        self.window_height = 380

        self.dlab_width = 510
        self.dlab_height = 380


        self.plugin_dir = os.path.dirname(os.path.abspath(__file__))

        self.workspace_dir = join(self.plugin_dir,"workspace")

        self.current_project = join(self.plugin_dir,"workspace")

        self.project_points_folder = ""
        self.project_stl_folder = ""

        if version[:3] >= self.PYTHON_VERSION:
            self.icon = os.path.join(self.plugin_dir, 'assets\\agh.ico')
            self.ico_btn_open = os.path.join(self.plugin_dir, "assets\\open.png")
        else:
            self.icon = ''
            self.ico_btn_open =''


        self.files_opened = []
        self.current_filename = ''
        self.created_stl = []

        self.current_stl = ""

        self.created_pcd = []

        self.stl_param = []

        self.nodeTolerance = "1E-006"

        self.setup_workspace()
        self.init_project()

        self.title = "Import Mesh to Abaqus - Project -"

    def setup_workspace(self):
        try:
            if not os.path.exists(self.workspace_dir):
                os.makedirs(self.workspace_dir)
        except OSError:
            if not os.path.isdir(self.workspace_dir):
                raise

    def setup_images(self):

        if version[:3] >= self.PYTHON_VERSION:
            self.img_open_btn = Image.open(self.ico_btn_open)
            self.tk_img_open = ImageTk.PhotoImage(self.img_open_btn)

    def dump_vars(self):
        print "WORKSPACE DIR" + str(self.workspace_dir)
        print "PLUGIN DIR" + str(self.current_project)
        print "POINTS DIR" + str(self.project_points_folder)
        print "STL DIR" + str(self.project_stl_folder)
        print "FILES " + str(self.files_opened)

    def dump_last_project(self):
        with open(os.path.join(self.workspace_dir,"plugin.ini"), "w") as file:
            file.write("[!ProjectDir]\n")
            file.write("dir={0}".format(self.current_project))
            file.close()
        with open(os.path.join(self.current_project,"project.ini"), "w") as file:
            print "dumping files" + str(self.files_opened)
            file.write("[!ProjectDir]\n")
            file.write("dir={0}\n".format(self.current_project))
            file.write("[!PointsList]\n")
            file.write("files=")
            #for item in self.files_opened:
                #file.write(item)
            file.writelines(';'.join(self.files_opened))
            file.write('\n')
            file.write("[!StlList]\n")
            file.write("stl=")
            file.writelines(';'.join(self.created_stl))
            file.close()

    def init_project(self):
        canContinue = True
        print "INITIAL PROJECT\n\n"
        try:
            with open(os.path.join(self.workspace_dir ,"plugin.ini"),"r") as file:
                for line in file.readlines():
                    print line
                    if line[:4] =='dir=':
                        if os.path.exists(line[4:]):
                            self.update_project_dir(line[4:].replace("\\","/"))
                        else:
                            canContinue = False
                file.close()
        except EnvironmentError:
            print "Plugin.ini not found"
        try:
            if canContinue:
                with open(os.path.join( self.current_project ,"project.ini"),"r") as file:
                    for line in file.readlines():
                        print line
                        if line[:6] =='files=' and len(line) != 6:
                            self.files_opened = line[6:].strip().replace("\\","/").split(';')
                            self.current_filename = self.files_opened[0].strip().replace("\\","/")
                        if line[:4] =='stl=' and len(line) != 4 :
                            self.current_stl = line[6:].strip().replace("\\","/").split(';')
                            self.current_stl = self.current_stl[0].strip()
                    file.close()
        except EnvironmentError:
            print "Project.ini not found or project dir doesnt exists"

    def del_file_open(self,name):
        """
        Usuwanie sciezki do pliku z listy plikow gotowych do procesu stla
        ze stringa w tkinterze
        """
        for file_name in self.files_opened:
            #print file_name[-len(name):] + " " + name
            if file_name[-len(name):] == name:
                self.files_opened.remove(file_name)
        print self.files_opened

    def del_file_pcd(self, name):
        """
        Usuwanie sciezki do pliku z listy plikow gotowych do procesu stla
        ze stringa w tkinterze
        """
        for file_name in self.created_pcd:
            # print file_name[-len(name):] + " " + name
            if file_name[-len(name):] == name:
                self.created_pcd.remove(file_name)
        #print self.files_opened

    def get_opened_file_by_name(self, name, type):

        if type =='txt':
            for file_name in self.files_opened:
                if file_name[-len(name):] == name:
                    return file_name
        elif type =='stl':
            for file_name in self.created_stl:
                print "get_opened_by "+name + "filename" + file_name
                if file_name[-len(name):] == name:
                    print "found" + file_name
                    return file_name
        return ''

    def update_currentfile(self,name):
        if self.current_filename != name:
            self.current_filename = self.get_opened_file_by_name(name,'txt')

    def update_currentstl(self,name):
        if self.current_stl != name:
            self.current_stl = self.get_opened_file_by_name(name, 'stl')



    def update_project_dir(self,name):
        self.current_project = name
        self.project_points_folder = join(self.current_project,"points")
        self.project_stl_folder = join(self.current_project,"stl")
        #self.project_points_folder = os.path.join(self.current_project, "points").replace("\\","/")
        #self.project_stl_folder = os.path.join(self.current_project, "stl").replace("\\","/")
        print "UPDATE_DIR" + self.current_project


    def add_project(self):
        self.current_filename = ''
        self.current_stl = ''
        self.current_stl = ''
        self.created_pcd = []
        self.created_stl = []
        self.files_opened = []

    def get_filename_from_path(self, filepath):
        import ntpath
        head, tail = ntpath.split(filepath)
        return tail

    def is_same_list(self, list , build_list):
        for item in build_list:
            if not self.contains(item, list):
                return False
        return True

    # ONLY FOR TRANSLATE LISTBOX TO LIST
    def contains(self, name, list):
        for item in list:
            if name == item:
                return True
        return False

    def get_items(self, list ,build_list):
        new_list = []
        for item in build_list:
            if not self.contains(item , list):
                new_list.append(item)
        return new_list


    def update_project_params(self,project):
        self.current_project = project
        self.project_points_folder =  join(self.current_project,"points")
        self.project_stl_folder = join(self.current_project,"stl")

    def update_point_files(self, points_files):
        #nadgraj obecne pliki
        if isinstance(points_files , Iterable):
            self.files_opened = []
            for file in points_files:
                if not file[-3:] in ('stl', 'pcd'):
                    self.files_opened.append(file)
            #self.files_opened = points_files

    def update_stl_files(self, stl_files):

        if isinstance(stl_files, Iterable):
            self.created_stl = stl_files

global_vars = PluginConfig()



