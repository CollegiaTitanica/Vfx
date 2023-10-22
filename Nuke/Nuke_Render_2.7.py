import os,shutil,webbrowser
from shutil import rmtree
import socket
import sys,subprocess
from contextlib import closing
from threading import Timer
from time import sleep
from pathlib import Path

from Opening import Ui_Opening
from FrameRange import Ui_FrameRangeWindow
import time
#import progressBarUI6
#from PyQt5.QtCore import QObject, QThread, pyqtSignal,Qt
#from PyQt5 import QtCore, QtGui, QtWidgets
#from PyQt5.QtWidgets import (
#    QApplication,
#    QLabel,
#    QMainWindow,
#    QPushButton,
#    QVBoxLayout,
#    QWidget,
#)

sys.path.append(r"\\fs3\Sh1\uber\Nuke_Scripts")
import psutil

parent_pid = psutil.Process().ppid()

parent_process = psutil.Process(parent_pid)
parent_args = parent_process.cmdline()
parent_app = r"{}".format(parent_args[0])
print("parent_process = {}".format(parent_process))
print("parent_args = {}".format(parent_args))
print("parent_app = {}".format(parent_app))

pyside2_apps = ["Maya2020","Maya2022","Maya2023"]
parent_app = parent_app.split("\\")
importes_pyside2 = False
for x in parent_app:
    if x in pyside2_apps:
        importes_pyside2 = True    

print("importes_pyside2 = {}".format(importes_pyside2))

if importes_pyside2 == True:
    from progressBarUI2 import Ui_Form
    from PySide2 import QtGui,QtCore

    from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
        QMetaObject, QObject, QPoint, QRect,
        QSize, QTime, QUrl, Qt, Signal,QThread,QEventLoop,QTimer)
    from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
        QFont, QFontDatabase, QGradient, QIcon,
        QImage, QKeySequence, QLinearGradient, QPainter,
        QPalette, QPixmap, QRadialGradient, QTransform,QIntValidator)
    from PySide2.QtWidgets import (QApplication, QLabel, QMainWindow, QProgressBar,
        QPushButton, QSizePolicy, QStatusBar, QWidget, QLineEdit, QCheckBox)
else:
    from progressBarUI6 import Ui_Form
    from PySide6 import QtGui,QtCore

    from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
        QMetaObject, QObject, QPoint, QRect,
        QSize, QTime, QUrl, Qt, Signal,QThread)
    from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
        QFont, QFontDatabase, QGradient, QIcon,
        QImage, QKeySequence, QLinearGradient, QPainter,
        QPalette, QPixmap, QRadialGradient, QTransform,QIntValidator)
    from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QProgressBar,
        QPushButton, QSizePolicy, QStatusBar, QWidget, QLineEdit, QCheckBox)

try:
    Nuke_FileName = nuke.scriptName()
except RuntimeError:
    nuke.message("Save the file on server !")
nuke.scriptSaveAs(Nuke_FileName,overwrite=1)
try:
    StudioName = Nuke_FileName.split("/")
    for j in StudioName[::-1]:
        StudioName.remove(j)
        if j == "3d_comp":
            break
    StudioName=StudioName[-2]
    print("StudioName = {}".format(StudioName))
except:
    StudioName = "Not_Important"

Nuke_ActualFileName = Nuke_FileName.split("/")[-1]

readNodeLIST = []
writeNodeLIST = []
FrameRangeLIST = []
RenderLocationLIST = []

def RecursiveFind(Depen):
    for i in Depen:
        depenCeption = nuke.Node.dependencies(i)
    #    print ("depenCeption = {}".format(depenCeption))
        for read in depenCeption:
            if read.Class() == "Read":
                readNodeLIST.append(read)
                FrameRange = str(read["first"].value()) + "-" + str(read["last"].value())
    #            print ("FrameRange = {}".format(FrameRange))
                FrameRangeLIST.append(FrameRange)
        
        if depenCeption:
            RecursiveFind(depenCeption)
    return 

for w in nuke.allNodes("Write"):
    writeNodeLIST.append(w)
    RenderLocation = w["file"].value()  
    print ("RenderLocation = {}".format(RenderLocation))
    RenderLocationLIST.append(RenderLocation)
    Depen = nuke.Node.dependencies(w)
#    print ("Depen = {}".format(Depen))
    if Depen:
        RecursiveFind(Depen)

    for i in Depen:
        depenCeption = nuke.Node.dependencies(i)
#        print ("depenCeption = {}".format(depenCeption))

print ("writeNodeLIST = {}".format(writeNodeLIST))   
print ("RenderLocationLIST = {}".format(RenderLocationLIST))
print ("readNodeLIST = {}".format(readNodeLIST))
print ("FrameRangeLIST = {}".format(FrameRangeLIST))

