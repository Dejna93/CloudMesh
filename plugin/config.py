from __future__ import with_statement
import os
from PIL import Image, ImageTk
class PluginConfig(object):

    instance = None

    def __init__(self,*args, **kwargs):

        for key, value in kwargs.iteritems():
            self.__dict__[key] = value

        self.window_width = 400
        self.window_height = 300

        self.dlab_width = 350
        self.dlab_height = 250

        self.plugin_dir = os.path.dirname(os.path.abspath(__file__))

        self.workspace_dir = self.plugin_dir + "\\workspace"

        self.current_project = self.plugin_dir + "\\workspace"


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
        print "WINDOW WIDHT" + str(self.window_width)
        print "WINDOW HEIGHT" + str(self.window_height)
        print "PLUGIN DIR" + str(self.plugin_dir)

    def dump_last_project(self):
        with open(self.workspace_dir + "\\plugin.ini", "w") as file:
            file.write("[!ProjectDir]\n")
            file.write("dir={0}".format(self.current_project))
            file.close()
        with open(self.current_project +"\\project.ini", "w") as file:
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
        try:

            with open(self.workspace_dir + "\\plugin.ini","r") as file:
                for line in file.readlines():
                    if line[:4] =='dir=':
                        print line[4:]
                        self.current_project = line[4:]
                file.close()
        except EnvironmentError:
            print "Plugin.ini not found"
        try:
            with open(self.current_project +"\\project.ini","r") as file:
                for line in file.readlines():
                    if line[:6] =='files=' and len(line) != 6:
                        self.files_opened = line[6:].split(';')
                        print self.files_opened
                file.close()
        except EnvironmentError:
            print "Plugin.ini not found"


global_vars = PluginConfig()

