import os,sys,subprocess,time,multiprocessing
sys.path.append(r"\\fs3\Sh1\uber\Nuke_Scripts")
sys.path.append(r"\\fs3\Sh1\uber\Master\MayaScripts_2018\main_scripts_Python_3")

#os.environ['QT_PREFERED_BINGIND'] = 'PySide6'

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt,QTimer)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide2.QtWidgets import (QApplication, QLabel, QMainWindow, QProgressBar,
    QPushButton, QSizePolicy, QStatusBar, QWidget,QLineEdit)

#from PySide2.QtCore import *
#from PySide2.QtGui import *
#
from PySide2 import QtWidgets,QtCore,QtGui
#from PySide2.QtWidgets import QApplication
import shiboken2

import maya.OpenMayaUI as omui
import maya.cmds as mc

from NukeLauncher_JPG import Ui_NukeLauncher_Window

#venv_path = r"\\fs3\Sh1\uber\Nuke_Scripts\NukeScripts\Python_3.10_VENV\Scripts\activate.bat"
#os.system(venv_path)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_NukeLauncher_Window()
        self.ui.setupUi(self)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.ui.JPG_Link.textChanged.connect(self.debounce_on_text_changed)
        self.debounce_Timer = QTimer()
        self.debounce_Timer.setSingleShot(True)
        self.debounce_Timer.timeout.connect(self.on_text_changed)

        self.ui.LaunchButton.setEnabled(False)
        self.Valid_Link = False
        self.Source_Detected = False
        self.DisabledButtonStyleSheet = ("background-color: rgb(18, 192, 240);\n"
            "background-color: qlineargradient(spread:pad, x1:0.153045, y1:0.176, x2:0.676, y2:1, stop:0 rgba(105, 55, 55, 212), stop:1 rgba(255, 255, 255, 0));\n"
            "\n"
            "color: rgb(0, 0, 0);\n"
            "border-radius:12px;"
            )
        self.EnabledButtonStyleSheet = ("background-color: rgb(18, 192, 240);\n"
            "background-color: qlineargradient(spread:pad, x1:0.153045, y1:0.176, x2:0.676, y2:1, stop:0 rgba(0, 153, 171, 212), stop:1 rgba(255, 255, 255, 0));\n"
            "\n"
            "color: rgb(255, 255, 255);\n"
            "border-radius:12px;"
            )
        self.ui.LaunchButton.setStyleSheet(self.DisabledButtonStyleSheet)
        self.Get_Three_D_Path()

    def debounce_on_text_changed(self):
        self.debounce_Timer.stop()
        self.debounce_Timer.start(300) # 300 ms delay


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

    def Check(self,path):
        print ("Text = {}".format(path))

        #if path.startswith("//fs3") and len(path) < 6:
        if path.startswith("//") and path.count("/") <=3:
            print("Fs3 path")
            return

        try:
            for item in os.listdir(path):
                item_path = os.path.join(path,item)
                if os.path.isdir(item_path):
                    continue
                elif os.path.isfile(item_path):
                    print(item)
                    if item.endswith(".jpg"):
                        self.Valid_Link = True
                        break
                    else:
                        self.Valid_Link = False
        except FileNotFoundError as e:
            #print(e)
            self.Valid_Link = False
            pass
        
        except SyntaxError:
            self.Valid_Link = False
            pass

    def on_text_changed(self):
        # VALID
        self.text = self.ui.JPG_Link.text()
        self.Check(self.text)
        if self.Valid_Link == True:
            self.ui.LinkStatus.setStyleSheet(u"font: 10pt \"Segoe UI\";\n"
            "color: rgb(5, 255, 193);")
            self.ui.LinkStatus.setText("Valid Link")
            self.ui.LaunchButton.setEnabled(True)
            self.ui.LaunchButton.setStyleSheet(self.EnabledButtonStyleSheet)

        # INVALID
        elif self.Valid_Link == False and len(self.ui.JPG_Link.text())>=1:
            self.ui.LinkStatus.setStyleSheet(u"font: 10pt \"Segoe UI\";\n"
            "color: rgb(255, 179, 1);")
            self.ui.LinkStatus.setText("Invalid Link / Empty Folder")
            self.ui.LaunchButton.setEnabled(False)
            self.ui.LaunchButton.setStyleSheet(self.DisabledButtonStyleSheet)
        # NO LINK
        if len(self.ui.JPG_Link.text()) == 0:
            self.ui.LinkStatus.setStyleSheet(u"font: 10pt \"Segoe UI\";\n"
            "color: rgb(255, 0, 0);")
            self.ui.LinkStatus.setText("No Link")
            self.ui.LaunchButton.setEnabled(False)
            self.ui.LaunchButton.setStyleSheet(self.DisabledButtonStyleSheet)

    def closeWithDelay(self):
        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.Close_Window)
        self.timer.start(3000) # 3 seconds delay

    def Close_Window(self):
        self.close()

    def Get_Maya_Path(self):
        FullMayaPath_No_ext = mc.file(q=True,sn=True)
        FullMayaPath_No_ext = FullMayaPath_No_ext.split(".")
        FullMayaPath_No_ext.pop()
        FullMayaPath_No_ext = "".join(FullMayaPath_No_ext)
        print("FullMayaPath_No_ext = {}".format(FullMayaPath_No_ext))
        return FullMayaPath_No_ext

    def Get_Three_D_Path(self):
        self.MayaPath = r"{}".format(self.Get_Maya_Path())
        if self.MayaPath == '':
            mc.confirmDialog(title="ERROR:",message="Maya Not saved ! ",button=["OK"],defaultButton="OK")
            sys.exit()
        self.MayaPath = self.MayaPath.split("/")
        print("self.MayaPath = {}".format(self.MayaPath))
        if "fs3" not in self.MayaPath:
            mc.confirmDialog(title="ERROR:",message="Maya Not saved on server! ",button=["OK"],defaultButton="OK")
            sys.exit()

        
        self.Three_D_Path = self.MayaPath[:]
        self.Render_Path = self.MayaPath[:]
        for j in self.Three_D_Path[::-1]:
            self.Three_D_Path.remove(j)
            if j == "main3d":
                break
        for j in self.Render_Path[::-1]:
            self.Render_Path.remove(j)
            if j == "main3d":
                break
        for n, k in enumerate(self.Render_Path):
            if k == "3d_comp":
                self.Render_Path[n] = "render" 
        self.Three_D_Path = "\\".join(self.Three_D_Path)
        self.Render_Path = "\\".join(self.Render_Path)      
        print("ThreeD_comp_Path = {}".format(self.Three_D_Path))
        print("self.Render_Path = {}".format(self.Render_Path))
        self.Check_Source(self.Three_D_Path,self.Render_Path)
    

    def Haunt(self):
        python_path = r"\\fs3\Sh1\uber\Nuke_Scripts\NukeScripts\Python310\python.exe"
        script = r"C:\Users\CollegiaTitanica\Desktop\mayatest.py"
        #script = r"\\fs3\Sh1\uber\Nuke_Scripts\NukeLauncher_Experimental.exe"
        #script = r"C:\Users\CollegiaTitanica\Desktop\NukeLauncher_v13.1.exe"
        #Arguements = "{}".format(python_path)
        Arguements = "{} {}".format(python_path,script)
        os.system(Arguements)
        



    def Check_Source(self,Three_D_Path,Render_Path):
        self.JPG_Check_Path = Three_D_Path[:]
        self.JPG_Check_Path = self.JPG_Check_Path.replace("3d_comp","source") + "\\jpg"
        print("self.JPG_Check_Path = {}".format(self.JPG_Check_Path))
        try:
            for item in os.listdir(self.JPG_Check_Path):
                item_path = os.path.join(self.JPG_Check_Path,item)
                if os.path.isdir(item_path):
                    continue
                elif os.path.isfile(item_path):
                    print(item)
                    if item.endswith(".jpg"):
                        self.Source_Detected = True

                        self.Launch_Nuke_Directly(self.JPG_Check_Path)
                    #    self.Haunt()
                    #    script = r"C:\Users\CollegiaTitanica\Desktop\mayatest.py"
                    #    Arguements = [r"python",script]
                    #    subprocess.Popen(Arguements)
                        break
                    else:
                        self.Source_Detected = False
        except FileNotFoundError as e:
            #print(e)
            self.Source_Detected = False
            pass

    def Launch_Nuke_Directly(self,jpg_path):
        self.jpg_Path = self.JPG_Check_Path
        
        self.ShotName = self.Three_D_Path.split("\\")
        self.ShotName = self.ShotName[-1]
        print (self.ShotName)
        
        try:
            self.Version = self.FindMayaVersion(self.Three_D_Path)
        except:
            self.Version = "v001"
        print ("self.Version = {}".format(self.Version))
        Arguements = [r"C:\Program Files\Nuke13.1v3\Nuke13.1.exe",r'\\fs3\Sh1\uber\Nuke_Scripts\NukeScripts\NukeMenu3.py',self.Three_D_Path,self.Render_Path,self.jpg_Path,self.ShotName,self.Version]
        subprocess.Popen(Arguements)


    def Give_Paths(self):
        self.ui.LaunchButton.setStyleSheet(u"background-color: rgb(18, 192, 240);\n"
        "background-color: qlineargradient(spread:pad, x1:0.153045, y1:0.176, x2:0.676, y2:1, stop:0 rgba(243, 190, 16, 212), stop:1 rgba(255, 255, 255, 0));\n"
        "\n"
        "color: rgb(0, 0, 0);\n"
        "border-radius:12px;")
        self.ui.LaunchButton.setText("Launching Nuke")
        self.ui.LaunchButton.setEnabled(False)
        self.jpg_Path = r"{}".format(self.ui.JPG_Link.text())
        
        self.ShotName = self.Three_D_Path.split("\\")
        self.ShotName = self.ShotName[-1]
        print (self.ShotName)
        
        try:
            self.Version = self.FindMayaVersion(self.Three_D_Path)
        except:
            self.Version = "v001"
        print ("self.Version = {}".format(self.Version))
        Arguements = [r"C:\Program Files\Nuke13.1v3\Nuke13.1.exe",r'\\fs3\Sh1\uber\Nuke_Scripts\NukeScripts\NukeMenu3.py',self.Three_D_Path,self.Render_Path,self.jpg_Path,self.ShotName,self.Version]
        subprocess.Popen(Arguements)


        self.closeWithDelay()

if __name__ == "__main__":
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)

    window = MainWindow()
 #   window.show()
    

    if window.Source_Detected == True:
        print("window.JPG_Check_Path = {}".format(window.Source_Detected))
        #sys.exit()
    else:
        maya_window_ptr = omui.MQtUtil.mainWindow()
        mayaMainWindow = shiboken2.wrapInstance(int(maya_window_ptr),QtWidgets.QMainWindow)
        window.setParent(mayaMainWindow)
        window.setWindowFlags(QtCore.Qt.Window)
        window.setWindowTitle("NukeLauncher")

        window.setWindowIcon(QtGui.QIcon(r'\\fs3\Sh1\uber\Master\MayaScripts_2018\vertigo_shelf\icons\O_Nuke_F_Icon.png'))
        window.ui.LaunchButton.clicked.connect(window.Give_Paths)

        window.show()

        QApplication.processEvents()
        #sys.exit()

# Valid Link color: rgb(5, 255, 193);
# Invalid Link - No Images color: rgb(255, 179, 1);
# No Link - color: rgb(255, 0, 0);
