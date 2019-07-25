# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Main.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(697, 596)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(20, 10, 191, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.line = QtWidgets.QFrame(Form)
        self.line.setGeometry(QtCore.QRect(180, 0, 161, 621))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(Form)
        self.line_2.setGeometry(QtCore.QRect(260, 205, 441, 41))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(50, 130, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.API_Key = QtWidgets.QPushButton(Form)
        self.API_Key.setGeometry(QtCore.QRect(80, 180, 101, 23))
        self.API_Key.setObjectName("API_Key")
        self.CreateDB = QtWidgets.QPushButton(Form)
        self.CreateDB.setGeometry(QtCore.QRect(80, 220, 101, 23))
        self.CreateDB.setObjectName("CreateDB")
        self.Generate_Archive = QtWidgets.QPushButton(Form)
        self.Generate_Archive.setGeometry(QtCore.QRect(80, 260, 101, 23))
        self.Generate_Archive.setObjectName("Generate_Archive")
        self.Data = QtWidgets.QLabel(Form)
        self.Data.setGeometry(QtCore.QRect(300, 20, 47, 13))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.Data.setFont(font)
        self.Data.setObjectName("Data")
        self.Single_Pull = QtWidgets.QPushButton(Form)
        self.Single_Pull.setGeometry(QtCore.QRect(340, 50, 91, 23))
        self.Single_Pull.setObjectName("Single_Pull")
        self.Custom_Pull = QtWidgets.QPushButton(Form)
        self.Custom_Pull.setGeometry(QtCore.QRect(340, 80, 91, 23))
        self.Custom_Pull.setObjectName("Custom_Pull")
        self.UpdateDB = QtWidgets.QPushButton(Form)
        self.UpdateDB.setGeometry(QtCore.QRect(340, 110, 91, 23))
        self.UpdateDB.setObjectName("UpdateDB")
        self.Archive = QtWidgets.QPushButton(Form)
        self.Archive.setGeometry(QtCore.QRect(340, 140, 91, 23))
        self.Archive.setObjectName("Archive")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(290, 250, 91, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(330, 290, 47, 13))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(510, 290, 47, 13))
        self.label_5.setObjectName("label_5")
        self.Export_Day = QtWidgets.QPushButton(Form)
        self.Export_Day.setGeometry(QtCore.QRect(530, 320, 101, 23))
        self.Export_Day.setObjectName("Export_Day")
        self.Export_Custom = QtWidgets.QPushButton(Form)
        self.Export_Custom.setGeometry(QtCore.QRect(530, 360, 101, 23))
        self.Export_Custom.setObjectName("Export_Custom")
        self.Export_Archive = QtWidgets.QPushButton(Form)
        self.Export_Archive.setGeometry(QtCore.QRect(530, 400, 101, 23))
        self.Export_Archive.setObjectName("Export_Archive")
        self.Mesh = QtWidgets.QPushButton(Form)
        self.Mesh.setGeometry(QtCore.QRect(340, 320, 101, 23))
        self.Mesh.setObjectName("Mesh")
        self.Hisotry = QtWidgets.QPushButton(Form)
        self.Hisotry.setGeometry(QtCore.QRect(340, 360, 101, 23))
        self.Hisotry.setObjectName("Hisotry")
        self.Archive_A = QtWidgets.QPushButton(Form)
        self.Archive_A.setGeometry(QtCore.QRect(340, 400, 101, 23))
        self.Archive_A.setObjectName("Archive_A")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "OptionsDB"))
        self.label_2.setText(_translate("Form", "Set Up"))
        self.API_Key.setText(_translate("Form", "API Key"))
        self.CreateDB.setText(_translate("Form", "Generate DB"))
        self.Generate_Archive.setText(_translate("Form", "Generate Archive"))
        self.Data.setText(_translate("Form", "Data"))
        self.Single_Pull.setText(_translate("Form", "Single Pull"))
        self.Custom_Pull.setText(_translate("Form", "Custom Pull"))
        self.UpdateDB.setText(_translate("Form", "Update DB"))
        self.Archive.setText(_translate("Form", "Archive Data"))
        self.label_3.setText(_translate("Form", "Analysis"))
        self.label_4.setText(_translate("Form", "In App"))
        self.label_5.setText(_translate("Form", "Export"))
        self.Export_Day.setText(_translate("Form", "Export Day "))
        self.Export_Custom.setText(_translate("Form", "Export Custom"))
        self.Export_Archive.setText(_translate("Form", "Export Archive"))
        self.Mesh.setText(_translate("Form", "Create Mesh"))
        self.Hisotry.setText(_translate("Form", "Historical View"))
        self.Archive_A.setText(_translate("Form", "Archive Analysis"))
