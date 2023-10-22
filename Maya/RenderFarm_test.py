import imp
import maya.app.renderSetup.model.renderLayer as renderLayer
import maya.app.renderSetup.model.renderSetup as renderSetup
import maya.cmds as mc
import os,shutil

import socket
import sys
from _thread import *
from threading import Timer
from time import sleep
from pathlib import Path
from shutil import rmtree
import time

sys.path.append(r"\\fs3\Sh1\uber\Nuke_Scripts")

print(sys.path)
#import progressBarUI6
#from progressBarUI6 import Ui_Form

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt, Signal,QThread)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide2.QtWidgets import (QApplication, QLabel, QMainWindow, QProgressBar,
    QPushButton, QSizePolicy, QStatusBar, QWidget)
#########################################################
class Ui_Form(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(405, 167)
        MainWindow.setStyleSheet(u"background-color: rgb(61, 61, 61);\n"
"\n"
"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(10, 50, 381, 41))
        font = QFont()
        font.setFamilies([u"Microsoft PhagsPa"])
        font.setPointSize(11)
        self.progressBar.setFont(font)
        self.progressBar.setStyleSheet(u"color: rgb(15, 143, 255);")
        self.progressBar.setValue(0)
        self.progressBar.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 10, 81, 31))
        font1 = QFont()
        font1.setFamilies([u"Segoe MDL2 Assets"])
        font1.setPointSize(14)
        self.label.setFont(font1)
        self.label.setStyleSheet(u"color: rgb(218, 218, 218);")
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(100, 110, 191, 31))
        font2 = QFont()
        font2.setPointSize(12)
        self.pushButton.setFont(font2)
        self.pushButton.setStyleSheet(u"background-color: rgb(166, 166, 166);")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Progress", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"I know da wae", None))
    # retranslateUi

#########################################################

Constant = r'"C:\Program Files\Autodesk\Maya2022\bin\Render.exe"'
Constant2 = r" -r hw2 -rd "
print("Constant = {}".format(Constant))

MayaName = mc.file(q=True,sn=True,shn=True)
print("MayaName = {}".format(MayaName))

displayLayers = mc.ls(type="displayLayer")
print("displayLayers = {}".format(displayLayers))

SplitMayaName = MayaName.split(".")
SplitMayaName.pop()
SplitMayaName = "".join(SplitMayaName)
SplitMayaName = SplitMayaName.split("_")
print("SplitMayaName = {}".format(SplitMayaName))
LastSLOG = SplitMayaName[-1]
print("LastSLOG = {}".format(LastSLOG))

FullMayaPath_No_ext = mc.file(q=True,sn=True)
FullMayaPath_No_ext = FullMayaPath_No_ext.split(".")
FullMayaPath_No_ext.pop()
FullMayaPath_No_ext = "".join(FullMayaPath_No_ext)
print("FullMayaPath_No_ext = {}".format(FullMayaPath_No_ext))

RenderMayaName = '{}'.format(FullMayaPath_No_ext) + "_Render" + ".ma"
print("RenderMayaName = {}".format(RenderMayaName))
if LastSLOG.lower() != "Render".lower():

    
    for layer in displayLayers:
        if layer == "Cones_" or layer == "Geo_" or layer == "LIDAR_" or layer == "RIG_" or layer == "RIG_1":
            print ("Render LAYERS FOUND")
            mc.file(rename=RenderMayaName)
            mc.file(save=True,type='mayaAscii')
            break
        else:
            mc.error("Not Render Version, please use Render Script")
elif LastSLOG.lower() == "Render".lower():
    print("Render Version")
    for layer in displayLayers:
        if layer == "Cones_" or layer == "Geo_" or layer == "RIG_" or layer == "RIG_1":
            print ("Render LAYERS FOUND")
            mc.file(save=True,type='mayaAscii')
            break
        else:
            mc.error("Not Render Version, please use Render Script")


###################################################
FullMayaPath = mc.file(q=True,sn=True)
ActualMayaPath = FullMayaPath.split("/")

for j in ActualMayaPath[::-1]:
    ActualMayaPath.remove(j)
    if j == "main3d":
        break
for n, k in enumerate(ActualMayaPath):
    if k == "3d_comp":
        ActualMayaPath[n] = "render"

