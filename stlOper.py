
import numpy
from stl import mesh

class FileOperation:

    filename = ''
    vertice_count = 0
    #asci vesion


    def txtTopcd(self,filename):
        file = open(filename,'r')
        data = []
        for line in file:
            data.append([float(split) for split in line.split()] )

        file.close()
        filename = filename.replace('.txt','.pcd')
        self.vertice_count = len(data)
        self.pcdheader(filename,self.vertice_count)
        self.pcddata(filename,data)

        return  filename


    def pcdheader(self, filename, size):
        header = [
                    ('HEAD' , "# .PCD v.7 - Point Cloud Data file format"),
                    ('VERSION',"VERSION .7"),
                    ('FIELDS' , "FIELDS x y z"),
                    ('SIZE'  ,  "SIZE 4 4 4"),
                    ('TYPE'  ,   "TYPE F F F"),
                    ('COUNT'   ,   "COUNT 1 1 1"),
                    ('WIDTH'   ,   "WIDTH %s"),
                    ('HEIGHT'  ,   "HEIGHT 1"),
                    ('VIEWPORT' ,   "VIEWPOINT 0 0 0 1 0 0 0"),
                    ('POINTS'    ,   "POINTS %s"),
                    ('DATA'     ,  "DATA ascii")
                   ]
        print size
        file = open(filename,'w')
        for key , value  in header:
            if key=="WIDTH" or key=="POINTS":
                file.write(value%(size)+'\n')
            else:
                file.write(value+'\n')

        file.close()

    def pcddata(self,filename,data):
        file = open(filename,'a')
        if file:
            for points in data:
                file.write(str(points)[1:-1].replace(',','')+'\n')

        file.close()











