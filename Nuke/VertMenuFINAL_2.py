import sys
import time
start_time = time.time()

from PyQt5 import QtCore, QtGui, QtWidgets,uic
from PyQt5.QtCore import QSize, Qt,QItemSelectionModel,QEvent
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton,QTableWidget,QStyledItemDelegate,QComboBox,QTableWidgetItem
from PyQt5.QtGui import QMouseEvent,QFontDatabase

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True) #enable highdpi scaling
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True) #use highdpi icons


class NavigationWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(NavigationWidget,self).__init__(parent)


        
        # add your buttons
        #layout.addWidget(QtWidgets.QPushButton('Save'))
        #layout.addWidget(QtWidgets.QPushButton('Edit'))
        #layout.addWidget(QtWidgets.QPushButton('Delete'))
        
        self.JPG_Button = QtWidgets.QPushButton()
        self.JPG_Button.setGeometry(QtCore.QRect(1210, 280, 55, 31))
        
        self.JPG_Button.setObjectName("JPG_Button")
        self.ThreeD_Button = QtWidgets.QPushButton()
        self.ThreeD_Button.setGeometry(QtCore.QRect(1280, 280, 55, 31))
        
        self.ThreeD_Button.setObjectName("ThreeD_Button")
        self.Render_Button_3 = QtWidgets.QPushButton()
        self.Render_Button_3.setGeometry(QtCore.QRect(1350, 280, 55, 31))
        
        
        self.Render_Button_3.setObjectName("Render_Button_3")
        self.JPG_Button.setText("JPG")
        self.ThreeD_Button.setText("3D")
        self.Render_Button_3.setText("Render")

        self.JPG_Button.setStyleSheet("QPushButton#JPG_Button\n"
"{\n"
"    background-color: rgb(18, 192, 240);\n"
"    background-color: rgb(114, 184, 92);\n"
"    background-color: qlineargradient(spread:pad, x1:0.153045, y1:0.176, x2:0.676, y2:1, stop:0 rgba(27, 115, 27, 212), stop:1 rgba(255, 255, 255, 255));\n"
"    border-radius:12px;\n"
"}")
        self.ThreeD_Button.setStyleSheet("QPushButton#ThreeD_Button\n"
"{\n"
"    background-color: rgb(18, 192, 240);\n"
"    background-color: qlineargradient(spread:pad, x1:0.153045, y1:0.176, x2:0.676, y2:1, stop:0 rgba(255, 161, 29, 212), stop:1 rgba(255, 255, 255, 255));\n"
"    color:rgba(0, 0, 0, 210);\n"
"    border-radius:12px;\n"
"}")

        self.Render_Button_3.setStyleSheet("QPushButton#Render_Button_3\n"
"{\n"
"    background-color: qlineargradient(spread:pad, x1:0.153045, y1:0.176, x2:0.676, y2:1, stop:0 rgba(0, 153, 171, 212), stop:1 rgba(255, 255, 255, 255));\n"
"    color:rgba(0, 0, 0, 210);\n"
"    border-radius:12px;\n"
"}")

        self.JPG_Button.setFont(QtGui.QFont(NavigationFont_families[0], 9))
        self.ThreeD_Button.setFont(QtGui.QFont(NavigationFont_families[0], 9))
        self.Render_Button_3.setFont(QtGui.QFont(NavigationFont_families[0], 9))


        window.AddShot.setFont(QtGui.QFont(EternalFont_families[0], 12))
        window.CreateSyntheyesFile.setFont(QtGui.QFont(EternalFont_families[0], 10))
        window.ProjectStatus.setFont(QtGui.QFont(EternalFont_families[0], 12))
        window.Achievements.setFont(QtGui.QFont(EternalFont_families[0], 12))

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
     #   sizePolicy.setHeightForWidth(messageformForm.sizePolicy().hasHeightForWidth())
        
        
        # add your buttons
        layout = QtWidgets.QHBoxLayout()

        # adjust spacings to your needs
        layout.setContentsMargins(5,5,5,5)
        layout.setSpacing(4)

        self.Button_Width = 55
        self.Button_Height= 31
        
    #    self.JPG_Button.setFixedWidth(self.Button_Width)
    #    self.JPG_Button.setFixedHeight(self.Button_Height)
        self.JPG_Button.setSizePolicy(sizePolicy)
        self.ThreeD_Button.setSizePolicy(sizePolicy)
        self.Render_Button_3.setSizePolicy(sizePolicy)


        layout.addWidget(self.JPG_Button,stretch = 0)
        layout.addWidget(self.ThreeD_Button,stretch = 0)
        layout.addWidget(self.Render_Button_3,stretch = 0)

        self.setLayout(layout)