def FindMayaVersion():
    MayaActual,ext = os.path.splitext(MayaName)
    SplitMayaName = MayaActual.split("_")
    print ("SplitMayaName = {}".format(SplitMayaName))
    for q in reversed(SplitMayaName):
        if "v00" in q:
            return (q)

Version = FindMayaVersion()
print ("Version = {}".format(Version))
MayaRenderPath = "/".join(ActualMayaPath) + "/main3d/" + Version + "/"
if not os.path.exists(MayaRenderPath):
    original_umask = os.umask(0)
    os.makedirs(MayaRenderPath,mode=0o777  )

###################################################
#mc.workspace(fr=["images", MayaRenderPath])
#MayaRenderPath = mc.workspace(fre='images')
mc.workspace(fr=["images", MayaRenderPath])
print("MayaRenderPath = {}".format(MayaRenderPath))

#HostName = os.path.expanduser('~Desktop')
#HostName = HostName.replace("\\","/")
HostName = "C:/Users/Dame/Desktop"
print("HostName = {}".format(HostName))

ShotCopy = MayaRenderPath.split("/")
print("ShotCopy = {}".format(ShotCopy))
ShotName = MayaRenderPath.split("/")[-4]
print("ShotName = {}".format(ShotName))
DesktopMayaRenderPath = HostName + "/MayaRenders/" + ShotName
print("HostDesktopMayaRenderPathName = {}".format(DesktopMayaRenderPath))





RoyalCommand = Constant + Constant2 + DesktopMayaRenderPath + " " + FullMayaPath
print("RoyalCommand = {}".format(RoyalCommand))
##########################################
class MayaRenderCheck(QObject):
    stopped = Signal()
    finished = Signal()
    progress = Signal(int)
    def __init__(self,interval,fail_interval,function,fail_function,ShotName):
        super().__init__()
        self._timer      = None
        self.fail_timer      = None
        self.interval     = interval
        self.fail_interval     = fail_interval
        self.function     = function
        self.fail_function     = fail_function
        self.ShotName     = ShotName
        self.MayaPercentage = 0
        self.prevPercentageNumber = 0
        self.failCounter = 0
    #    self.args         = args
    #    self.kwargs       = kwargs
        self.is_running   = False
        self.fail_is_running   = False
        self.start()
        self.fail_start()
        self.inkrement = 0
        self.StudioName   = "Tippett"
        self.MayaLogs = r"C:\Users\Dame\Desktop\MayaLogs\\"
        self.MayaRenderFile = self.MayaLogs + "{}.txt".format(self.ShotName)
        self.ResetPercentage()
        self.Renderable_Layers = [str(rl.name()) for rl in RenderLayers if rl.isRenderable()]
        self.RemovePreviousRender()
    
    def ResetPercentage(self):
        mayaTruth = "{}={}".format(self.ShotName,self.MayaPercentage)
        with open (self.MayaRenderFile,"w") as file:
            file.writelines(mayaTruth)
    
    def RemovePreviousRender(self):
        for folder in os.listdir(MayaRenderPath):
            if folder in self.Renderable_Layers:
                rmtree(os.path.join(MayaRenderPath,folder))


    def run(self):
        self.is_running = False
        self.start()
        self.function(self)

    def fail_run(self):
        self.fail_is_running = False
        self.fail_start()
        self.fail_function(self)
    
    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval,self.run)
            self._timer.start()
            self.is_running = True

    def fail_start(self):
        if not self.fail_is_running:
            self.fail_timer = Timer(self.fail_interval,self.fail_run)
            self.fail_timer.start()
            self.fail_is_running = True

    def stop(self):
        print("STOPPING !!!!!!!!!!!!!!!!!")
        self._timer.cancel()
        self.fail_timer.cancel()
        self.is_running = False
        self.fail_is_running = False

    def CheckForFailiure(self):
        if self.prevPercentageNumber < self.MayaPercentage:
            self.prevPercentageNumber = self.MayaPercentage
            self.failCounter = 0
        elif self.prevPercentageNumber == self.MayaPercentage:
            self.failCounter += 1
            print ("self.failCounter = {}".format(self.failCounter))

    def Nuke_The_Maya_Process(self):
        self.MayaLogsStatus = r"C:\Users\Dame\Desktop\MayaStatusLogs\\"
        self.MayaStatusRenderFile = self.MayaLogsStatus + "{}.txt".format(self.ShotName)

        with open(self.MayaStatusRenderFile) as mrf:
            MayaStatusRenderText = mrf.readlines()
            for line in MayaStatusRenderText:
                if "{}".format(self.ShotName) in line:
                    line = line.split("=")[-1]
                    self.MayaStatusTruth = line
                    print ("self.MayaStatusTruth = {}".format(self.MayaStatusTruth))
                    
            print ("MayaStatusRenderText = {}".format(MayaStatusRenderText))
        if self.MayaStatusTruth == "True":
            self.stopped.emit()
            self.stop()

    def CheckMayaRenderStatus(self):
        self.Nuke_The_Maya_Process()
    #    self.MayaRenderFile = self.MayaLogs + "MayaRenderProgress.txt"
        
        with open(self.MayaRenderFile) as mrf:
            MayaRenderText = mrf.readlines()
            for line in MayaRenderText:
                if "{}".format(self.ShotName) in line:
                    line = line.split("=")[-1]
                    self.MayaPercentage = int(line)
                    print ("self.MayaPercentage = {}".format(self.MayaPercentage))
        #    print ("MayaRenderText = {}".format(MayaRenderText))
            self.progress.emit(self.MayaPercentage)

        if self.failCounter > 15:
            print("ABORTION")
            self.stop()
        
        if self.MayaPercentage == 100:
            self.finished.emit()
            self.stop()

