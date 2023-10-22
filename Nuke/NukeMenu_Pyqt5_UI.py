import sys,os
import subprocess
sys.path.append(r"\\fs3\Sh1\uber\Nuke_Scripts")



from PyQt5.QtWidgets import (QApplication, QMainWindow,QPushButton,QLabel,QFrame,
QGroupBox,QComboBox,QRadioButton,QButtonGroup)

from PyQt5.QtGui import QFont,QIcon
from PyQt5.QtCore import Qt,QRect,QCoreApplication,QMetaObject
#from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Main(object):
    def setupUi(self, Main):
        Main.setObjectName("Main")
        Main.resize(349, 524)
        Main.setAutoFillBackground(False)
        Main.setStyleSheet("background-color:rgb(44, 44, 44)")
        self.Undist_Crop_Button = QPushButton(Main)
        self.Undist_Crop_Button.setGeometry(QRect(40, 20, 271, 61))
        self.Undist_Crop_Button.setStyleSheet("background-color:rgb(60, 53, 97)")
        self.Undist_Crop_Button.setObjectName("Undist_Crop_Button")
        self.Nuke_File_Button = QPushButton(Main)
        self.Nuke_File_Button.setGeometry(QRect(40, 90, 271, 61))
        self.Nuke_File_Button.setStyleSheet("background-color: rgb(122, 80, 31);")
        self.Nuke_File_Button.setObjectName("Nuke_File_Button")
        self.Preview_Button = QPushButton(Main)
        self.Preview_Button.setGeometry(QRect(40, 230, 271, 61))
        self.Preview_Button.setStyleSheet("\n"
"background-color:rgb(85, 170, 255)")
        self.Preview_Button.setObjectName("Preview_Button")
        self.Nuke_LD_to_UV_Button = QPushButton(Main)
        self.Nuke_LD_to_UV_Button.setGeometry(QRect(40, 160, 271, 61))
        self.Nuke_LD_to_UV_Button.setStyleSheet("background-color: rgb(53, 115, 43);")
        self.Nuke_LD_to_UV_Button.setObjectName("Nuke_LD_to_UV_Button")
        self.Preview_Image_Selection_Label = QLabel(Main)
        self.Preview_Image_Selection_Label.setGeometry(QRect(70, 300, 201, 21))
        font = QFont()
        font.setFamily("Lucida Sans Unicode")
        font.setPointSize(11)
        self.Preview_Image_Selection_Label.setFont(font)
        self.Preview_Image_Selection_Label.setStyleSheet("color: rgb(208, 208, 208);")
        self.Preview_Image_Selection_Label.setAlignment(Qt.AlignCenter)
        self.Preview_Image_Selection_Label.setObjectName("Preview_Image_Selection_Label")
        self.Shot_Type_Label = QLabel(Main)
        self.Shot_Type_Label.setGeometry(QRect(70, 370, 201, 21))
        font = QFont()
        font.setFamily("Lucida Sans Unicode")
        font.setPointSize(11)
        self.Shot_Type_Label.setFont(font)
        self.Shot_Type_Label.setStyleSheet("color: rgb(208, 208, 208);")
        self.Shot_Type_Label.setAlignment(Qt.AlignCenter)
        self.Shot_Type_Label.setObjectName("Shot_Type_Label")
        self.Preview_Image_Selection_Line = QFrame(Main)
        self.Preview_Image_Selection_Line.setGeometry(QRect(0, 320, 351, 16))
        self.Preview_Image_Selection_Line.setFrameShape(QFrame.HLine)
        self.Preview_Image_Selection_Line.setFrameShadow(QFrame.Sunken)
        self.Preview_Image_Selection_Line.setObjectName("Preview_Image_Selection_Line")
        self.Shot_Type_Line = QFrame(Main)
        self.Shot_Type_Line.setGeometry(QRect(0, 390, 351, 16))
        self.Shot_Type_Line.setFrameShape(QFrame.HLine)
        self.Shot_Type_Line.setFrameShadow(QFrame.Sunken)
        self.Shot_Type_Line.setObjectName("Shot_Type_Line")
        self.PIS_GroupBox = QGroupBox(Main)
        self.PIS_GroupBox.setGeometry(QRect(10, 320, 331, 41))
        self.PIS_GroupBox.setStyleSheet("QGroupBox{\n"
"    border:0px\n"
"}")
        self.PIS_GroupBox.setTitle("")
        self.PIS_GroupBox.setObjectName("PIS_GroupBox")
        self.Source_Button = QRadioButton(self.PIS_GroupBox)
        self.Source_Button.setEnabled(True)
        self.Source_Button.setGeometry(QRect(10, 20, 89, 20))
        self.Source_Button.setStyleSheet("color: rgb(74, 222, 222);")
        self.Source_Button.setChecked(True)
        self.Source_Button.setAutoRepeat(False)
        self.Source_Button.setObjectName("Source_Button")
        self.PIS_buttonGroup = QButtonGroup(Main)
        self.PIS_buttonGroup.setObjectName("PIS_buttonGroup")
        self.PIS_buttonGroup.addButton(self.Source_Button)
        self.Crop_Button = QRadioButton(self.PIS_GroupBox)
        self.Crop_Button.setEnabled(True)
        self.Crop_Button.setGeometry(QRect(220, 20, 89, 20))
        self.Crop_Button.setStyleSheet("color: rgb(103, 43, 255);")
        self.Crop_Button.setObjectName("Crop_Button")
        self.PIS_buttonGroup.addButton(self.Crop_Button)
        self.Undist_Button = QRadioButton(self.PIS_GroupBox)
        self.Undist_Button.setEnabled(True)
        self.Undist_Button.setGeometry(QRect(120, 20, 89, 20))
        self.Undist_Button.setStyleSheet("color: rgb(206, 77, 17);")
        self.Undist_Button.setObjectName("Undist_Button")
        self.PIS_buttonGroup.addButton(self.Undist_Button)
        self.ShotType_GroupBox = QGroupBox(Main)
        self.ShotType_GroupBox.setGeometry(QRect(10, 390, 331, 41))
        self.ShotType_GroupBox.setStyleSheet("QGroupBox{\n"
"    border:0px\n"
"}")
        self.ShotType_GroupBox.setTitle("")
        self.ShotType_GroupBox.setObjectName("ShotType_GroupBox")
        self.LD_Button = QRadioButton(self.ShotType_GroupBox)
        self.LD_Button.setEnabled(True)
        self.LD_Button.setGeometry(QRect(120, 20, 89, 20))
        self.LD_Button.setStyleSheet("color: rgb(103, 131, 255);")
        self.LD_Button.setObjectName("LD_Button")
        self.UV_LD_buttonGroup = QButtonGroup(Main)
        self.UV_LD_buttonGroup.setObjectName("UV_LD_buttonGroup")
        self.UV_LD_buttonGroup.addButton(self.LD_Button)
        self.UV_Button = QRadioButton(self.ShotType_GroupBox)
        self.UV_Button.setEnabled(True)
        self.UV_Button.setGeometry(QRect(10, 20, 89, 20))
        self.UV_Button.setStyleSheet("color: rgb(255, 158, 102);")
        self.UV_Button.setChecked(True)
        self.UV_Button.setAutoRepeat(False)
        self.UV_Button.setObjectName("UV_Button")
        self.UV_LD_buttonGroup.addButton(self.UV_Button)
        self.Shot_Type_Line_2 = QFrame(Main)
        self.Shot_Type_Line_2.setGeometry(QRect(0, 440, 351, 16))
        self.Shot_Type_Line_2.setFrameShape(QFrame.HLine)
        self.Shot_Type_Line_2.setFrameShadow(QFrame.Sunken)
        self.Shot_Type_Line_2.setObjectName("Shot_Type_Line_2")
        self.Version = QComboBox(Main)
        self.Version.setGeometry(QRect(120, 480, 101, 22))
        self.Version.setObjectName("Version")
        self.Version.addItem("")
        self.Version.addItem("")
        self.Version.addItem("")
        self.Version.addItem("")
        self.Version.addItem("")
        self.Version.addItem("")
        self.Version.addItem("")
        self.Version.addItem("")
        self.Version.addItem("")
        self.Version_Label = QLabel(Main)
        self.Version_Label.setGeometry(QRect(70, 450, 201, 21))
        font = QFont()
        font.setFamily("Lucida Sans Unicode")
        font.setPointSize(11)
        self.Version_Label.setFont(font)
        self.Version_Label.setStyleSheet("color: rgb(208, 208, 208);")
        self.Version_Label.setAlignment(Qt.AlignCenter)
        self.Version_Label.setObjectName("Version_Label")
        self.PIS_GroupBox.raise_()
        self.ShotType_GroupBox.raise_()
        self.Undist_Crop_Button.raise_()
        self.Nuke_File_Button.raise_()
        self.Preview_Button.raise_()
        self.Nuke_LD_to_UV_Button.raise_()
        self.Preview_Image_Selection_Label.raise_()
        self.Shot_Type_Label.raise_()
        self.Preview_Image_Selection_Line.raise_()
        self.Shot_Type_Line.raise_()
        self.Shot_Type_Line_2.raise_()
        self.Version.raise_()
        self.Version_Label.raise_()

        self.retranslateUi(Main)
        QMetaObject.connectSlotsByName(Main)

    def retranslateUi(self, Main):
        _translate = QCoreApplication.translate
        Main.setWindowTitle(_translate("Main", "Form"))
        self.Undist_Crop_Button.setText(_translate("Main", "Undist Crop"))
        self.Nuke_File_Button.setText(_translate("Main", "Nuke File"))
        self.Preview_Button.setText(_translate("Main", "Preview"))
        self.Nuke_LD_to_UV_Button.setText(_translate("Main", "LD to UV"))
        self.Preview_Image_Selection_Label.setText(_translate("Main", "Preview Image Selection"))
        self.Shot_Type_Label.setText(_translate("Main", "Shot Type"))
        self.Source_Button.setText(_translate("Main", "Source"))
        self.Crop_Button.setText(_translate("Main", "Crop"))
        self.Undist_Button.setText(_translate("Main", "Undist"))
        self.LD_Button.setText(_translate("Main", "LD Node"))
        self.UV_Button.setText(_translate("Main", "UV Map"))
        self.Version.setItemText(0, _translate("Main", "v001"))
        self.Version.setItemText(1, _translate("Main", "v002"))
        self.Version.setItemText(2, _translate("Main", "v003"))
        self.Version.setItemText(3, _translate("Main", "v004"))
        self.Version.setItemText(4, _translate("Main", "v005"))
        self.Version.setItemText(5, _translate("Main", "v006"))
        self.Version.setItemText(6, _translate("Main", "v007"))
        self.Version.setItemText(7, _translate("Main", "v008"))
        self.Version.setItemText(8, _translate("Main", "v009"))
        self.Version_Label.setText(_translate("Main", "Version"))
