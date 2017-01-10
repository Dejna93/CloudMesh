from __future__ import with_statement
import os
from PIL import Image, ImageTk


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

        self.window_width = 400
        self.window_height = 300

        self.dlab_width = 350
        self.dlab_height = 250

        self.plugin_dir = os.path.dirname(os.path.abspath(__file__))

        self.workspace_dir = os.path.join(self.plugin_dir,"workspace")

        self.current_project = os.path.join(self.plugin_dir,"workspace")

        self.project_points_folder = ""
        self.project_stl_folder = ""

        self.icon = os.path.join(self.plugin_dir, 'assets\\agh.ico')
        self.ico_btn_open = os.path.join(self.plugin_dir, "assets\\open.png")

        self.title = "Import Mesh to Abaqus"

        self.files_selected = []
        self.files_opened = []
        self.current_filename = ''
        self.created_stl = []

        self.stl_param = []

        self.setup_workspace()
        self.init_project()

    def setup_workspace(self):
        try:
            if not os.path.exists(self.workspace_dir):
                os.makedirs(self.workspace_dir)
        except OSError:
            if not os.path.isdir(self.workspace_dir):
                raise

    def setup_images(self):
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
            for item in self.files_opened:
                if item != self.files_opened[-1]:
                    file.write(item+";")
                else:
                    file.write(item)
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
                            self.update_project_dir(line[4:])
                        else:
                            canContinue = False
                file.close()
        except EnvironmentError:
            print "Plugin.ini not found"
        try:
            if canContinue:
                with open(os.path.join( self.current_project ,"\\project.ini"),"r") as file:
                    for line in file.readlines():
                        print line
                        if line[:6] =='files=' and len(line) != 6:
                            self.files_opened = line[6:].split(';')
                            print self.files_opened
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
                print "COMBOBOOO"
                self.files_opened.remove(file_name)
        print self.files_opened


    def update_project_dir(self,name):
        self.current_project = name
        self.project_points_folder = os.path.join(self.current_project, "points")
        self.project_stl_folder = os.path.join(self.current_project, "stl")
        print "UPDATE_DIR" + self.current_project
global_vars = PluginConfig()


