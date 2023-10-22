import os,webbrowser,nuke,nukescripts
import os,shutil

import socket
import sys
from contextlib import closing
from threading import Timer
import time

import sys
# sys.path.append(r"\\fs3\Sh1\uber\Nuke_Scripts")
sys.path.append(r"C:\Users\Dame\Desktop\S")
sys.path.append(r"C:\Users\Dame\AppData\Local\Programs\Python\Python310\Lib\site-packages")


import psutil

try:
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
except psutil.NoSuchProcess:
    importes_pyside2 = True
print("importes_pyside2 = {}".format(importes_pyside2))


def Undist_Crop(ShotName,render_Path,jpg_Path,Version):
    for a in nuke.allNodes():
        nuke.delete(a)
    NukeVersion = nuke.NUKE_VERSION_MAJOR
    
    if NukeVersion == 10:
        try:
            from progressBarUI2 import Ui_Form

            from PySide.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                QMetaObject, QObject, QPoint, QRect,
                QSize, QTime, QUrl, Qt, Signal,QThread)
            from PySide.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
                QFont, QFontDatabase, QGradient, QIcon,
                QImage, QKeySequence, QLinearGradient, QPainter,
                QPalette, QPixmap, QRadialGradient, QTransform)
            from PySide.QtWidgets import (QApplication, QLabel, QMainWindow, QProgressBar,
                QPushButton, QSizePolicy, QStatusBar, QWidget)
        except:
            pass    
    elif NukeVersion == 13:
        if importes_pyside2 == True:
            from progressBarUI2 import Ui_Form
            from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
            QMetaObject, QObject, QPoint, QRect,
            QSize, QTime, QUrl, Qt, Signal,QThread,QTimer)
            from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
                QFont, QFontDatabase, QGradient, QIcon,
                QImage, QKeySequence, QLinearGradient, QPainter,
                QPalette, QPixmap, QRadialGradient, QTransform)
            from PySide2.QtWidgets import (QApplication, QLabel, QMainWindow, QProgressBar,
                QPushButton, QSizePolicy, QStatusBar, QWidget)
            from pathlib import Path

        else:
            from progressBarUI6 import Ui_Form
            from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                QMetaObject, QObject, QPoint, QRect,
                QSize, QTime, QUrl, Qt, Signal,QThread,QTimer)
            from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
                QFont, QFontDatabase, QGradient, QIcon,
                QImage, QKeySequence, QLinearGradient, QPainter,
                QPalette, QPixmap, QRadialGradient, QTransform)
            from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QProgressBar,
                QPushButton, QSizePolicy, QStatusBar, QWidget)
            from pathlib import Path

    



    print ("NukeVersion = {}".format(NukeVersion))
    print (type(NukeVersion))
    ProjectPath = render_Path.split("\\")[:-2]
    ProjectPath = "/".join(ProjectPath)
    print ("ProjectPath = {}".format(ProjectPath))
    JPGPath=jpg_Path + "\\"
    JPGPath=JPGPath.replace("\\","/")
    print ("JPGPath = {}".format(JPGPath))                  
    for seq in nuke.getFileNameList(JPGPath):
        Split = seq.split(" ")
        Split.pop()
        Split = "".join(Split)
        if Split.endswith(".jpg"):
            Read_JPG = nuke.createNode('Read')
            try:
                Read_JPG.knob('file').fromUserText(JPGPath + seq)
                JPG_FORMAT = Read_JPG['format'].value()
            except:
                pass
    OriginalUndistPath=render_Path + "\\undist" + "\\"
    OriginalUndistPath=OriginalUndistPath.replace("\\","/")
    UndistFolder=os.listdir(OriginalUndistPath)
    for folders in UndistFolder:
        SplitFolderName= folders.split("_")
        Reversed_SplitFolderName = reversed(SplitFolderName)
        print ("OriginalSplitFolderName = {}".format(SplitFolderName))
        LastSLOG = SplitFolderName[-1]
    #    UndistFolderName="_".join(SplitFolderName)
        if LastSLOG=="undist" or LastSLOG =="undistorted":
            for index,v in enumerate(Reversed_SplitFolderName):
                if LastSLOG=="undist" or LastSLOG =="undistorted":
                    if "v00" in v:
                        (SplitFolderName[-index-1]) = Version
                        break

                UndistFolderName="_".join(SplitFolderName)
            print ("UndistFolderName         = {}".format(UndistFolderName))
            print ("LastSLOG         = {}".format(LastSLOG))
            print ("SplitFolderName         = {}".format(SplitFolderName))
    try:
        CropPath = OriginalUndistPath + "{}".format(UndistFolderName) + "_crop" + "/"
    except NameError:
        nuke.message("""Undist folder not found/Incorrectly named.
        Folder must end with '_v001_undist'""")
    if not os.path.exists(CropPath):
        original_umask = os.umask(0)
        os.makedirs(CropPath,mode=0o777  )
    
    UndistPath=render_Path + "\\undist\\"
    UndistPath=UndistPath.replace("\\","/")

    UndistFile=UndistPath + ShotName + ".nk"

    UVDistortPath=render_Path + "\\uvmap\\"
    UVDistortPath=UVDistortPath.replace("\\","/")
    #for files in os.listdir(UndistPath):
    #    if "undist" and not "_crop" in files:
    #        UndistPath+= files + "\\"
    UndistPath+=UndistFolderName + "\\"                 
    print ("OriginalUndistPath = {}".format(OriginalUndistPath))
    print ("CropPath = {}".format(CropPath))
    print ("UVDistortPath = {}".format(UVDistortPath))
    print ("UndistPath = {}".format(UndistPath))
    for seq in nuke.getFileNameList(UndistPath): 
        print ("seq = {}".format(seq))
        try:
            Split = seq.split(" ")
            Split.pop()
            Split = "".join(Split)
            if Split.endswith(".jpg"):
                Read_Undist = nuke.createNode('Read')
                Read_Undist.knob('file').fromUserText(UndistPath + seq)
        except:
            pass
    Read_Undist.setXYpos(Read_JPG.xpos()+140,Read_JPG.ypos())
    ReformatNode = nuke.createNode("Reformat")
    ReformatNode['format'].setValue(JPG_FORMAT)
    ReformatNode['resize'].setValue("none")
    ReformatNode.setXYpos(Read_Undist.xpos(),Read_Undist.ypos()+120)
    WriteUndistCropNode = nuke.createNode("Write")
    WriteUndistCropNode.setXYpos(ReformatNode.xpos(),ReformatNode.ypos()+60)
    #WriteUndistCropNode['file'].setValue(CropPath + "{}".format(ShotName) + "_undist_crop.####.jpg" )
    WriteUndistCropNode['file'].setValue(CropPath + "{}".format(UndistFolderName) + "_crop.####.jpg" )
    WriteUndistCropNode['_jpeg_quality'].setValue(1)
    WriteUndistCropNode['name'].setValue(ShotName + " Crop")

    nuke.selectAll()
    nuke.zoomToFitSelected()
    for node in nuke.selectedNodes():
        node.knob("selected").setValue(False)


    Nuke_FileName = UndistFile
    nuke.scriptSaveAs(Nuke_FileName,overwrite=1)
    Nuke_ActualFileName = Nuke_FileName.split("/")[-1]
    print ("Nuke_ActualFileName = {}".format(Nuke_ActualFileName))

    First_Frame = Read_Undist['first'].value()
    Last_Frame = Read_Undist['last'].value()

    Frame_Range = "{}-{}".format(First_Frame,Last_Frame)
