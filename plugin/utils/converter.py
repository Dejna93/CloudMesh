import os
import csv
from plugin.utils.oso import join
from plugin.config import global_vars
def convert_txt_to_pcd(filename):
    print filename
    if filename[-3:] == 'txt':
        with open(filename,'r') as file:
            data = []
            for line in file.readlines():
                data.append([split for split in line.split()])
            file.close()
            filename = filename.replace('.txt', '.pcd')
            print "converting" + filename
            pcdheader(filename,len(data))
            write_data(filename,data)
    return filename


def convert_csv_to_pcd(filename, type='T'):
    data = {}
    with open(filename,'r') as file:
        try:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                temp = list(row)
                if len(temp) == 3:
                    type = 'N'
                if type == 'T':
                    if temp[-1] in data:
                        data[temp[-1]].append(temp[0:3])
                    else:
                        data[temp[-1]] = [temp[0:3]]
                else:
                    data["0"].append(temp[0:3])

        finally:
            file.close()
        if data:
            #TODO dodanie pytania czy rozbijac na fazy czy nie ?
            for key, value in data.iteritems():
                folder , tail = os.path.split(filename)
                #file_pcd = filename[:-4] + str(key) + ".pcd"
                file_pcd = join(folder,"".join((os.path.splitext(tail)[0],key,".pcd")))
                global_vars.created_pcd.append(file_pcd)
                pcdheader(file_pcd,len(value))
                write_data(file_pcd,value)
                print file_pcd
                #TODO dodanie do files_pcd


    return filename

def pcdheader( filename, size):
    header = """# .PCD v.7 - Point Cloud Data file format
VERSION .7
FIELDS x y z
SIZE 4 4 4
TYPE F F F
COUNT 1 1 1
WIDTH {0}
HEIGHT 1
VIEWPOINT 0 0 0 1 0 0 0
POINTS {0}
DATA ascii
"""
    with open(filename,'w') as file:
        file.write(header.format(size))
        file.close()

def write_data(filename, data):
    with open(filename,'a') as file:
        format = "{0} {1} {2} \n"
        for points in data:
            #file.write(str(points)[1:-1].replace(',', '') + '\n')
            file.write(format.format(*points))
        file.close()