class NukeRenderCheck_Test(QObject):
    start_task = Signal()
    stopped = Signal()
    finished = Signal()
    progress = Signal(int)
    def __init__(self,interval,fail_interval,FrameRange,RenderLocation):
        super().__init__()
        self._timer      = None
        self.fail_timer      = None
        self.interval     = interval
        self.fail_interval     = fail_interval
        self.FrameRange   = FrameRange
        self.imagesNumber = 0
        self.prevImagesNumber = 0
        self.failCounter = 0
        RenderPathFolder = RenderLocation.split("/")[:-1]
        RenderPathFolder="/".join(RenderPathFolder)
        RenderPathFolder=RenderPathFolder.replace("'","")
        print("RenderPathFolder = {}".format(RenderPathFolder))
        self.RenderLocation = RenderPathFolder
    #    self.args         = args
    #    self.kwargs       = kwargs
        self.inkrement = 0
        self.StudioName   = "Tippett"


        self.RemovePreviousRender_Timer = QTimer()
        self.RemovePreviousRender_Timer.timeout.connect(self.RemovePreviousRender)
        self.RemovePreviousRender()
        
    #    self.start_task.connect(self.run_task)

        self.timer1 = QTimer()
        self.timer1.setInterval(interval * 1000)
        self.timer1.timeout.connect(self.CheckNukeRenderStatus)

        self.timer2 = QTimer()
        self.timer2.setInterval(fail_interval * 1000)
        self.timer2.timeout.connect(self.CheckForFailiure)

        

        self.run_task()
    #    self.start_task.emit()

    def RemovePreviousRender(self):
        try:
            for path in Path(self.RenderLocation).glob("**/*"):
                if path.is_file():
                    path.unlink()
                elif path.is_dir():
                    rmtree(path)
            self.RemovePreviousRender_Timer.stop()
        except PermissionError:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            self.RemovePreviousRender_Timer.start(10 * 1000) # Try again in 10 seconds

    def run_task(self):
        self.timer1.start()
        self.timer2.start()
        #self.RemovePreviousRender()
        print("started")

    def stop(self):
     #   print("Stopping")
        self.timer1.stop()
        self.timer2.stop()

    def CheckForFailiure(self):
        if self.prevImagesNumber < self.imagesNumber:
            self.prevImagesNumber = self.imagesNumber
            self.failCounter = 0

        elif self.prevImagesNumber == self.imagesNumber:
            self.failCounter += 1
    #        print ("self.failCounter = {}".format(self.failCounter))

        elif self.prevImagesNumber > self.imagesNumber:
            self.failCounter += 1
     #       print ("self.failCounter = {}".format(self.failCounter))

    def Nuke_The_Nuke_Process(self):
        self.NukeLogs = r"\\fs3\Sh1\uber\Nuke_Scripts\NukeScripts\NukeLogs\\"
        self.NukeRenderFile = self.NukeLogs + "{}.txt".format(Nuke_ActualFileName)
        with open(self.NukeRenderFile) as nrf:
            NukeRenderText = nrf.readlines()
            for line in NukeRenderText:
                if "{}".format(Nuke_ActualFileName) in line:
                    line = line.split("=")[-1]
                    self.NukeTruth = line
        #            print ("self.NukeTruth = {}".format(self.NukeTruth))
                    
        #    print ("NukeRenderText = {}".format(NukeRenderText))
        if self.NukeTruth == "True":
            self.stopped.emit()
            self.stop()


    def CheckNukeRenderStatus(self):
        self.Nuke_The_Nuke_Process()
        FirstFrame = self.FrameRange.split("-")[-2]
        LastFrame = self.FrameRange.split("-")[-1]
        FirstFrame = int(FirstFrame.replace("'",""))
        LastFrame = int(LastFrame.replace("'",""))
    #    print("FirstFrame = {}".format(FirstFrame))
    #    print("LastFrame = {}".format(LastFrame))
        self.CompleteImageCount = (LastFrame - FirstFrame) + 1
    #    print ("self.CompleteImageCount = {}".format(self.CompleteImageCount))
        count = 0.0
        #for root_dir, cur_dir, files in os.walk(self.RenderLocation):
        for img in os.listdir(self.RenderLocation):
            if not img.endswith(".tmp") and not img.endswith(".mov") and not img.endswith(".nk"):
                count += 1
    #    print('file count:', count)
        self.imagesNumber = count
        self.NukePercentageTest = (count / self.CompleteImageCount) * 100
    #    print ("self.NukePercentageTest = {}".format(self.NukePercentageTest))
        self.NukePercentage = int(self.NukePercentageTest)
    #    print ("self.NukePercentage = {}".format(self.NukePercentage))
        self.progress.emit(self.NukePercentage)
        
        
        if self.failCounter > 9:
        #    print("ABORTION")
            self.stop()

        if self.NukePercentage == 100:
            self.finished.emit()
            self.stop()

            


