import sys,subprocess,os,re,time,fileinput
import maya.cmds as mc

sys.path.append(r"\\fs3\Sh1\uber\Nuke_Scripts")
sys.path.append(r"\\fs3\Sh1\uber\Nuke_Scripts\NukeScripts")

from progressBar_FPS import Ui_Form
from Change_FPS import Ui_MainWindow_FPS

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt, Signal,Slot,QThread,QEventLoop,QTimer,QRegularExpression)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform,QIntValidator,QRegularExpressionValidator)
from PySide2.QtWidgets import (QApplication, QLabel, QMainWindow, QProgressBar,
    QPushButton, QSizePolicy, QStatusBar, QWidget, QLineEdit, QCheckBox,QFileDialog)



Maya_Version = str(mc.about(version=True))
Maya_Version = "Maya" + "{}".format(Maya_Version)
print ("Maya_Version = {}".format(Maya_Version))

Pyside2_Apps = ["Maya2020","Maya2022","Maya2023"]
Pyside6_Apps = ["Maya2024"]


if Maya_Version in Pyside2_Apps:
    importes_pyside2 = True
    print(importes_pyside2)
else:
    importes_pyside2 = False

class MayaProgressCheck(QObject):
    start_task = Signal()
    stopped = Signal()
    finished = Signal()
    progress = Signal(int, float)
    def __init__(self,interval,lines,To_Replace,Replaced_by,input_file):
        super().__init__()
        self._timer      = None
        self.fail_timer      = None
        self.interval     = interval
        # self.lines = lines
        self.To_Replace = To_Replace
        self.Replaced_by = Replaced_by
        self.input_file = input_file

        self.FullMayaPath = mc.file(q=True,sn=True)
    #    self.input_file = r"{}".format(self.FullMayaPath)
        self.output_file,ext = os.path.splitext(self.input_file)
        self.output_file = self.output_file + "_FPS" + ext


        self.processed_bytes = 0
        self.total_size = os.path.getsize(self.input_file)
        self.start_open = time.time()
        self.last_progress_time = self.start_open
        # self.outfile = open(self.output_file,"w")

        self.film_replaced = False
    #    self.To_Replace = "film"
    #    self.Replaced_by = "23.976fps"

        self.worker_thread = None 

    def do_work2(self):
        self.processed_bytes = 0
        self.total_size = os.path.getsize(self.input_file)
        self._progress = 0

        line_number = 0  # Initialize line number
        with fileinput.input(files=(self.input_file), inplace=True) as file:
            for line in file:
                if not self.film_replaced and 'currentUnit' in line:
                    line = line.replace(self.To_Replace, self.Replaced_by)
                    self.film_replaced = True
                print(line, end='')  # Write the line

                line_number += 1  # Increment line number

                # Progress calculation and signal emission
                self.processed_bytes += len(line.encode('utf-8'))
                self._progress = int(self.processed_bytes / self.total_size * 100)
                self.elapsed_time = time.time() - self.start_open
                self.speed = self.processed_bytes / self.elapsed_time / (1024 * 1024)

                if time.time() - self.last_progress_time >= 1:
                    # print(f"{self._progress:.2f}% | Speed: {self.speed:.2f} MB/s")
                    self.last_progress_time = time.time()
                    self.progress.emit(self._progress, self.speed)

        # Rename the input file to the output file
        # os.rename(self.input_file, self.output_file)
        self.finished.emit()


    def do_work(self):
        
        with open(self.output_file, "w") as outfile:
            for line in self.lines:
                self.processed_bytes += len(line.encode('utf-8'))

                if not self.film_replaced and 'currentUnit' in line:
                    self.modified_line = line.replace(self.To_Replace, self.Replaced_by)
                    self.film_replaced = True
                else:
                    self.modified_line = line

                outfile.write(self.modified_line)

                # Progress calculation and signal emission
                self._progress = int(self.processed_bytes / self.total_size * 100)
                self.elapsed_time = time.time() - self.start_open
                self.speed = self.processed_bytes / self.elapsed_time / (1024 *1024)

                if time.time() - self.last_progress_time >= 1:
                    # print(f"{self._progress:.2f}% | Speed: {self.speed:.2f} MB/s")
                    self.last_progress_time = time.time()
                    self.progress.emit(self._progress, self.speed)

            self.finished.emit()


