import sys,os
import subprocess
sys.path.append(r"\\fs3\Sh1\uber\Nuke_Scripts")
sys.path.append(r"\\fs3\Sh1\uber\Nuke_Scripts\NukeScripts")


from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QFile,Qt
# from PixoSTMapMenu import Ui_Form
from NukeLauncherUI_PyQt5 import Ui_Form
from PyQt5 import QtGui

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
    def FindMayaVersion(self, ThreeD_comp_Path):
        MayaPath= ThreeD_comp_Path + "\main3d"
        print (MayaPath)
        ActualMayaPath = MayaPath.split("/")
        print(ActualMayaPath)
        ProjectPath = ThreeD_comp_Path.split("\\")[:-2]
        ProjectName = ProjectPath[-1]
        StudioName = ProjectPath[-2]
        print ("ProjectName = {}".format(ProjectName))
        print ("StudioName = {}".format(StudioName))
        ListOfMayas = []
        for n in os.listdir(MayaPath):
            if n.endswith(".ma"):
                ListOfMayas.append(n)

        print ("ListOfMayas = {}".format(ListOfMayas))
        if ListOfMayas:
            for i in reversed(ListOfMayas):
                ActualName = i.split("_")
                for q in reversed(ActualName):
                    if "v00" in q:
                        return (q)
            print ("ListOfMayas = {}".format(ListOfMayas))
        else:
            Version = "v001"
            return Version
    

    def Give_Paths(self):
        ThreeD_comp_Path = r"{}".format(self.ui.Three_D_Path.text())
        render_Path = r"{}".format(self.ui.Render_Path.text())
        jpg_Path = r"{}".format(self.ui.JPG_Path.text())
        ShotName = ThreeD_comp_Path.split("\\")
        ShotName = ShotName[-1]
        try:
            Version = self.FindMayaVersion(ThreeD_comp_Path)
        except:
            Version = "v001"
        Arguements = [r"C:\Program Files\Nuke13.1v3\Nuke13.1.exe",r'\\fs3\Sh1\uber\Nuke_Scripts\NukeScripts\NukeMenu3.py',ThreeD_comp_Path,render_Path,jpg_Path,ShotName,Version]
        subprocess.Popen(Arguements)

        print (ThreeD_comp_Path)
        print (render_Path)
        print (jpg_Path)
        print (ShotName)
        print ("Version = {}".format(Version))
 

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    window.setWindowTitle("NukeLauncher")
    window.setWindowIcon(QtGui.QIcon(r'\\fs3\Sh1\uber\Nuke_Scripts\NukeScripts\Icons\nukelauncher.ico'))
    # window.setWindowIcon(QtGui.QIcon(r'C:\Users\Dame\Desktop\NukeTest\NukeScripts\Pixomondo STMap Generator\pxo.ico'))
    window.ui.Process.clicked.connect(window.Give_Paths)
    sys.exit(app.exec())
