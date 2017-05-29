import os
import csv
from plugin.utils.oso import join
from plugin.config import storage


def convert_txt_to_pcd(filename):
    """

    :type filename: String
    """
    print filename
    if filename[-3:] == 'txt':
        with open(filename, 'r') as txt_file:
            data = []
            for line in txt_file.readlines():
                data.append([split for split in line.split()])
            txt_file.close()
            filename = filename.replace('.txt', '.pcd')
            # print "converting" + filename
            pcdheader(filename, len(data))
            write_data(filename, data)
    return filename


def convert_csv_to_pcd(filename, csv_type='T'):
    data = {}
    with open(filename, 'r') as csv_file:
        try:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                temp = list(row)
                if len(temp) == 3:
                    csv_type = 'N'
                if len(temp) == 4 and csv_type == 'T':
                    if temp[-1] in data:
                        data[temp[-1]].append(temp[0:3])
                    else:
                        data[temp[-1]] = [temp[0:3]]
                else:
                    data["0"].append(temp[0:3])
        finally:
            csv_file.close()
        if data:
            # TODO dodanie pytania czy rozbijac na fazy czy nie ?
            for key, value in data.iteritems():
                folder, tail = os.path.split(filename)
                file_pcd = join(folder, "".join((os.path.splitext(tail)[0], key, ".pcd")))
                storage.created_pcd.append(file_pcd)
                pcdheader(file_pcd, len(value))
                write_data(file_pcd, value)

    return filename


def pcdheader(filename, size):
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
    with open(filename, 'w') as pcd_file:
        pcd_file.write(header.format(size))
        pcd_file.close()


def write_data(filename, data):
    with open(filename, 'a') as pcd_file:
        pcd_format = "{0} {1} {2} \n"
        for points in data:
            # file.write(str(points)[1:-1].replace(',', '') + '\n')
            pcd_file.write(pcd_format.format(*points))
        pcd_file.close()
