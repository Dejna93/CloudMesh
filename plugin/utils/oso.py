import os.path
import platform

def join(path, *args):
    for arg in args:
        path = os.path.join(path,arg)
    if platform.system() == 'Windows':
        return path.replace("\\","/")
    else:
        return path.replace("//","/")