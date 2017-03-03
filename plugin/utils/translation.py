from xml.dom.minidom import parse
import xml.dom.minidom

from plugin.utils.oso import join
from plugin.config import storage


class Translation(object):
    def __init__(self):
        self.string_path = join(storage.plugin_dir, "assets/strings.xml")
        self.strings = self.load_strings(self.string_path)
        # self.getDictByCategory("PoissonPage")

    def load_strings(self, filepath):
        stringXml = parse(filepath)
        strings = stringXml.documentElement.getElementsByTagName("string")
        loaded_string = {}
        for string in strings:
            key = string.getElementsByTagName("key")[0].childNodes[0].data
            category = string.getElementsByTagName("category")[0].childNodes[0].data
            text = string.getElementsByTagName("text")[0].childNodes[0].data
            loaded_string[key] = [category, text]

        # print loaded_string
        return loaded_string

    def getDictByCategory(self, category):
        result = {}
        for key, value in self.strings.items():
            if value[0] == category:
                result[key] = value[1]
                # print result
        return result

    def getValueByKey(self, key):
        value = self.strings.get(key, None)
        if value:
            return value[1]
        return ""


translation = Translation()
