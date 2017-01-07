import os
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

        self.icon = os.path.join(self.plugin_dir, 'assets\\agh.ico')
        self.ico_btn_open = os.path.join(self.plugin_dir, "assets\\open.png")

        self.title = "Import Mesh to Abaqus"

        self.files_selecteced = []

        self.current_filename = ''
        self.created_stl = []

        self.stl_param = []

    def dump_vars(self):
        print "WINDOW WIDHT" + str(self.window_width)
        print "WINDOW HEIGHT" + str(self.window_height)
        print "PLUGIN DIR" + str(self.plugin_dir)

global_vars = PluginConfig()