class StyleSheets():

    def __init__(self,Status):
        self.Colors = {
        "Initializing ...":"#E4DD83",
        "Not Started":"#B9B79F",
        "Track":"#41CB35",
        "Track Approval":"#267935",
        "For Solving":"#1F7968",
        "Solve":"#30D8E2",
        "For GeoBuild":"#e0cc78",               # #2596be    "#E2A730"
        "GeoBuild":"#c18d4b",                   #"#E28E30"
        "For Rotomation":"#F3DE6C",
        "Rotomation":"#F38D6C",
        "Waiting Assets":"#9A4C4F",
        "For Packing":"#4bc1b2",
        "Packing":"#4B8DC1",
        "Preview":"#72E476",
        "Ready":"#B272E4",
        "For Delivery":"#93A9EC",
        "Delivered":"#6258bf",
        "Approved":"#b258bf",
        "Cancelled":"#EF5454",
        "On Hold":"#625151",
        "Got Issue":"#620101",

        }
        self.Status = Status
        for key,value in self.Colors.items():
            print (f"self.Status = {self.Status},key = {key}, value={value}")
            if key == self.Status:
                self.StatusColor = value
                break


        self.StyleSheet = ("QComboBox\n"
    "{\n"
    "    subcontrol-origin: padding;\n"
    "    subcontrol-position: top right;\n"
    "    selection-background-color: #111;\n"
    "    selection-color: yellow;\n"
    "    color: black;\n"
    "    font: 10pt 'Candara';\n"
    "    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);\n"
    "    border-style: solid;\n"
    "    border: 1px solid #1e1e1e;\n"
    "    border-radius: 5;\n"
    "    padding: 1px 0px 1px 20px;\n"
    "}\n"
    "\n"
    "\n"
    "QComboBox:hover, QPushButton:hover\n"
    "{\n"
    "    border: 1px solid yellow;\n"
    "    color: black;\n"
    "}\n"
    "\n"
    "QComboBox:editable {\n"
    "    background: red;\n"
    "    color: pink;\n"
    "}\n"
    "\n"
    "QComboBox:on\n"
    "{\n"
    "    padding-top: 0px;\n"
    "    color: black;\n"
    "    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);\n"
    "    selection-background-color: #ffaa00;\n"
    "}\n"
    "\n"
    "QComboBox:!on\n"
    "{\n"
    "    color: black;\n"
    f"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #666, stop: 0.1 {value}, stop: 0.7 {value}, stop: 0.9 #444, stop: 1 #333);\n"
    "}\n"
    "\n"
    "QComboBox QAbstractItemView\n"
    "{\n"
    "    border: 2px solid darkgray;\n"
    "    color: black;\n"
    "    selection-background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #111, stop: 1 #333);\n"
    "}\n"
    "\n"
    "QComboBox::drop-down\n"
    "{\n"
    "     subcontrol-origin: padding;\n"
    "     subcontrol-position: top right;\n"
    "     width: 15px;\n"
    "     color: black;\n"
    "     border-left-width: 0px;\n"
    "     border-left-color: darkgray;\n"
    "     border-left-style: solid; /* just a single line */\n"
    "     border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
    "     border-bottom-right-radius: 3px;\n"
    "     padding-left: 10px;\n"
    " }\n"
    "\n"
    "QComboBox::down-arrow, QSpinBox::down-arrow, QTimeEdit::down-arrow, QDateEdit::down-arrow\n"
    "{\n"
    "     image: url(:/icons/down_arrow.png);\n"
    "     width: 7px;\n"
    "     height: 5px;\n"
    "}"
    "QListView::item {\n"
    "   height: 30px;\n"
    "}"

    )



class ColumnDelegate(QStyledItemDelegate):

    def createEditor(self, parent, option, index):
        if index.column() != 7 or index.column() !=8:
            return

    def initStyleOption(self, option, index):
        super(ColumnDelegate, self).initStyleOption(option, index)
        color = QtGui.QColor("#FFFFFF")
        #!!!!!!!!!!!!!! ORIGINAL COLOR = color: rgb(17, 160, 255);
        if index.column() == 0:
            color = QtGui.QColor(247,238,238)        # White
        elif index.column() == 1:
            #color = QtGui.QColor("#34ebc6")
            color = QtGui.QColor(255, 181, 62)      # Orange
        elif index.column() == 2:
            color = QtGui.QColor(255, 181, 62)      # Orange
        elif index.column() == 3:
            color = QtGui.QColor(17, 160, 255)

        if option.state & QtWidgets.QStyle.State_Selected:
            option.palette.setBrush(QtGui.QPalette.HighlightedText, QtGui.QBrush(QtGui.QColor(17, 160, 255)))
        else:
        #    option.palette.setColor(cg, QtGui.QPalette.Text, color)
            option.palette.setBrush(QtGui.QPalette.Text, QtGui.QBrush(QtGui.QColor(color)))
    def paint(self, painter, option, index):
        if option.state & QtWidgets.QStyle.State_Selected: # highligh background if selected
        #    painter.fillRect(option.rect, option.palette.highlight())           
            painter.save()
            painter.fillRect(option.rect, QtGui.QBrush(QtGui.QColor(30, 66, 109))) # Initializing ...
            painter.restore()

        QtWidgets.QStyledItemDelegate.paint(self, painter, option, index)

class WriteDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        QtWidgets.QStyledItemDelegate.__init__(self, parent=parent)
        QtWidgets.qApp.installEventFilter(self)

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            if event.oldState() and Qt.WindowMinimized:
                print("WindowMinimized")
            elif event.oldState() == Qt.WindowNoState or self.windowState() == Qt.WindowMaximized:
                print("WindowMaximized")

    def createEditor(self, parent, option, index):
        editor = super().createEditor(parent, option, index)

        return editor

    def initStyleOption(self, option, index):
        super(WriteDelegate, self).initStyleOption(option, index)
        color = QtGui.QColor("#FFFFFF")
        if index.column() == 7:
            color = QtGui.QColor(247,238,238)    
        elif index.column() == 8:
            color = QtGui.QColor(247,238,238)    
        elif index.column() == 10:
            color = QtGui.QColor(52,252,255)  

        if option.state & QtWidgets.QStyle.State_Selected:
            option.palette.setBrush(QtGui.QPalette.HighlightedText, QtGui.QBrush(QtGui.QColor(17, 160, 255)))
        #    option.palette.setBrush(QtGui.QPalette.Highlight,(QtGui.QColor(228, 221, 131)))
        else:
        #    option.palette.setColor(cg, QtGui.QPalette.Text, color)
            option.palette.setBrush(QtGui.QPalette.Text, QtGui.QBrush(QtGui.QColor(color)))

    def paint(self, painter, option, index):
        if option.state & QtWidgets.QStyle.State_Selected: # highligh background if selected
        #    painter.fillRect(option.rect, option.palette.highlight())           
            painter.save()
            painter.fillRect(option.rect, QtGui.QBrush(QtGui.QColor(30, 66, 109))) # Initializing ...
            painter.restore()

        QtWidgets.QStyledItemDelegate.paint(self, painter, option, index)

    


    def eventFilter(self, source, event):
        if ((source is window.ShotTable and
            event.type() == QtCore.QEvent.KeyPress and
            event.key() in (
                QtCore.Qt.Key.Key_Down,
                QtCore.Qt.Key.Key_Up,
            ) and
            event.modifiers() == Qt.NoModifier)):
            return True
        return super().eventFilter(source, event)

#        elif event.type() == QtCore.QEvent.KeyPress:
#            if event.key() in (
#                QtCore.Qt.Key.Key_Down,
#                QtCore.Qt.Key.Key_Up,
#            ):
#                print("DOWN WAS PRESSED")
#                return True
#        return super().eventFilter(source, event)


class FontDelegate(QStyledItemDelegate):
    def createEditor(self, parent, opt, index):
        editor = super().createEditor(parent, opt, index)
        font = index.data(Qt.FontRole)
        if font is not None:
            editor.setFont(font)
        return editor

class MyQComboBox(QtWidgets.QComboBox):
    def __init__(self, scrollWidget=None, *args, **kwargs):
        super(MyQComboBox, self).__init__(*args, **kwargs)  
        self.scrollWidget=scrollWidget
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

    def wheelEvent(self, *args, **kwargs):
        return
#        if self.hasFocus():
#            return QtWidgets.QComboBox.wheelEvent(self, *args, **kwargs)
#        else:
#            return self.scrollWidget.wheelEvent(*args, **kwargs)

class StatusItemDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent=None):
        QtWidgets.QStyledItemDelegate.__init__(self, parent=parent)

    

    def paint(self, painter, option, index):
        if index.row() == 0 :
            if option.state & QtWidgets.QStyle.State_Selected: # highligh background if selected
                painter.fillRect(option.rect, option.palette.highlight())           
            painter.save()
            painter.fillRect(option.rect, QtGui.QBrush(QtGui.QColor(228, 221, 131))) # Initializing ...
            painter.restore()
        elif index.row() == 1 :
            painter.save()
            painter.fillRect(option.rect, QtGui.QBrush(QtGui.QColor(185, 183, 159))) # Not Started
            painter.restore()
        elif index.row() == 2 :
            painter.save()
            painter.fillRect(option.rect, QtGui.QBrush(QtGui.QColor(65, 203, 53))) # Track
            painter.restore()
        elif index.row() == 3 :
            painter.save()
            painter.fillRect(option.rect, QtGui.QBrush(QtGui.QColor(38, 121, 31))) # Track Apporval
            painter.restore()
        elif index.row() == 4 :
            painter.save()
            painter.fillRect(option.rect, QtGui.QBrush(QtGui.QColor(31, 121, 104))) # For Solve
            painter.restore()
        elif index.row() == 5 :
            painter.save()
            painter.fillRect(option.rect, QtGui.QBrush(QtGui.QColor(48, 216, 226))) # Solve
            painter.restore()
        elif index.row() == 6 :
            painter.save()
            painter.fillRect(option.rect, QtGui.QBrush(QtGui.QColor("#e0cc78"))) # For GeoBuild
            painter.restore()
        elif index.row() == 7 :
            painter.save()
            #painter.fillRect(option.rect, QtGui.QBrush(QtGui.QColor(226, 142, 48))) # GeoBuild 
            painter.fillRect(option.rect, QtGui.QBrush(QtGui.QColor("#c18d4b")))
            painter.restore()
        elif index.row() == 8 :
            painter.save()
            painter.fillRect(option.rect, QtGui.QBrush(QtGui.QColor(243, 222, 108))) # For Rotomation
            painter.restore()
        elif index.row() == 9 :
            painter.save()
            painter.fillRect(option.rect, QtGui.QBrush(QtGui.QColor(243, 141, 108))) # Rotomation
            painter.restore()
        elif index.row() == 10 :
            painter.save()
            painter.fillRect(option.rect, QtGui.QBrush(QtGui.QColor(154, 76, 79))) # Waiting Assets
            painter.restore()
        elif index.row() == 11 :
            painter.save()
            painter.fillRect(option.rect, QtGui.QBrush(QtGui.QColor("#4bc1b2"))) # For Packing
            painter.restore()
        elif index.row() == 12 :
            painter.save()
            painter.fillRect(option.rect, QtGui.QBrush(QtGui.QColor("#4B8DC1"))) # Packing
            painter.restore()
        elif index.row() == 13 :
            painter.save()
            painter.fillRect(option.rect, QtGui.QBrush(QtGui.QColor(114, 228, 118))) # Preview
            painter.restore()
        elif index.row() == 14 :
            painter.save()
            painter.fillRect(option.rect, QtGui.QBrush(QtGui.QColor(178, 114, 228))) # Ready
            painter.restore()
        elif index.row() == 15 :
            painter.save()
            painter.fillRect(option.rect, QtGui.QBrush(QtGui.QColor(147, 169, 236))) # For Delivery
            painter.restore()
        elif index.row() == 16 :
            painter.save()
            painter.fillRect(option.rect, QtGui.QBrush(QtGui.QColor("#6258bf"))) # Delivered
            painter.restore()
        elif index.row() == 17 :
            painter.save()
            painter.fillRect(option.rect, QtGui.QBrush(QtGui.QColor("#b258bf"))) # Approved
            painter.restore()
        elif index.row() == 18 :
            painter.save()
            painter.fillRect(option.rect, QtGui.QBrush(QtGui.QColor(239, 84, 84))) # Cancelled
            painter.restore()
        elif index.row() == 19 :
            painter.save()
            painter.fillRect(option.rect, QtGui.QBrush(QtGui.QColor(98, 81, 81))) # On Hold
            painter.restore()
        elif index.row() == 20 :
            painter.save()
            painter.fillRect(option.rect, QtGui.QBrush(QtGui.QColor(98, 1, 1))) # Got Issue
            painter.restore()
        QtWidgets.QStyledItemDelegate.paint(self, painter, option, index)