##########################################
class Ui_MainWindow(QMainWindow):
    def __init__(self,ShotName):
        super(Ui_MainWindow, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.ui.pushButton.setEnabled(False)
        self.ui.progressBar.setValue(0) # 255, 85, 127
        self.ui.progressBar.setFormat("Initializing ...")
        MayaStylesheet = """
                            QProgressBar{
                                color: white;
                                border: 2px solid grey;
                                border-radius 5px;
                                text-align: center;
                            }

                            QProgressBar::chunk{
                                background-color: #3b8fa8 ;
                                width 10px;
                            }
                            """
        
        self.start_time = time.time()
        self.render_time = None
        self.resize(405, 177)
        self.ui.progressBar.setStyleSheet(MayaStylesheet)
        self.ShotName = ShotName
        
        self.Canceled = False
        self.MayaLogsStatus = r"C:\Users\Dame\Desktop\MayaStatusLogs\\"
        self.MayaRenderFile = self.MayaLogsStatus + "{}.txt".format(self.ShotName)

        self.MayaStatusTruth = "{}={}".format(self.ShotName,self.Canceled)
        with open (self.MayaRenderFile,"w") as file:
                    file.writelines(self.MayaStatusTruth)
        
        self.runLongTask()
        self.ui.pushButton.clicked.connect(lambda: self.CloseUI_And_Show_Da_Wae())

    def reportProgress(self, mayaPercengage):
        if mayaPercengage > 0:
            self.ui.progressBar.setProperty("value", mayaPercengage)
            self.ui.progressBar.setFormat(str(mayaPercengage)+ "%")

    def closeEvent(self,event):
        print("EVENT CLOSING")
        try:
            self.UI_Check_Close()
            event.accept() # let the window close
        except:
            print("Close Event has failed")
            event.ignore()

    def UI_Check_Close(self):
        self.Canceled = True
        UI_Canceled_Status = self.Canceled     
        print ("UI_Canceled_Status = {}".format(self.Canceled))
        
        self.MayaStatusTruth = "{}={}".format(self.ShotName,self.Canceled)
        with open (self.MayaRenderFile,"w") as file:
            file.writelines(self.MayaStatusTruth)


        self.close()

    def CloseUI_And_Show_Da_Wae(self):
    #    self.WindowzRenderLocation = self.RenderLocation.replace("/","\\")
    #    webbrowser.open(os.path.realpath(self.WindowzRenderLocation))
        self.close()

    def STAHP(self):
        self.end_time = time.time()
        self.render_time = self.end_time - self.start_time
        self.Render_Time_Label = QLabel(self)
        self.Render_Time_Label.setAlignment(Qt.AlignCenter)
        self.Render_Time_Label.setGeometry(self.width() //2 - 100 ,self.height()-32,200,25)
       
        self.Render_Time_Label.setStyleSheet(
        "QLabel {"
        "color: rgb(112,161,204);"  #Blue
        "font: 10pt ;"
        "}"
        "QLabel span {"
        "color: rgb(112,161,204);"
        "}"
        )

        Seconds = self.render_time

        Minutes = int(Seconds / 60)
        Remainder = int(Seconds % 60)

        DigitLength = len(str(Remainder))

        if DigitLength == 1:
            Render_Time = "{}:0{} minutes".format(Minutes,Remainder)
            self.Render_Time_Label.setText("Render time: {}:0{} minutes".format(Minutes,Remainder))
        else:
            Render_Time = "{}:{} minutes".format(Minutes,Remainder)
            self.Render_Time_Label.setText("Render time: {}:{} minutes".format(Minutes,Remainder))


        self.Render_Time_Label.show()
        self.worker.stop()

    def runLongTask(self):
        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = MayaRenderCheck(1,13,MayaRenderCheck.CheckMayaRenderStatus,MayaRenderCheck.CheckForFailiure,self.ShotName)
        # (self,interval,fail_interval,function,fail_function,ShotName)
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
       # self.thread.started.connect(self.worker.run)
        self.thread.finished.connect(lambda: self.ui.pushButton.setEnabled(True))
        self.thread.finished.connect(lambda: self.STAHP())
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.reportProgress)
        # Step 6: Start the thread
        self.thread.start()
        

#################################################################

##########################################
# HOST, PORT = "10.100.20.139", 9998
HOST, PORT = "192.168.100.4", 9998
#data = " ".join(sys.argv[1:])
# NukeBoolean = "MayaRenderEXP"
NukeBoolean = "MayaRenderEXP"

dmrp = DesktopMayaRenderPath
MayaPateshestvie = r"{}".format(MayaRenderPath)

#startF = int(mc.playbackOptions(min=True, q=True))
#endF = int(mc.playbackOptions(max=True, q=True))

startF = int(mc.getAttr("defaultRenderGlobals.startFrame"))
endF =   int(mc.getAttr("defaultRenderGlobals.endFrame"))


FirstFrame = startF
LastFrame = endF
FrameRange = "{FirstFrame}-{LastFrame}".format(FirstFrame=FirstFrame,LastFrame=LastFrame)

LayerCount = 0
rs = renderSetup.instance()
RenderLayers = rs.getRenderLayers()
for rl in RenderLayers:
    if rl.isRenderable():
        LayerCount += 1

#layers= mc.ls(long=True,type="displayLayer")
#for layer in layers:
#    if "defaultLayer" not in layer:
#        if layer.isRenderable():
#            LayerCount += 1

print("layers: {}".format(LayerCount))


# Create a socket (SOCK_STREAM means a TCP socket)
try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    #    if not os.path.exists(DesktopMayaRenderPath):
    #        os.makedirs(DesktopMayaRenderPath)
        # Connect to server and send data
        sock.connect((HOST, PORT))
    #    sock.sendall(bytes(NukeBoolean  , "utf-8"))
        sock.sendall(bytes("\n".join(map(str,[NukeBoolean,RoyalCommand,dmrp,MayaPateshestvie,FrameRange,LayerCount])) , "utf-8"))
    #    sock.sendall(bytes(MayaPateshestvie , "utf-8"))
        # MayaRenderCheck(6,MayaRenderCheck.CheckMayaRenderStatus,ShotName)
        app = QApplication.instance()
        if app == None:
            app = QApplication(sys.argv)
        win = Ui_MainWindow(ShotName)
        win.show()
        app.exec_()
        # Receive data from the server and shut down
        received = str(sock.recv(2048), "utf-8")

    print("Sent:     {}".format(NukeBoolean))
    print("Received: {}".format(received))

except PermissionError:
    cmds.confirmDialog(title="ERROR:",message="Wait a bit for the files to transfer first",button=["ok :/"],defaultButton="ok :/")
    win.UI_Check_Close()


except:
    HostName = os.path.expanduser('~Desktop')
    DesktopMayaRenderPath = HostName + "/MayaRenders/" + ShotName
    RoyalCommand = Constant + Constant2 + DesktopMayaRenderPath + " " + FullMayaPath
    print("RoyalCommand = {}".format(RoyalCommand))
    os.system(RoyalCommand)

    for folder in os.listdir(DesktopMayaRenderPath):
        try:
            shutil.rmtree(os.path.join(MayaRenderPath,folder),ignore_errors=True)
            shutil.move(os.path.join(DesktopMayaRenderPath,folder),MayaRenderPath)
        except: 
            pass




