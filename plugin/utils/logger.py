import datetime
import sys
from colorsys import *

from plugin.utils.oso import join


class Singelton(type):
    def __init__(cls, name, bases, dict):
        super(Singelton, cls).__init__(name, bases, dict)
        cls.instance = None

    def __call__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(Singelton, cls).__call__(*args, **kwargs)
        return cls.instance


class Logger(object):
    __metaclass__ = Singelton

    RED = "\033[1;31m"
    RESET = "\033[0;0m"

    def log(self, message):
        self.reset_console()
        print message

    def error(self, message):
        self.error_console()
        print message

    def error_console(self):
        sys.stdout.write(self.RED)

    def reset_console(self):
        sys.stdout.write(self.RESET)


class FileLogger(Logger):
    def log(self, message):
        message = "{ts} - {msg}".format(ts=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                        msg=message)
        super(FileLogger, self).log(message)

    def error(self, message):
        message = "{ts} - {msg}".format(ts=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), msg=message)
        super(FileLogger, self).error(message)


Log = FileLogger()
