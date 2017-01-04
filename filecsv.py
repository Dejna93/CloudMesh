import csv
import os.path

def singelton(class_):
    instances  = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args,**kwargs)
        return instances[class_]
    return getinstance

@singelton
class FileIO(object):
    phase = {}
    file_path = ""
    def __init__(self, filepath):
        self.fileTypes = FileExtension()
        self.filepath = filepath

    def file_load(self, filepath=file_path):
        if self.empty_filepath(filepath):
            print("Empty filepath")
            return 0
        if not self.exists_file(filepath):
            print("File doesnt exists")
            return 0
        elif not self.check_extension(filepath):
            print("Incorrect file extension")
            return 0

        if self.get_extension(filepath) == '.txt':
            self.load_txt_to_pcd(filepath)


        return 1

    def empty_filepath(self, filepath=file_path):
        if filepath:
            return 0
        return 1

    def exists_file(self,filepath=file_path):
        if os.path.exists(filepath):
            return 1
        return 0

    def check_extension(self,filepath=file_path):
        if not self.fileTypes.check_type(filepath):
            return 0
        return 1

    def get_extension(self,filepath=file_path):
        if self.exists_file(filepath):
            return os.path.splitext(filepath)[-1].lower()
        return ''

    def load_txt_to_pcd(self,filepath=file_path):
        try:
            file_txt = open(filepath,'r')
        except IOError as e:
            print "I/O error({0}) : {1} ".format(e.errno, e.strerror)


    def pcd_header(self, filepath=file_path):
        header = [
            ('HEAD', "# .PCD v.7 - Point Cloud Data file format"),
            ('VERSION', "VERSION .7"),
            ('FIELDS', "FIELDS x y z"),
            ('SIZE', "SIZE 4 4 4"),
            ('TYPE', "TYPE F F F"),
            ('COUNT', "COUNT 1 1 1"),
            ('WIDTH', "WIDTH %s"),
            ('HEIGHT', "HEIGHT 1"),
            ('VIEWPORT', "VIEWPOINT 0 0 0 1 0 0 0"),
            ('POINTS', "POINTS %s"),
            ('DATA', "DATA ascii")
        ]

    def get_data(self,filepath=file_path):
        data = {}
        if self.get_extension(filepath) == '.txt':
            file_txt = open(filepath,'r')
            data["0"] = []
            for line in file_txt:
                data["0"].append([float(x) for x in line.split()])
        elif self.get_extension(filepath) == '.csv':
            file_csv = open(filepath,'r')
            data = {}
            try:
                reader = csv.reader(file_csv)
                for row in reader:
                    temp = list(row)
                    if temp[-1] in data:
                        data[temp[-1]].append(temp[0:3])
                    else:
                        data[temp[-1]] = [temp[0:3]]
            finally:
                file_csv.close()
        print data
        return data

    def get_data_size(self):
        size = 0
        for key,value in self.get_data():
            size += len(value)
        return  size


@singelton
class FileExtension(object):
    file_type = ('.txt' , '.csv' )

    def check_type(self,filepath):
        return self.correct_type(os.path.splitext(filepath)[-1].lower())

    def correct_type(self,type):
        return type in self.file_type

    def current_type(self,filepath):
        _index = self.file_type.index(os.path.splitext(filepath)[-1].lower())
        return self.file_type[_index]



f = open('microstructure.csv','rt')
points = []
fazy = {}
try:
    reader = csv.reader(f)
    for row in reader:
       temp = list(row)
       if temp[-1] in fazy:
           fazy[temp[-1]].append(temp[0:3])
       else:
           fazy[temp[-1]] = [temp[0:3]]
#
#
finally:
    f.close()
for key,value in fazy.iteritems():
    w = open(key+'.txt','w')
    