class ReadOnlyDelegate(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        return
    
    def paint(self, painter, option, index): 

        if index.column() == 1:
#            if option.state & QtWidgets.QStyle.State_Selected: # highligh background if selected
#                painter.fillRect(option.rect, option.palette.highlight())           
            painter.save()
#            painter.fillRect(option.rect, QtGui.QBrush(QtGui.QColor(228, 221, 131))) # Initializing ...
            painter.restore()
        #    painter.setPen(QtGui.QPen(QtGui.QColor("#FF0000")))
            if option.state & QtWidgets.QStyle.State_Selected:
                painter.setPen(QtGui.QPen(QtCore.Qt.red))
            else:
                painter.setPen(QtGui.QPen(QtCore.Qt.white))
        #    return QtGui.QBrush(QtCore.Qt.red)
#        else:
#            return QtGui.QBrush(QtCore.Qt.black)
        painter.save()
        if option.state & QtWidgets.QStyle.State_Selected:
            painter.setPen(QtGui.QPen(QtCore.Qt.red))
        else:
            painter.setPen(QtGui.QPen(QtCore.Qt.white))
        value = index.data(QtCore.Qt.DisplayRole)
    #    if value.isValid():
        text = value
#        painter.drawText(option.rect, QtCore.Qt.AlignLeft | QtCore.Qt.AlignCenter, text)
        
        painter.restore()
        QtWidgets.QStyledItemDelegate.paint(self, painter, option, index)

qtCreatorFile = "C:/Users/Damjan/Desktop/VertigoCentral_2.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class Table(QtWidgets.QTableWidget):
    def __init__(self):
        super(Table, self).__init__()

#        self.setupUi(self)
        self.Ui_MainWindow=uic.loadUi('VertigoCentral_2.ui', self)

class MainWindow(QMainWindow, Ui_MainWindow):
    signal = QtCore.pyqtSignal()
    signal_up = QtCore.pyqtSignal()
    signal_down = QtCore.pyqtSignal()
    def __init__(self):
        super(MainWindow, self).__init__()
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.Ui_MainWindow=uic.loadUi('VertigoCentral_2.ui', self)
        self.show()
        self.TYPE = ("UV","LD")
        self.STATUS = ("Initializing ...","Not Started","Track","Track Approval",
        "For Solving", "Solve", "For GeoBuild", "GeoBuild", "For Rotomation",
        "Rotomation","Waiting Assets",
        "For Packing", "Packing","Preview","Ready",
        "For Delivery","Delivered","Approved",
        "Cancelled","On Hold","Got Issue!")
        QtWidgets.qApp.installEventFilter(self)
        self.row = 0
#        self.setChildrenFocusPolicy(QtCore.Qt.NoFocus)
#        self.model.rowsInserted.connect(lambda: QtCore.QTimer.singleShot(0, self.view.scrollToBottom))
        
    def eventFilter(self, source, event):
        
        return super().eventFilter(source, event)

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            if event.oldState() and Qt.WindowMinimized:
                print("WindowMinimized")
            #    window.task4LineEdit.setFocus()
                window.ShotTable.clearFocus()
            elif event.oldState() == Qt.WindowNoState or self.windowState() == Qt.WindowMaximized:
                print("WindowMaximized")
            #    window.task4LineEdit.setFocus()
                window.ShotTable.clearFocus()

    def setChildrenFocusPolicy (self, policy):
        def recursiveSetChildFocusPolicy (parentQWidget):
            for childQWidget in parentQWidget.findChildren(QtWidgets.QWidget):
                childQWidget.setFocusPolicy(policy)
                recursiveSetChildFocusPolicy(childQWidget)
        recursiveSetChildFocusPolicy(self)

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.KeyPress:
            print(event.key())
            self.row = window.ShotTable.currentRow()
            print('self.row={}'.format(self.row))

        if ((source is window.ShotTable and
             event.type() == QtCore.QEvent.KeyPress and
             event.key() == Qt.Key_Escape and
             event.modifiers() == Qt.NoModifier) or
            (source is window.ShotTable.viewport() and
             event.type() == QtCore.QEvent.MouseButtonPress and
             not window.ShotTable.indexAt(event.pos()).isValid())):
            window.ShotTable.selectionModel().clear()
            Status.clearFocus()
            print("CLEARED")
        
        
        
        return super(MainWindow, self).eventFilter(source, event)
    
    @QtCore.pyqtSlot()
    def arrowkey(self,num):
    #    try:
        selection_model = window.ShotTable.selectionModel()
        indexes = selection_model.selectedIndexes()
        if indexes:
            muh = self.row
#            muh = indexes[0].row()
        else:
            muh = 0
        window.ShotTable.clearSelection()
        if num == 1:
            window.ShotTable.selectRow(muh -1)
        else:
            window.ShotTable.selectRow(muh + 1)

    #    except UnboundLocalError:
    #        pass


    def keyPressEvent (self, event):
        key = event.key()
        indexes = self.row
        

        if event.key() == QtCore.Qt.Key_Up:
            if indexes:
                index = indexes

        #    window.ShotTable.selectionModel().select(index, QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Rows)
            window.ShotTable.selectRow(indexes - 1)
        elif event.key() == QtCore.Qt.Key_Down:
            if indexes:
                index = indexes

           # window.ShotTable.selectionModel().select(index, QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Rows)

            window.ShotTable.selectRow(indexes + 1)
        elif key == QtCore.Qt.Key_F1:
            print ('Help')
        elif key == QtCore.Qt.Key_F5:
            print ('Reload')
        elif key == QtCore.Qt.Key_Left:
            print ('Left')
    #    elif key == QtCore.Qt.Key_Up:
    #        print ('Up')
        elif key == QtCore.Qt.Key_Right:
            print ('Right')
    #    elif key == QtCore.Qt.Key_Down:
    #        print ('Down')
    #    messageQMessageBox = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Question, 'Question', 'Hello Main', QtWidgets.QMessageBox.Yes)
    #    messageQMessageBox.exec_()
        QtWidgets.QWidget.keyPressEvent(self, event)

app = QApplication(sys.argv)

NavigationFont_ID = QFontDatabase.addApplicationFont(r"C:\Users\Damjan\Desktop\fonts\MonoBold.ttf")
EternalFont_ID = QFontDatabase.addApplicationFont(r"C:\Users\Damjan\Desktop\fonts\EternalUiBold.ttf")


#Opkrop_ID = QFontDatabase.addApplicationFont(r"C:C:\Users\Damjan\Desktop\fonts\Opkrop.otf")

if (EternalFont_ID<0):
    print("ERRA")
else:
    print("NO ERRA")

	
NavigationFont_families = QFontDatabase.applicationFontFamilies(NavigationFont_ID)
EternalFont_families = QFontDatabase.applicationFontFamilies(EternalFont_ID)
#Opkrop_Font_families = QFontDatabase.applicationFontFamilies(Opkrop_ID)


window = MainWindow()
window.setFixedSize(1920, 1080)
window.ShotTable.setAutoScroll(True)
#window.ShotTable.setAutoScrollMargin(20)
# create an cell widget
btn = QPushButton(window.Ui_MainWindow.ShotTable)
btn.setText('12/1/12')


#currentRowCount = window.ShotTable.rowCount() #necessary even when there are no rows in the table
#for rau in range(0,400):
#    window.ShotTable.insertRow(currentRowCount)

# Preview Image
imagePath = r"\\fs3\TPN\Tippett\JAM_RTR\input\Vertigo_Tippett_JAM_20221222\rtr_1450\plates\bg\original01\v001\jpg\rtr_1450_bg_original01_v001_aces.977.jpg"
imagePath = imagePath.replace("\\","/")
print(imagePath)
window.Ui_MainWindow.PreviewImage.setPixmap(QtGui.QPixmap(imagePath))
#
#window.ShotTable.setCellWidget(0, 0, btn)
QTableWidget.contextMenuEvent

window.ShotTable.horizontalHeader().setDefaultAlignment(Qt.AlignLeft|Qt.AlignVCenter)

#window.ShotTable.setFont(QtGui.QFont('Seroe UI', 9,40))

def setColortoRow(table, rowIndex, r,g,b):
    for j in range(table.columnCount()):
        table.item(rowIndex, j).setBackground(QtGui.QColor(r,g,b))

for i in range(1):
    print ("i = {}".format(i))
    print ("FirstFrame = {}".format(window.ShotTable.item(i, 3)))
    #window.ShotTable.item(i, 3).setBackground(QtGui.QColor(100,100,150))
 #   window.ShotTable.item(1,0).setBackground(QtGui.QColor(152,129,0))

#setColortoRow(window.ShotTable,2,120,120,120)

Read_Only_Delegate = ReadOnlyDelegate(window.ShotTable)
#window.ShotTable.setItemDelegateForRow(1, Read_Only_Delegate)
window.ShotTable.setItemDelegateForColumn(0, Read_Only_Delegate)
window.ShotTable.setItemDelegateForColumn(1, Read_Only_Delegate)
window.ShotTable.setItemDelegateForColumn(2, Read_Only_Delegate)
window.ShotTable.setItemDelegateForColumn(3, Read_Only_Delegate)
window.ShotTable.setItemDelegateForColumn(4, Read_Only_Delegate)
window.ShotTable.setItemDelegateForColumn(5, Read_Only_Delegate)
window.ShotTable.setItemDelegateForColumn(6, Read_Only_Delegate)
window.ShotTable.setItemDelegateForColumn(9, Read_Only_Delegate)
window.ShotTable.setItemDelegateForColumn(10, Read_Only_Delegate)
window.ShotTable.setItemDelegateForColumn(11, Read_Only_Delegate)

try:
    for n in range(5):
        window.ShotTable.setRowHeight(n,36)
except:
    pass
window.ShotTable.setColumnWidth(0, 40)  # id
window.ShotTable.setColumnWidth(1, 120) # Studio
window.ShotTable.setColumnWidth(2, 100) # Project
window.ShotTable.setColumnWidth(3, 310) # Shot
window.ShotTable.setColumnWidth(4, 40)  # Type
window.ShotTable.setColumnWidth(5, 140) # Status
window.ShotTable.setColumnWidth(6, 130) # FrameRange
window.ShotTable.setColumnWidth(7, 60)  # SG_Lens
window.ShotTable.setColumnWidth(8, 110) # Backplate
window.ShotTable.setColumnWidth(9, 180) # Navigation
window.ShotTable.setColumnWidth(10, 150) # Download/Upload
window.ShotTable.setColumnWidth(11, 90) # Version
window.ShotTable.setColumnWidth(12, 350) # Scripts

window.ShotTable.horizontalHeader().setSectionResizeMode(2) # Fixed

ShotType= QtWidgets.QComboBox(window.Ui_MainWindow.centralwidget)
for index,it in enumerate(window.TYPE):
    ShotType.addItem("")
    ShotType.setItemText(index, it)

def index_changed_id_by_combobox(combobox: QComboBox, selected_index: int) -> None:

    print(f"Combobox: {combobox.objectName()}, changed to index:{selected_index}")
    print(f"Combobox_Current_Status: {combobox.currentText()}, changed to index:{selected_index}")
    StatusResult = combobox.currentText()
    StatusStylesheet = StyleSheets(StatusResult)
    combobox.setStyleSheet(StatusStylesheet.StyleSheet)
    combobox.clearFocus()
    if combobox.currentText() == "Delivered":
        print("DELIVERED")

def index_combobox_activated(combobox: QComboBox, selected_index: int) -> None:
    combobox.clearFocus()
    print("ACTIF")

def index_combobox_highlighted(combobox: QComboBox, selected_index: int) -> None:
    combobox.clearFocus()
    print("HIGHLIGHT")

def pass_Net_Adap(self):
    StatusResult = Status.currentText()
  #  StatusResult = window.ShotTable.item(1,5).currentText()
    print ("StatusResult = {}".format(StatusResult))


def Selected_Row():
    if window.ShotTable.selectedIndexes():
        for index in sorted(window.ShotTable.selectionModel().selectedRows()):
            row = index.row()
            id = window.ShotTable.model().data(window.ShotTable.model().index(row, 0))
            StudioName =    window.ShotTable.model().data(window.ShotTable.model().index(row, 1))
            ProjectName =   window.ShotTable.model().data(window.ShotTable.model().index(row, 2))
            ShotName =      window.ShotTable.model().data(window.ShotTable.model().index(row, 3))
            Type =          window.ShotTable.model().data(window.ShotTable.model().index(row, 4))
            Status =        window.ShotTable.model().data(window.ShotTable.model().index(row, 5))
            FrameRange =    window.ShotTable.model().data(window.ShotTable.model().index(row, 6))
            SGLens =        window.ShotTable.model().data(window.ShotTable.model().index(row, 7))
            BackPlate =     window.ShotTable.model().data(window.ShotTable.model().index(row, 8))
            Down_Upload =   window.ShotTable.model().data(window.ShotTable.model().index(row, 10))
            Version =       window.ShotTable.model().data(window.ShotTable.model().index(row, 11))
        print("selected_indexes = {}".format(window.ShotTable.selectedIndexes()))
        print ("id = {}".format(id))
        print ("StudioName = {}".format(StudioName))
        print ("ProjectName = {}".format(ProjectName))
        print ("ShotName = {}".format(ShotName))
        print ("Type = {}".format(Type))
        print ("Status = {}".format(Status))
        print ("FrameRange = {}".format(FrameRange))
        print ("SGLens = {}".format(SGLens))
        print ("BackPlate = {}".format(BackPlate))
        print ("Down_Upload = {}".format(Down_Upload))
        print ("Version = {}".format(Version))
        print ("--------------------------------")
    else:
        print("Nothing")




#Status= QtWidgets.QComboBox()
StatusCount = 0
for row in range(window.ShotTable.rowCount()):
    StatusCount += 1
    window.ShotTable.setRowHeight(row,36)
    scrollArea = QtWidgets.QScrollArea()
    frmScroll = QtWidgets.QFrame(scrollArea)
    cmbOption = MyQComboBox(frmScroll)
    Status = cmbOption
#    Status.setObjectName("Status")
    Status.setObjectName(f"Status_{StatusCount}")
    for index,it in enumerate(window.STATUS):
        Status.addItem("")
        Status.setItemText(index, it)
    #Status.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
    Status.setStyleSheet("QComboBox\n"
    "{\n"
    "    subcontrol-origin: padding;\n"
    "    subcontrol-position: top right;\n"
    "    selection-background-color: #111;\n"
    "    selection-color: yellow;\n"
    "    color: white;\n"
    "    font: 10pt 'Candara';\n"
    "    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);\n"
    "    border-style: solid;\n"
    "    border: 1px solid #1e1e1e;\n"
    "    border-radius: 5;\n"
    "    padding: 1px 0px 1px 20px;\n"
    "}\n"
    "\n"
    "\n"
    "QComboBox:hover, QPushButton:hover\n"
    "{\n"
    "    border: 1px solid yellow;\n"
    "    color: white;\n"
    "}\n"
    "\n"
    "QComboBox:editable {\n"
    "    background: red;\n"
    "    color: pink;\n"
    "}\n"
    "\n"
    "QComboBox:on\n"
    "{\n"
    "    padding-top: 0px;\n"
    "    color: white;\n"
    "    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);\n"
    "    selection-background-color: #ffaa00;\n"
    "}\n"
    "\n"
    "QComboBox:!on\n"
    "{\n"
    "    color: white;\n"
    "    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #666, stop: 0.1 #555, stop: 0.5 #555, stop: 0.9 #444, stop: 1 #333);\n"
    "}\n"
    "\n"
    "QComboBox QAbstractItemView\n"
    "{\n"
    "    border: 2px solid darkgray;\n"
    "    color: black;\n"
    "    selection-background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #111, stop: 1 #333);\n"
    "}\n"
    "\n"
    "QComboBox::drop-down\n"
    "{\n"
    "     subcontrol-origin: padding;\n"
    "     subcontrol-position: top right;\n"
    "     width: 15px;\n"
    "     color: white;\n"
    "     border-left-width: 0px;\n"
    "     border-left-color: darkgray;\n"
    "     border-left-style: solid; /* just a single line */\n"
    "     border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
    "     border-bottom-right-radius: 3px;\n"
    "     padding-left: 10px;\n"
    " }\n"
    "\n"
    "QComboBox::down-arrow, QSpinBox::down-arrow, QTimeEdit::down-arrow, QDateEdit::down-arrow\n"
    "{\n"
    "     image: url(:/icons/down_arrow.png);\n"
    "     width: 7px;\n"
    "     height: 5px;\n"
    "}"
    "QListView::item {\n"
    "   height: 30px;\n"
    "}"

    )


    Status.currentIndexChanged.connect(
        lambda selected_index, combobox=Status: index_changed_id_by_combobox(combobox, selected_index))
    Status.activated.connect(
        lambda selected_index, combobox=Status: index_combobox_activated(combobox, selected_index))
    Status.highlighted.connect(
        lambda selected_index, combobox=Status: index_combobox_highlighted(combobox, selected_index))
    Status.setItemDelegate(StatusItemDelegate())
    window.ShotTable.setCellWidget(row, 5, Status)
    window.ShotTable.setCellWidget(row,9, NavigationWidget())
    view = Status.view()
    view.setFixedHeight(570)
    window.ShotTable.selectionModel().clear()
    Status.clearFocus()
#    Status.activated.connect(pass_Net_Adap)
#    Status.activated.connect(Selected_Row)
    
ShotType.setItemText(0, "UV")
ShotType.setItemText(1, "LD")

window.ShotTable.setSelectionBehavior(window.ShotTable.SelectRows)
window.ShotTable.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
window.ShotTable.itemClicked.emit(window.ShotTable.item(0, 0))

window.ShotTable.ScrollHint(QtWidgets.QAbstractItemView.EnsureVisible)




window.ShotTable.setCellWidget(0, 4, ShotType)
#window.ShotTable.setCellWidget(0, 5, Status)
#window.ShotTable.setCellWidget(6, 5, cmbOption)

#Status.resize(Status.sizeHint())

#window.ShotTable.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
#window.ShotTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectColumns)
window.ShotTable.setFocusPolicy(Qt.NoFocus)

#window.PreviewImage.setStyleSheet("border: 3px solid blue;")
#window.ShotTable.setItemDelegate(FontDelegate(window.ShotTable))
Column_Delegate = ColumnDelegate(window.ShotTable)
Write_Delegate = WriteDelegate(window.ShotTable)
window.ShotTable.setItemDelegateForColumn(0,Column_Delegate)
window.ShotTable.setItemDelegateForColumn(1,Column_Delegate)
window.ShotTable.setItemDelegateForColumn(2,Column_Delegate)
window.ShotTable.setItemDelegateForColumn(3,Column_Delegate)
window.ShotTable.setItemDelegateForColumn(6,Column_Delegate)
window.ShotTable.setItemDelegateForColumn(7,Write_Delegate)
window.ShotTable.setItemDelegateForColumn(8,Write_Delegate)
window.ShotTable.setItemDelegateForColumn(10,Write_Delegate)
window.ShotTable.setItemDelegateForColumn(11,Write_Delegate)

#window.task1LineEdit.resize(200,62)
#window.ProjectInfoText.setPlainText("VERTIGO TEST RUN")
window.ProjectInfoText.setPlaceholderText("Project Info") 

def get_table_row_value():
    rows = set()
    for index in window.ShotTable.selectedIndexes():
        rows.add(index.row())
    for row in rows:
        ix = window.ShotTable.model().index(row, 0)
        print ("IndexValue = {}".format(ix.data()))
        CurrentRow = window.ShotTable.currentRow()
        print ("CurrentRow = {}".format(CurrentRow))

#window.ShotTable.cellClicked.connect(Selected_Row)
#window.ShotTable.currentCellChanged.connect(Selected_Row)
#window.ShotTable.itemSelectionChanged.connect(Selected_Row)
#window.ShotTable.selectionModel().selectionChanged.connect(get_table_row_value)
window.ShotTable.selectionModel().clear()
window.ShotTable.selectionModel().selectionChanged.connect(Selected_Row)
window.ShotTable.setSortingEnabled(True)

indexes = window.ShotTable.selectionModel().selectedIndexes()
if indexes:
    index = window.ShotTable.model().index(indexes[0].row() + 1, indexes[0].column())
else:
    index = window.ShotTable.model().index(0, 0)
window.ShotTable.selectionModel().select(index, QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Rows)

class CustomStyle(QtWidgets.QCommonStyle):
    def drawPrimitive(self, element, option, painter, widget):
        if element == QtWidgets.QStyle.PE_PanelItemViewItem:
            option.state = QtWidgets.QStyle.State_Selected
        super(CustomStyle, self).drawPrimitive(element, option, painter, widget)


window.setFocusPolicy(Qt.StrongFocus)

#window.ShotTable.setStyle(CustomStyle())
print("--- %s seconds ---" % (time.time() - start_time))
window.show()

app.exec()