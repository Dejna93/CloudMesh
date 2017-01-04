import filecsv
import  unittest
import os

class FileFilepathInput(unittest.TestCase):

    goodFile = "C:\\Users\\callo\\abaqus_plugins\\CloudMesh\\data.txt"

    badFile = "C:\\Users\\callo\\abaqus_plugins\\CloudMesh\\niema.txt"

    badType = "test.exe"

    dataTest = "C:\\Users\\callo\\abaqus_plugins\\CloudMesh\\test\\test.txt"
    fileIO = filecsv.FileIO("")

    def test_empty(self):

        self.assertEqual(self.fileIO.empty_filepath(""),1)

    def test_no_empty(self):

        self.assertEqual(self.fileIO.empty_filepath("data.txt"),0)

    def test_exists_file(self):


        self.assertEqual(self.fileIO.exists_file(self.goodFile),1)

    def test_no_exists_file(self):

        self.assertEqual(self.fileIO.exists_file(self.badFile),0)

    def test_check_extension(self):

        self.assertEqual(self.fileIO.check_extension(self.goodFile),1)

    def test_check_bad_extension(self):

        self.assertEqual(self.fileIO.check_extension(self.badType),0)

    def test_file_load(self):

        self.assertEqual(self.fileIO.file_load(self.goodFile), 1)

    def test_no_file_load(self):

        self.assertEqual(self.fileIO.file_load(self.badFile), 0)

    def test_get_extension(self):

        self.assertEqual(self.fileIO.get_extension(self.goodFile), '.txt')

    def test_get_no_extension(self):

        self.assertEqual(self.fileIO.get_extension(self.badFile), '')

    def test_get_data(self):
        test_txt = {"0" : [[4.8025699 ,42.687401, 50.8004],
                            [3.9458301 ,42.592499 ,50.446701],
                            [3.0706, 42.431599 ,50.075901],
                            [4.56215, 42.778999 ,51.6693],
                            [3.7053599, 42.708099, 51.3274]]
        }
        test_csv = {"1": [ [4.8025699,42.687401,50.8004],[3.9458301,42.592499,50.446701] ],
                    "2": [[3.0706,42.431599,50.075901]],
                    "3": [[4.56215,42.778999,51.6693]],
                    "4": [ [3.7053599,42.708099,51.3274]]
                    }


        if self.fileIO.get_extension() == '.txt':
            self.assertEqual(self.fileIO.get_data(), test_txt)
        elif self.fileIO.get_extension() == '.csv':
            self.assertEqual(self.fileIO.get_data(), test_csv)