class Ui_MainWindow(QMainWindow):
    def __init__(self,lines,To_Replace,Replaced_by,input_file):
        super(Ui_MainWindow, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.ui.pushButton.setEnabled(False)
        self.ui.progressBar.setValue(0) 
        self.ui.progressBar.setFormat("Initializing ...")
        self.lines = lines
        self.worker = None  # Create a worker attribute in the main class
        self.To_Replace = To_Replace
        self.Replaced_by = Replaced_by
        self.input_file = input_file

        FPS_Stylesheet_Save = ("""
                            QProgressBar{
                                color: white;
                                border: 2px solid grey;
                                border-radius 5px;
                                text-align: center;
                            }

                            QProgressBar::chunk{
                                background-color: rgb(186,135,117) ;
                                width 10px;
                            }
                            """
                            )

        self.start_time = time.time()
        self.render_time = None
        self.resize(405, 177)
        self.ui.progressBar.setStyleSheet(FPS_Stylesheet_Save)
        self.Canceled = False

        
        self.runLongTask()
        self.ui.pushButton.clicked.connect(lambda: self.UI_Check_Close())

    def reportProgress(self, nukePercengage, speed):
        if nukePercengage > 0:
            self.ui.progressBar.setProperty("value", nukePercengage)
            self.ui.progressBar.setFormat(f"{nukePercengage:}% | Speed: {speed:.2f} MB/s")

    def closeEvent(self,event):
        print("EVENT CLOSING")
        try:
            self.UI_Check_Close()
            event.accept() # let the window close
        except:
            print("Close Event has failed")
            event.ignore()


    def UI_Check_Close(self):
        self.close()
        # self.worker.stop()


    def CloseUI_And_Show_Da_Wae(self):
        path = CropPath
        webbrowser.open(os.path.realpath(path))
        self.close()

    def STAHP(self):

        self.ui.progressBar.setProperty("value", 100)
        self.ui.progressBar.setFormat(str(100)+ "%")

        self.end_time = time.time()
        self.render_time = self.end_time - self.start_time
        self.Render_Time_Label = QLabel(self)
        self.Render_Time_Label.setAlignment(Qt.AlignCenter)
        self.Render_Time_Label.setGeometry(self.width() //2 - 100 ,self.height()-32,200,25)

        self.Render_Time_Label.setStyleSheet(
        "QLabel {"
        "color: rgb(112,204,155);" # Green-Blue
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
            self.Render_Time_Label.setText("Save time: {}:0{} minutes".format(Minutes,Remainder))
        else:
            Render_Time = "{}:{} minutes".format(Minutes,Remainder)
            self.Render_Time_Label.setText("Save time: {}:{} minutes".format(Minutes,Remainder))


        self.Render_Time_Label.show()
        # self.worker.stop()
        
    

    def runLongTask(self):
    
        self.worker = MayaProgressCheck(1, self.lines,self.To_Replace,self.Replaced_by,self.input_file)
        self.thread = QThread()
        self.worker.worker_thread = self.thread

        self.thread.finished.connect(lambda: self.ui.pushButton.setEnabled(True))
        self.thread.finished.connect(lambda: self.STAHP())
        self.thread.started.connect(self.worker.do_work2)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        # self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.reportProgress)
        
        self.worker.moveToThread(self.thread)
        self.thread.start()


        

#################################################################


class OpeningMaya(QObject):
    started = Signal()
    opened = Signal(list)
    
    def __init__(self,input_file):
        super().__init__()
        self.input_file = input_file
        print("self.input_file = {}".format(self.input_file))
        self.started.emit()
        # self.Check_FPS_Value(self.input_file)

    def Check_FPS_Value(self,input_file):
        with open(input_file, "r") as infile:
            for line in infile:
                if 'currentUnit' in line:
                    parts = line.split('-t')
                    if len(parts) > 1:
                        value = parts[1].strip().split()[0].rstrip(';')
                        print("value = {}".format(value))
                        break  # Optional: exit the loop after finding the first occurrence
        return value
    
    @Slot()
    def Open_Maya_File(self,input_file):
        with open(input_file, "r") as infile:
            # self.lines = infile.readlines()
            self.lines = []

        # for line in self.lines:
        #     if 'currentUnit' in line:
        #         parts = line.split('-t')
        #         if len(parts) > 1:
        #             value = parts[1].strip().split()[0].rstrip(';')
        #             print("value = {}".format(value))
        #             break  # Optional: exit the loop after finding the first occurrence

        # Current_FPS_Label
        # Maya_Set_FPS.update_current_fps_label(value)
        self.opened.emit(self.lines)

class Maya_Set_FPS(QMainWindow):
    closed = Signal()
    def __init__(self):
        super(Maya_Set_FPS, self).__init__()
        self.ui = Ui_MainWindow_FPS()
        self.ui.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.ui.TippettButton.setChecked(True)

        self.FullMayaPath = mc.file(q=True,sn=True)
        self.MayaName = mc.file(q=True,sn=True,shn=True)
        self.input_file = r"{}".format(self.FullMayaPath)

        Maya_Version = None
        self.film_replaced = False

        #self.To_Replace = "film"
        #self.Replaced_by = "23.976fps"
        self.To_Replace = ""
        self.Replaced_by = ""
        
        


        self.total_size = os.path.getsize(self.input_file)
        self.start_open = time.time()
        self.last_progress_time = self.start_open
        self.processed_bytes = 0

        self.Continue = False
        self.ui.Change_FPS_Button.setEnabled(False)
        self.ui.Change_FPS_Button.setText("Opening ...")
        
        self.ui.Maya_Name_Label.setText(self.MayaName)
        self.Change_FPS_Stylesheet = """

                            QPushButton{
                                color: black;
                                background-color: rgb(174, 216, 255);
                                font-family: "Segoe UI";
                                font-size: 12px;
                                border-radius 5px;
                                text-align: center;
                            }

                            QPushButton:disabled{
                                color: gray;
                                background-color: rgb(174, 216, 255);
                                font-family: "Segoe UI";
                                font-size: 12px;
                                border-radius 5px;
                                text-align: center;
                            }

                            QPushButton:pressed{
                                color: green;
                                background-color: rgb(174, 216, 255);
                                font-family: "Segoe UI";
                                font-size: 12px;
                                border-radius 5px;
                                text-align: center;
                            }
                            """
        self.ui.BrowseButton.clicked.connect(self.BrowseMaya)

        self.ui.Change_FPS_Button.setStyleSheet(self.Change_FPS_Stylesheet)
        self.ui.Change_FPS_Button.clicked.connect(self.Handle_button_click)

        self.ui.FPS_Value_lineEdit.setStyleSheet("QLineEdit:disabled{ color: rgb(152,101,101);} QLineEdit {color: rgb(73, 152, 255);}")
        self.ui.FPS_Value_lineEdit.setEnabled(False)

        regex = QRegularExpression('^[0-9]{0,3}(\\.[0-9]{0,7})?$')
        validator = QRegularExpressionValidator(regex)
        self.ui.FPS_Value_lineEdit.setValidator(validator)

        self.GetRadioButtonValue()
        self.ui.TippettButton.toggled.connect(self.RadioButtonToggled)
        self.ui.TippettButton.toggled.connect(self.GetRadioButtonValue)
        self.ui.Custom_FPS_Butoon.toggled.connect(self.RadioButtonToggled)
        self.ui.Custom_FPS_Butoon.toggled.connect(self.GetRadioButtonValue)

        self.run_long_task()

    def BrowseMaya(self):
        self.browse_path = r"\\fs3\TPN\Framestore\HOS\3d_comp\lof108_0300_v0043\main3d"
        options = QFileDialog.Options()
       # options |= QFileDialog.DontUseNativeDialog
        self.file_name, _ = QFileDialog.getOpenFileName(
            #self, "Select File","{}".format(self.browse_path),"All Files (*);;Text Files (*.txt)", options=options)
            self, "Select File","{}".format(self.browse_path),"Maya ASCII (*.ma)", options=options)
        if self.file_name:
            self.input_file = r"{}".format(self.file_name)
            print("Selected File: {}".format(self.input_file))
            self.NewMayaName = self.input_file.split("/")
            self.MayaNEW = self.NewMayaName[-1]

            self.ui.Maya_Name_Label.setText(self.MayaNEW)
            self.run_long_task()

    def RadioButtonToggled(self):
        if self.ui.TippettButton.isChecked():
            self.ui.FPS_Value_lineEdit.setEnabled(False)
        else:
            self.ui.FPS_Value_lineEdit.setEnabled(True)

    def GetRadioButtonValue(self):
        if self.ui.TippettButton.isChecked():
            value = self.ui.TippettButton.text()
            if "Tippett" in value:
                value = "23.976fps"
                self.Replaced_by = value
        else:
            value = self.ui.FPS_Value_lineEdit.text()
            value += "fps"
            self.Replaced_by = value
        
        print("Selected Value :  = {}".format(value))

    def closeEvent(self,event):
        #self.closed.emit()
        super(Maya_Set_FPS,self).closeEvent(event)

    def run_long_task(self):
        self.thread = QThread()
        self.worker = OpeningMaya(self.input_file)

        self.FPS_Display_Label_VALUE = self.worker.Check_FPS_Value(self.input_file)
        self.ui.FPS_Display_Label.setText(self.FPS_Display_Label_VALUE)

        self.To_Replace = self.FPS_Display_Label_VALUE
        

        self.worker.started.connect(lambda:self.worker.Open_Maya_File(self.input_file))
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(lambda:self.worker.Open_Maya_File(self.input_file))
        self.worker.opened.connect(self.Enable_Button)
        self.worker.opened.connect(self.thread.quit)
        self.worker.opened.connect(self.thread.quit)
        self.worker.opened.connect(self.worker.deleteLater)
        self.thread.start()

        

    @Slot(list)
    def Enable_Button(self,lines):
        self.lines = lines
        self.ui.Change_FPS_Button.setEnabled(True)
        self.ui.Change_FPS_Button.setText("Change FPS")

    @Slot()
    def Handle_button_click(self):
        self.close()
        self.Write_Maya(self.lines)
        

    def Write_Maya(self,lines):
        print("self.To_Replace = {}".format(self.To_Replace))
        print("self.Replaced_by = {}".format(self.Replaced_by))
        
        win_FPS = Ui_MainWindow(lines,self.To_Replace,self.Replaced_by,self.input_file)
        win_FPS.show()

    

appFPS_Window = QApplication.instance()
if appFPS_Window == None:
    appFPS_Window = QApplication(sys.argv)



if importes_pyside2 == True:
    print(" Pyside2")
    fps_window = Maya_Set_FPS()    
    appFPS_Window.exec_()
    fps_window.setFocus()
    fps_window.show()


else:
    # appFPS_Window = QApplication.instance()
    print("Not Pyside2")
    fps_window = Maya_Set_FPS()    
    appFPS_Window.exec_()
    fps_window.setFocus()
    fps_window.show()
    
    fps_window.closed.connect(lambda:fps_window.Open_Maya_File())
    fps_window.closed.connect(lambda:fps_window.Write_Maya())
    
    appFPS_Window.exec()
    