##########################################


##########################################
class NukeRenderCheck(QObject):
    start_task = Signal()
    stopped = Signal()
    finished = Signal()
    progress = Signal(int)
    def __init__(self,interval,fail_interval,function,fail_function,FrameRange,RenderLocation):
        super().__init__()
        self._timer      = None
        self.fail_timer      = None
        self.interval     = interval
        self.fail_interval     = fail_interval
        self.function     = function
        self.fail_function     = fail_function
        self.FrameRange   = FrameRange
        self.imagesNumber = 0
        self.prevImagesNumber = 0
        self.failCounter = 0
        RenderPathFolder = RenderLocation.split("/")[:-1]
        RenderPathFolder="/".join(RenderPathFolder)
        RenderPathFolder=RenderPathFolder.replace("'","")
        print("RenderPathFolder = {}".format(RenderPathFolder))
        self.RenderLocation = RenderPathFolder
    #    self.args         = args
    #    self.kwargs       = kwargs
        self.is_running   = False
        self.fail_is_running   = False
        self.start()
        self.fail_start()
        self.inkrement = 0
        self.StudioName   = "Tippett"
        self.RemovePreviousRender()
    def RemovePreviousRender(self):
        for path in Path(self.RenderLocation).glob("**/*"):
            if path.is_file():
                path.unlink()
            elif path.is_dir():
                rmtree(path)

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
        if self.prevImagesNumber < self.imagesNumber:
            self.prevImagesNumber = self.imagesNumber
            self.failCounter = 0

        elif self.prevImagesNumber == self.imagesNumber:
            self.failCounter += 1
            print ("self.failCounter = {}".format(self.failCounter))

        elif self.prevImagesNumber > self.imagesNumber:
            self.failCounter += 1
            print ("self.failCounter = {}".format(self.failCounter))

    def Nuke_The_Nuke_Process(self):
        self.NukeLogs = r"\\fs3\Sh1\uber\Nuke_Scripts\NukeScripts\NukeLogs\\"
        self.NukeRenderFile = self.NukeLogs + "{}.txt".format(Nuke_ActualFileName)
        with open(self.NukeRenderFile) as nrf:
            NukeRenderText = nrf.readlines()
            for line in NukeRenderText:
                if "{}".format(Nuke_ActualFileName) in line:
                    line = line.split("=")[-1]
                    self.NukeTruth = line
                    print ("self.NukeTruth = {}".format(self.NukeTruth))
                    
            print ("NukeRenderText = {}".format(NukeRenderText))
        if self.NukeTruth == "True":
            self.stopped.emit()
            self.stop()


    def CheckNukeRenderStatus(self):
        self.Nuke_The_Nuke_Process()
        FirstFrame = self.FrameRange.split("-")[-2]
        LastFrame = self.FrameRange.split("-")[-1]
        FirstFrame = int(FirstFrame.replace("'",""))
        LastFrame = int(LastFrame.replace("'",""))
        print("FirstFrame = {}".format(FirstFrame))
        print("LastFrame = {}".format(LastFrame))
        self.CompleteImageCount = (LastFrame - FirstFrame) + 1
        print ("self.CompleteImageCount = {}".format(self.CompleteImageCount))
        count = 0.0
        #for root_dir, cur_dir, files in os.walk(self.RenderLocation):
        for img in os.listdir(self.RenderLocation):
            if not img.endswith(".tmp") and not img.endswith(".mov") and not img.endswith(".nk"):
                count += 1
        print('file count:', count)
        self.imagesNumber = count
        self.NukePercentageTest = (count / self.CompleteImageCount) * 100
    #    print ("self.NukePercentageTest = {}".format(self.NukePercentageTest))
        self.NukePercentage = int(self.NukePercentageTest)
        print ("self.NukePercentage = {}".format(self.NukePercentage))
        self.progress.emit(self.NukePercentage)
        
        
        if self.failCounter > 9:
            print("ABORTION")
            self.stop()

        if self.NukePercentage == 100:
            self.finished.emit()
            self.stop()
            


