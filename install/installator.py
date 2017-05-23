from zipfile import ZipFile
from shutil import copy2, rmtree
import os
import string
import random

N = 40
PACKAGE_ZIP = os.path.join(os.getcwd(), 'dll.zip')
PASSWORD = "zaq1@WSX"
WIN_DIR = os.path.join("c:\\temp\\windows")
TEMP_DIR = os.path.join("c:\\temp")
TEMP_NAME = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))
TEMP_FILEPATH = os.path.join(TEMP_DIR, TEMP_NAME)

if not os.path.exists(TEMP_FILEPATH):
    os.makedirs(TEMP_FILEPATH)

print TEMP_FILEPATH


def dezip_to_temp():
    with ZipFile(PACKAGE_ZIP) as file:
        file.extractall(path=TEMP_FILEPATH, pwd=PASSWORD)
        copy_windows(get_filepaths(TEMP_FILEPATH))
        rmtree(TEMP_FILEPATH)


def get_filepaths(filepath):
    files = []
    for dirname, dirnames, filenames in os.walk(filepath):
        for filename in filenames:
            files.append(os.path.join(dirname, filename))
    return files


def copy_windows(files):
    print ""
    for file in files:
        import ntpath
        head, tail = ntpath.split(file)
        if not os.path.exists(TEMP_FILEPATH):
            os.makedirs(TEMP_FILEPATH)
        # print TEMP_FILEPATH
        copy2(file, join(WIN_DIR, tail))


def join(src, dst):
    return os.path.join(src)


dezip_to_temp()