#    try:
#        frame_ranges = nukescripts.renderdialog._gRenderDialogState.getValue('frame_range_string')
#        print ("frame_ranges = {}".format(frame_ranges))
#    except:
#        pass

#    try:
#        Frame_Range = nuke.getInput("Frame Range", frame_ranges)
#    except:
#        Frame_Range = nuke.getInput("Frame Range", )
    #################################################################
    # HOST, PORT = "10.100.20.139", 9999
    HOST, PORT = "192.168.100.4", 9998


    #for WriteNodes in nuke.allNodes("Write"):
    #    data = """FnNsFrameServer.renderFrames(Nuke_FileName, Frame_Range, WriteNodes, ["main"])"""
    WriteNodes = WriteUndistCropNode['name'].value()
    #WriteNodes = "Write1"
    #WriteNodeRead = nuke.toNode("Write1")
    RenderLocation=WriteUndistCropNode["file"].value()
    NukeBoolean = "Undist"
    #data = """FnNsFrameServer.renderFrames({Nuke_FileName}, {Frame_Range}, {WriteNodes}, ["main"])""".format(Nuke_FileName=Nuke_FileName,Frame_Range=Frame_Range,WriteNodes=WriteNodes)
    data = Nuke_FileName
    StudioName = "Nebitno"
    print("data = {}".format(data))
    print("Frame_Range = {}".format(Frame_Range))
    print("WriteNodes = {}".format(WriteNodes))
    print("RenderLocation = {}".format(RenderLocation))

    ##########################################
    if NukeVersion == 13:
        class NukeRenderCheck(QObject):
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
            #    self.RemovePreviousRender_Timer = QTimer()
            #    self.RemovePreviousRender_Timer.timeout.connect(self.RemovePreviousRender)
                self.RemovePreviousRender()

            def RemovePreviousRender(self):
                try:
                    for path in Path(self.RenderLocation).glob("**/*"):
                        if path.is_file():
                            path.unlink()
                        elif path.is_dir():
                            rmtree(path)
            #        self.RemovePreviousRender_Timer.stop()
                except PermissionError:
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            #        self.RemovePreviousRender_Timer.start(10 * 1000) # Try again in 10 seconds

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
            #        print ("self.failCounter = {}".format(self.failCounter))

                elif self.prevImagesNumber > self.imagesNumber:
                    self.failCounter += 1
            #        print ("self.failCounter = {}".format(self.failCounter))

            def Nuke_The_Nuke_Process(self):
                # self.NukeLogs = r"\\fs3\Sh1\uber\Nuke_Scripts\NukeScripts\NukeLogs\\"
                self.NukeLogs = r"C:\Users\Dame\Desktop\NukeLogs"
                self.NukeRenderFile = self.NukeLogs + "{}.txt".format(Nuke_ActualFileName)
                with open(self.NukeRenderFile) as nrf:
                    NukeRenderText = nrf.readlines()
                    for line in NukeRenderText:
                        if "{}".format(Nuke_ActualFileName) in line:
                            line = line.split("=")[-1]
                            self.NukeTruth = line
            #                print ("self.NukeTruth = {}".format(self.NukeTruth))
                            
            #        print ("NukeRenderText = {}".format(NukeRenderText))
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
                
            
        #        if self.failCounter > 5:
        #            print("ABORTION")
        #            self.stop()

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
                self.setWindowTitle("{}".format(ShotName))
                #self.ui.progressBar.setStyleSheet(u"color: rgb(255, 85, 127);")
                UndistStylesheet = """
                                    QProgressBar{
                                        color: white;
                                        border: 2px solid grey;
                                        border-radius 5px;
                                        text-align: center;
                                    }

                                    QProgressBar::chunk{
                                        background-color: #ec944c ;
                                        width 10px;
                                    }
                                    """
            #    self.ui.progressBar.setStyleSheet("QProgressBar::chunk"
            #                                    "{"
            #                                    "background-color :  #ec944c;"
            #                                    "border : 1px"
            #                                    "}")
                self.start_time = time.time()
                self.render_time = None
                self.resize(405, 177)
                self.ui.progressBar.setStyleSheet(UndistStylesheet)
                self.Canceled = False

                # self.NukeLogs = r"\\fs3\Sh1\uber\Nuke_Scripts\NukeScripts\NukeLogs\\"
                self.NukeLogs = r"C:\Users\Dame\Desktop\NukeLogs"
                self.NukeRenderFile = self.NukeLogs + "{}.txt".format(Nuke_ActualFileName)
                NukeTruth = "{}={}".format(Nuke_ActualFileName,self.Canceled)
                with open (self.NukeRenderFile,"w") as file:
                            file.writelines(NukeTruth)
                            print("WRITTEN AS FALSE")
                
                self.Frame_Range = Frame_Range
                self.RenderLocation = RenderLocation
                self.runLongTask()
                self.ui.pushButton.clicked.connect(lambda: self.CloseUI_And_Show_Da_Wae())

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

            

            def CloseUI_And_Show_Da_Wae(self):
                path = CropPath
                webbrowser.open(os.path.realpath(path))
                self.close()

            def STAHP(self):
                self.end_time = time.time()
                self.render_time = self.end_time - self.start_time
                self.Render_Time_Label = QLabel(self)
                self.Render_Time_Label.setAlignment(Qt.AlignCenter)
                self.Render_Time_Label.setGeometry(self.width() //2 - 100 ,self.height()-32,200,25)
            
                self.Render_Time_Label.setStyleSheet(
                "QLabel {"
                "color: rgb(196,143,63);"  #Blue
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


            def runLongTask(self):
                # Step 2: Create a QThread object
                self.thread = QThread()
                # Step 3: Create a worker object
                self.worker = NukeRenderCheck(2,13,NukeRenderCheck.CheckNukeRenderStatus,NukeRenderCheck.CheckForFailiure,self.Frame_Range,self.RenderLocation)
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





    if NukeVersion == 10:
        try:
            with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
                # Connect to server and send data
                sock.connect((HOST, PORT))
            #    sock.sendall(bytes(NukeBoolean))
                sock.sendall(bytes("\n".join(map(str,[NukeBoolean,data,Frame_Range,WriteNodes,RenderLocation,None,]))))
            #    sock.sendall(bytes("\n".join([Frame_Range,WriteNodes])))

                # Receive data from the server and shut down
                received = str(sock.recv(2048))

            print("Sent:     {}".format(data))
            print("Received: {}".format(received))
            #Open Folder
            path = CropPath
            webbrowser.open(os.path.realpath(path))

        except:
            #Open Folder
            path = CropPath
            webbrowser.open(os.path.realpath(path))
            nuke.execute(WriteUndistCropNode)
            print("FrameServer Offline or Unreachable")
    elif NukeVersion == 13:
        
    #    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # Connect to server and send data
            sock.connect((HOST, PORT))
        #    sock.sendall(bytes(NukeBoolean))
            sock.sendall(bytes("\n".join(map(str,[NukeBoolean,data,Frame_Range,WriteNodes,RenderLocation,None,])), "utf-8"))
        #    sock.sendall(bytes("\n".join([Frame_Range,WriteNodes])))

            # Receive data from the server and shut down
        #    received = str(sock.recv(2048), "utf-8")
            app = QApplication.instance()
            if app == None:
                app = QApplication(sys.argv)
            QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
            win = Ui_MainWindow(Frame_Range,RenderLocation)
            win.show()
            app.exec_()
        #print("Sent:     {}".format(data))
        #print("Received: {}".format(received))
        #Open Folder
    

    #    except:
    #        #Open Folder
    #        path = CropPath
    #        webbrowser.open(os.path.realpath(path))
    #        nuke.execute(WriteUndistCropNode)
    #        print("FrameServer Offline or Unreachable")



ShotName = "DVX_010_400_BG_V001"
render_Path = r"C:\Users\Dame\Desktop\NUKESTUFF\TPN\FilmLance\DVX\render\DVX_010_400_BG_V001"
jpg_Path = r"C:\Users\Dame\Desktop\NUKESTUFF\TPN\FilmLance\DVX\input\DVX_010_400_BG_V001\Proxy"
Version = "v001"
Undist_Crop(ShotName,render_Path,jpg_Path,Version)