##########################################
class Ui_MainWindow(QMainWindow):
    def __init__(self,Frame_Range,RenderLocation):
        super(Ui_MainWindow, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.ui.pushButton.setEnabled(False)
        self.ui.progressBar.setValue(0) # 255, 85, 127
        self.ui.progressBar.setFormat("Initializing ...")
        try:
            self.setWindowTitle("{}".format(Nuke_ActualFileName))
        except:
            pass
        NukeStylesheet = """
                            QProgressBar{
                                color: white;
                                border: 2px solid grey;
                                border-radius 5px;
                                text-align: center;
                            }

                            QProgressBar::chunk{
                                background-color: #cf0c0c ;
                                width 10px;
                            }
                            """
        self.start_time = time.time()
        self.render_time = None
        self.resize(405, 177)
        
        self.ui.progressBar.setStyleSheet(NukeStylesheet)
        self.Canceled = False

        self.Frame_Range = Frame_Range
        self.RenderLocation = RenderLocation
        self.RenderPathFolder = RenderLocation.split("/")[:-1]
        self.RenderPathFolder="/".join(self.RenderPathFolder)
        self.RenderPathFolder=self.RenderPathFolder.replace("'","")

        self.NukeLogs = r"\\fs3\Sh1\uber\Nuke_Scripts\NukeScripts\NukeLogs\\"
        self.NukeRenderFile = self.NukeLogs + "{}.txt".format(Nuke_ActualFileName)
        NukeTruth = "{}={}".format(Nuke_ActualFileName,self.Canceled)
        with open (self.NukeRenderFile,"w") as file:
                    file.writelines(NukeTruth)

        self.runLongTask()
        self.ui.pushButton.clicked.connect(lambda: self.CloseUI_And_Show_Da_Wae())
        if StudioName == "Tippett":
            self.ui.pushButton.setText("Activate Phase 2 and 3")
    

    def reportProgress(self, nukePercengage):
        if nukePercengage > 0:
            self.ui.progressBar.setProperty("value", nukePercengage)
            self.ui.progressBar.setFormat(str(nukePercengage)+ "%")

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
        
        NukeTruth = "{}={}".format(Nuke_ActualFileName,self.Canceled)
        with open (self.NukeRenderFile,"w") as file:
            file.writelines(NukeTruth)


        self.close()

        #return UI_Canceled_Status

    def CloseUI_And_Show_Da_Wae(self):
    #    self.WindowzRenderLocation = self.RenderLocation.replace("/","\\")
    #    self.WindowzRenderLocation = self.RenderPathFolder + "/"
        webbrowser.open(os.path.realpath(self.RenderPathFolder))
    #    webbrowser.open(os.path.realpath(self.WindowzRenderLocation))
    #    os.startfile(self.WindowzRenderLocation)
        self.close()
        if StudioName == "Tippett":
            Args2 =[r"C:\Program Files\Nuke13.1v3\Nuke13.1.exe", r"\\fs3\Sh1\uber\Nuke_Scripts\NukeScripts\Nuke_Create_Tippett_NukeFile.py", self.RenderPathFolder,self.RenderLocation,Frame_Range,Nuke_FileName]
            Executa2 = subprocess.run(Args2)
            print("Tippett Phase 2 Completed")
            Args3 =[r"C:\Program Files\Nuke13.1v3\Nuke13.1.exe", r"\\fs3\Sh1\uber\Nuke_Scripts\NukeScripts\Nuke_PostMortem.py", self.RenderPathFolder,self.RenderLocation,Frame_Range,Nuke_FileName]
            Executa3 = subprocess.run(Args3)
            print("Tippett Phase 3 Completed")
            for pngs in os.listdir(self.RenderPathFolder):
                if pngs.endswith(".png"):
                    os.remove(os.path.join(self.RenderPathFolder,pngs))
                elif pngs.endswith(".nk"):
                    os.remove(os.path.join(self.RenderPathFolder,pngs))
                elif pngs.endswith(".tmp"):
                    os.remove(os.path.join(self.RenderPathFolder,pngs))

    def STAHP(self):
        self.end_time = time.time()
        self.render_time = self.end_time - self.start_time
        self.Render_Time_Label = QLabel(self)
        self.Render_Time_Label.setAlignment(Qt.AlignCenter)
        self.Render_Time_Label.setGeometry(self.width() //2 - 100 ,self.height()-32,200,25)
        #self.Render_Time_Label.setGeometry(200,30,200,30)
        
        self.Render_Time_Label.setStyleSheet(
        "QLabel {"
        "color: rgb(196,63,63);"  #Red
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

        #self.Render_Time_Label.setText("Render time: {:.2f} seconds".format(self.render_time))

        self.Render_Time_Label.show()
        

    def runLongTask(self):
        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        if importes_pyside2 == True:
            self.worker = NukeRenderCheck_Test(3,13,self.Frame_Range,self.RenderLocation)
        else:
            self.worker = self.worker = NukeRenderCheck(3,13,NukeRenderCheck.CheckNukeRenderStatus,NukeRenderCheck.CheckForFailiure,self.Frame_Range,self.RenderLocation)
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
       # self.thread.started.connect(self.worker.run)
        self.thread.finished.connect(lambda: self.ui.pushButton.setEnabled(True))
        self.thread.finished.connect(lambda: self.STAHP())
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.worker.stopped.connect(self.thread.quit)
    #    self.worker.stopped.connect(self.worker.deleteLater)
        #self.thread.stopped.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.reportProgress)
        # Step 6: Start the thread
        self.thread.start()
        #self.worker.start_task.emit()
        

#################################################################
def StartConnection(NukeBoolean,data,Frame_Range,WriteNodes,RenderLocation,index=0,writeNodeLIST_Length=0,MultiRender=False):

    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        
        # Connect to server and send data
        try:
            sock.connect((HOST, PORT))
        except ConnectionRefusedError:
            nuke.message("Render Farm is not Online!")
    #    sock.sendall(bytes(NukeBoolean))  
        sock.sendall(bytes("\n".join(map(str,[NukeBoolean,data,Frame_Range,WriteNodes,RenderLocation,StudioName,])),encoding="utf-8"))
    #    sock.sendall(bytes("\n".join([Frame_Range,WriteNodes])))
        
        # Receive data from the server and shut down
        received = str(sock.recv(2048))
    #    sleep(10)
    #    app = QApplication(sys.argv)
        if MultiRender==False:
        #    app = QApplication.instance()
        #    if app == None:
        #        app = QApplication(sys.argv)
            win = Ui_MainWindow(Frame_Range,RenderLocation)
            try:
                win.setWindowIcon(QIcon(r"\\fs3\Sh1\uber\Master\MayaScripts_2018\vertigo_shelf\icons\O_Nuke_F_Icon.png"))
            except:
                pass
            win.show()
            if importes_pyside2 == True:
            #    app.exec_()
                pass
            else:
                pass
        #        app.exec()
        #    app.setQuitOnLastWindowClosed(True)
        #    app.lastWindowClosed.connect(win.UI_Check_Close)
    #    NukeRenderCheck(5,NukeRenderCheck.CheckNukeRenderStatus,Frame_Range,RenderLocation)
        elif MultiRender:
            JobStatus = str(sock.recv(2048))
            print ("JobStatus = {}".format(JobStatus))
            if JobStatus and index <= (writeNodeLIST_Length-1):
                WriteNodes = writeNodeLIST[index]
                WriteNodeRead = WriteNodes
                RenderLocation=WriteNodeRead["file"].value()
                Frame_Range = FrameRangeLIST[index]
                WriteNodesName = WriteNodes['name'].value()
                print ("writeNodeLIST_Length = {}".format(writeNodeLIST_Length))
                print ("index = {}".format(index))
                if index <= (writeNodeLIST_Length-1):
                    StartConnection(NukeBoolean,data,Frame_Range,WriteNodesName,RenderLocation,index=index+1,writeNodeLIST_Length=writeNodeLIST_Length,MultiRender=True)
    #    
    #        print()
    print("Sent:     {}".format(data))
    print("Received: {}".format(received))
    #except:
    #    print("FrameServer Offline or Unreachable")


    #for WriteNodes in nuke.allNodes("Write"):
    #    FnNsFrameServer.renderFrames(Nuke_FileName, Frame_Range, WriteNodes, ["main"])

#################################################################

#################################################################
class OpeningWindow(QMainWindow):
    def __init__(self):
        super(OpeningWindow, self).__init__()
        self.ui = Ui_Opening()
        self.ui.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        

        #
        NavigationFont_ID = QFontDatabase.addApplicationFont(r"\\fs3\Sh1\uber\Nuke_Scripts\fonts\MonoBold.ttf")
        EternalFont_ID = QFontDatabase.addApplicationFont(r"\\fs3\Sh1\uber\Nuke_Scripts\fonts\EternalUiBold.ttf")


        #Opkrop_ID = QFontDatabase.addApplicationFont(r"C:C:\Users\Damjan\Desktop\fonts\Opkrop.otf")

        if (EternalFont_ID<0):
            print("ERRA")
        else:
            print("NO ERRA")

            
        NavigationFont_families = QFontDatabase.applicationFontFamilies(NavigationFont_ID)
        EternalFont_families = QFontDatabase.applicationFontFamilies(EternalFont_ID)
        #
        self.ui.label.setFont(QtGui.QFont(EternalFont_families[0], 15))
        NukeStylesheet = """color: rgb(232,11,11)"""
        self.ui.label.setStyleSheet(NukeStylesheet)
        QtCore.QTimer.singleShot(4000,self.close)


class FrameRangeWindow(QMainWindow): 
    closed = Signal()
    def __init__(self,FirstFrame,LastFrame,FirstFrameTippett=None):
        super(FrameRangeWindow, self).__init__()
        self.ui = Ui_FrameRangeWindow()
        self.ui.setupUi(self)
        #self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.ui.RenderButton.setStyleSheet(
        "QPushButton\n"
        "{\n"
        "   background-color: rgb(30, 127, 82);\n"
        "   border-radius:12px;\n"
        "}\n"
        
        "QPushButton:hover\n"
        "{\n"
        "   background-color: rgb(30, 127, 82);\n"
        "   border-radius:12px;\n"
        "    border: 1px solid yellow;\n"
        "    color: white;\n"
        "}\n"
        )
        self.ui.CancelButton.setStyleSheet(
        "QPushButton\n"
        "{\n"
        "   background-color: rgb(154, 0, 0);\n"
        "   border-radius:12px;\n"
        "}\n"
        
        "QPushButton:hover\n"
        "{\n"
        "   background-color: rgb(154, 0, 0);\n"
        "   border-radius:12px;\n"
        "    border: 1px solid yellow;\n"
        "    color: white;\n"
        "}\n"
        )
        self.ui.RenderButton.setDefault(True)
        self.ui.RenderButton.clicked.connect(self.Render)
        self.ui.CancelButton.clicked.connect(self.Cancel)
        #
        NavigationFont_ID = QFontDatabase.addApplicationFont(r"\\fs3\Sh1\uber\Nuke_Scripts\fonts\MonoBold.ttf")
        EternalFont_ID = QFontDatabase.addApplicationFont(r"\\fs3\Sh1\uber\Nuke_Scripts\fonts\EternalUiBold.ttf")

        if (EternalFont_ID<0):
            print("ERRA")
        else:
            print("NO ERRA")

            
        NavigationFont_families = QFontDatabase.applicationFontFamilies(NavigationFont_ID)
        EternalFont_families = QFontDatabase.applicationFontFamilies(EternalFont_ID)
        #
        #self.ui.label.setFont(QtGui.QFont(EternalFont_families[0], 15))
        #NukeStylesheet = """color: rgb(232,11,11)"""
        #self.ui.label.setStyleSheet(NukeStylesheet)
        self.First_Frame = 0
        self.Last_Frame = 0
        self.FirstFrame = str(FirstFrame)
        self.LastFrame = str(LastFrame)
        self.FirstFrameTippett = str(FirstFrameTippett)
        self.Canceled = False # True
        self.ui.FirstFrame.setText(self.FirstFrame)
        self.ui.LastFrame.setText (self.LastFrame)
        onlyInt = QIntValidator()
        onlyInt.setRange(0,900000)
        self.ui.FirstFrame.setValidator(onlyInt)
        self.ui.LastFrame.setValidator(onlyInt)
        self.ui.FirstFrame.setMaxLength(6)
        self.ui.LastFrame.setMaxLength(6)
        self.ui.OneFrameCheckBox.stateChanged.connect(self.OneFrame)
    
    def keyPressEvent(self,event):
    
        if event.key() == QtCore.Qt.Key_Enter or event.key() == QtCore.Qt.Key_Return :
            print("ENTER PRESSED")
            self.Render()    
        elif event.key() == QtCore.Qt.Key_Escape :
            print("ESCAPING")
            self.Cancel()

    def Render(self):
        print("Rendering")
        self.Canceled = False
        self.First_Frame = self.ui.FirstFrame.text()
        self.Last_Frame = self.ui.LastFrame.text()
        print ("First_Frame = {}".format(self.First_Frame))
        print ("Last_Frame = {}".format(self.Last_Frame))
        self.close()
    

    def Cancel(self):
        print("Canceled")
        self.Canceled = True
        self.close()

    def closeEvent(self,event):
        self.closed.emit()
        super(FrameRangeWindow,self).closeEvent(event)

    def OneFrame(self):
        self.OneFrameCheck = self.ui.OneFrameCheckBox.isChecked()
        print ("OneFrameCheck = {}".format(self.OneFrameCheck))
        if self.OneFrameCheck == True:
            if StudioName == "Tippett":
                self.ui.FirstFrame.setText(self.FirstFrameTippett)
                self.ui.LastFrame.setText (self.FirstFrameTippett)
            else:
                self.ui.FirstFrame.setText(self.FirstFrame)
                self.ui.LastFrame.setText (self.FirstFrame)
        else:
            self.ui.FirstFrame.setText(self.FirstFrame)
            self.ui.LastFrame.setText (self.LastFrame)
        #self.close()        


#################################################################



HOST, PORT = "10.100.20.139", 9999

NukeBoolean = True
data = Nuke_FileName

writeNodeLIST_Length = len(writeNodeLIST)
if (writeNodeLIST_Length == 1):
    OneFrame = False
    Cancel = False

    def Continue_One_Write_Render(NukeBoolean,data,Frame_Range,WriteNodesName,RenderLocation,Frame_Range_FIRSTFRAME,Frame_Range_LASTFRAME,OneFrame):
        print("OneFrame = {}".format(OneFrame))
        if OneFrame == True:
            print("One FRAME")
            nuke.execute(WriteNodesName,int(Frame_Range_FIRSTFRAME),int(Frame_Range_LASTFRAME))
            RenderLocationSplit = RenderLocation.split("/")[:-1]
            RenderLocationJoin = "/".join(RenderLocationSplit)
            RenderLocation = RenderLocation.replace("/","\\")

            RenderLocation = r"{}".format(RenderLocation)
            print("RenderLocationJoin = {}".format(RenderLocationJoin))

            for x in os.listdir(RenderLocationJoin):
                if x.endswith(".jpg") or x.endswith(".png"):
                    print(x)
                    #Arguements = [r"\\fs3\Sh1\uber\Nuke_Scripts\NukeScripts\Python_3.10_VENV\Scripts\python.exe",r'\\fs3\Sh1\uber\Nuke_Scripts\NukeScripts\Python_3.10_VENV\NukeScripts\OneImage.py',RenderLocation]
                    Arguements = [r"\\fs3\Sh1\uber\Nuke_Scripts\NukeScripts\Python310\python.exe",r'\\fs3\Sh1\uber\Nuke_Scripts\NukeScripts\Python_3.10_VENV\NukeScripts\OneImage.py',RenderLocation]
                    subprocess.Popen(Arguements)
                #    appOpen = QApplication.instance()
                    if appOpen == None:
                        appOpen = QApplication(sys.argv)
                    opn = OpeningWindow()
                    opn.show()
                    if importes_pyside2 == True:
                        appOpen.exec_()
                    else:
                        appOpen.exec()
                    break

        else:
            print("Not One Frame")
            StartConnection(NukeBoolean,data,Frame_Range,WriteNodesName,RenderLocation)

    def Check_Close():
        Canceled_Status = frw.Canceled     
        print ("Canceled_Status = {}".format(frw.Canceled))
        return Canceled_Status

    def Proceed(NukeBoolean,data,Frame_Range,RenderLocation,Frame_Range_FIRSTFRAME,Frame_Range_LASTFRAME,OneFrame):
    #    appFrameWindow.setQuitOnLastWindowClosed(True)
    #    appFrameWindow.lastWindowClosed.connect(Check_Close)
        print ("frw.First_Frame = {}".format(frw.First_Frame))
        print ("frw.Last_Frame = {}".format(frw.Last_Frame))
        
    #    try:
        #Frame_Range = nuke.getInput("Frame Range", frame_ranges)
        #Frame_Range = Frame_Range.split("-")
        #Frame_Range_FIRSTFRAME = Frame_Range[0]
        #Frame_Range_LASTFRAME = Frame_Range[1]
        Frame_Range_FIRSTFRAME = frw.First_Frame
        Frame_Range_LASTFRAME = frw.Last_Frame
    # Canceled = frw.Canceled
        Canceled = Check_Close()
        print ("Canceled = {}".format(Canceled))
        if type(Frame_Range_FIRSTFRAME) != str:
            Frame_Range_FIRSTFRAME = str(Frame_Range_FIRSTFRAME)
        if type(Frame_Range_LASTFRAME) != str:
            Frame_Range_LASTFRAME = str(Frame_Range_LASTFRAME)
        print (type(Frame_Range_FIRSTFRAME))
        print (type(Frame_Range_LASTFRAME))
        print ("Frame_Range_FIRSTFRAME = {}".format(Frame_Range_FIRSTFRAME))
        print ("Frame_Range_LASTFRAME = {}".format(Frame_Range_LASTFRAME))
        Frame_Range = Frame_Range_FIRSTFRAME + "-" + Frame_Range_LASTFRAME
        print ("Frame_Range = {}".format(Frame_Range))

        if Frame_Range_FIRSTFRAME == Frame_Range_LASTFRAME:
            OneFrame = True
    #    except:
    #        Frame_Range = nuke.getInput("Frame Range", )
        WriteNodes = writeNodeLIST[0]
        WriteNodeRead = WriteNodes
        RenderLocation=WriteNodeRead["file"].value()
        WriteNodesName = WriteNodes['name'].value()
        print("data = {}".format(data))
        print("Frame_Range = {}".format(Frame_Range))
    #    print("WriteNodes = {}".format(WriteNodes))
        print("RenderLocation = {}".format(RenderLocation))

        #def Continue_One_Write_Render(Frame_Range_FIRSTFRAME,Frame_Range_LASTFRAME,OneFrame,WriteNodesName,RenderLocation,Frame_Range,data,NukeBoolean):

        
        if Canceled == False:
            Continue_One_Write_Render(NukeBoolean,data,Frame_Range,WriteNodesName,RenderLocation,Frame_Range_FIRSTFRAME,Frame_Range_LASTFRAME,OneFrame)
        elif Canceled == True:
            print("Render Cancelled")
    try:
        #frame_ranges = nukescripts.renderdialog._gRenderDialogState.getValue('frame_range_string')
        frame_ranges = FrameRangeLIST[0]
        if frame_ranges == None or frame_ranges == '':
            frame_ranges = FrameRangeLIST[0]
            if StudioName == "Tippett":
                frame_ranges = frame_ranges.split("-")
                frame_ranges_FIRSTFRAME = frame_ranges[0]
                frame_ranges_FIRSTFRAME = int(frame_ranges_FIRSTFRAME)-1
                frame_ranges_FIRSTFRAME = str(frame_ranges_FIRSTFRAME)
                frame_ranges_LASTFRAME = frame_ranges[1]
                print (type(frame_ranges_FIRSTFRAME))
                print (type(frame_ranges_LASTFRAME))
                print ("frame_ranges_FIRSTFRAME = {}".format(frame_ranges_FIRSTFRAME))
                print ("frame_ranges_LASTFRAME = {}".format(frame_ranges_LASTFRAME))
                frame_ranges = frame_ranges_FIRSTFRAME + "-" + frame_ranges_LASTFRAME
                print ("frame_ranges = {}".format(frame_ranges))

            #    frame_ranges = "".join(frame_ranges)
            #    print ("frame_ranges = {}".format(frame_ranges))
        print ("frame_ranges = {}".format(frame_ranges))
    except:
        
        pass


    Frame_Range = frame_ranges.split("-")
    print ("Frame_Range = {}".format(Frame_Range))
    Frame_Range_FIRSTFRAME = int(Frame_Range[0])
    Frame_Range_LASTFRAME =  int(Frame_Range[1])
    
    appFrameWindow = QApplication.instance()
    if appFrameWindow == None:
        appFrameWindow = QApplication(sys.argv)
    
    
    if importes_pyside2 == True:
        if StudioName == "Tippett":
            frw = FrameRangeWindow(Frame_Range_FIRSTFRAME,Frame_Range_LASTFRAME,Frame_Range_FIRSTFRAME + 1)
        else:
            frw = FrameRangeWindow(Frame_Range_FIRSTFRAME,Frame_Range_LASTFRAME)
        
        appFrameWindow.exec_()
        frw.setFocus()
        frw.show()
        frw.closed.connect(lambda:Proceed(NukeBoolean,data,Frame_Range,RenderLocation,Frame_Range_FIRSTFRAME,Frame_Range_LASTFRAME,OneFrame))
    #    frw.activateWindow()
        

        
        #while frw.isVisible():
        #    QCoreApplication.processEvents()
        
    #    event_loop = QEventLoop()
    #    timer = QtCore.QTimer()
    #    def check_window_closed():
    #        if not frw.isVisible():
    #            event_loop.quit()
    #    timer.timeout.connect(check_window_closed)
    #    timer.start(100)
    #    event_loop.exec_()
        print("Window Closed")
    #    frw.closed.connect(event_loop.quit)
    #    event_loop.exec_()
    else:
       # appFrameWindow = QApplication.instance()
        if appFrameWindow == None:
            appFrameWindow = QApplication(sys.argv)
        if StudioName == "Tippett":
            frw = FrameRangeWindow(Frame_Range_FIRSTFRAME,Frame_Range_LASTFRAME,Frame_Range_FIRSTFRAME + 1)
        else:
            frw = FrameRangeWindow(Frame_Range_FIRSTFRAME,Frame_Range_LASTFRAME)
        
        frw.setFocus()
        #frw.activateWindow()
        frw.closed.connect(lambda:Proceed(NukeBoolean,data,Frame_Range,RenderLocation,Frame_Range_FIRSTFRAME,Frame_Range_LASTFRAME,OneFrame))
        
        frw.show()
        appFrameWindow.exec()
    

elif (writeNodeLIST_Length > 1):
    for index,wn in enumerate(writeNodeLIST):
        WriteNodes = writeNodeLIST[index]
        WriteNodeRead = WriteNodes
        RenderLocation=WriteNodeRead["file"].value()
        Frame_Range = FrameRangeLIST[index]
        WriteNodesName = WriteNodes['name'].value()
        print("WriteNodes = {}".format(WriteNodes['name'].value()))
        print("Frame_Range = {}".format(Frame_Range))
        print("RenderLocation = {}".format(RenderLocation))
        StartConnection(NukeBoolean,data,Frame_Range,WriteNodesName,RenderLocation,1,writeNodeLIST_Length,MultiRender=True)
        break
