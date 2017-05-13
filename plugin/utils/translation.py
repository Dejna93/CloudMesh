from xml.dom.minidom import parse
from plugin.utils.oso import join
from plugin.config import storage


class Translation(object):
    def __init__(self):
        self.string_path = join(storage.plugin_dir, "assets/strings.xml")
        self.strings = self.load_strings(self.string_path)
        # self.getDictByCategory("PoissonPage")

    def load_strings(self, filepath):
        string_xml = parse(filepath)
        strings = string_xml.documentElement.getElementsByTagName("string")
        loaded_string = {}
        for string in strings:
            key = string.getElementsByTagName("key")[0].childNodes[0].data
            category = string.getElementsByTagName("category")[0].childNodes[0].data
            text = string.getElementsByTagName("text")[0].childNodes[0].data
            loaded_string[key] = [category, text]

        # print loaded_string
        return loaded_string

    def get_dict_by_category(self, category):
        result = {}
        for key, value in self.strings.items():
            if value[0] == category:
                result[key] = value[1]
                # print result
        return result

    def get_value_by_key(self, key):
        value = self.strings.get(key, None)
        if value:
            return value[1]
        return ""


translation = Translation()
