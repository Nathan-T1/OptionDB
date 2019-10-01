from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QWidget, QToolBox, QVBoxLayout, QLabel, QMenuBar
import sys
from PyQt5 import QtGui, QtCore, uic
from PyQt5.QtCore import QRect
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *



from Main import Ui_Form as Main_Ui_Form
from SinglePull import Ui_Form
from CustomPull import Ui_Form as CustomPull_Ui_Form
from UpdateDataBase import Ui_Form as UpdateDatabase_Ui_Form
from ExportCustomDay import Ui_Form as ExportCustomDay_Ui_Form
from ExportCustom import Ui_Form as ExportCustom_Ui_Form
from Mesh import Ui_Form as Mesh_Ui_Form

from sqlalchemy import select, create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy import *
import time

import Set_Up as Set_Up
import Data as Data

class ExportCustom(QDialog, ExportCustom_Ui_Form):
        
    def __init__(self, parent = None, *args, **kwargs):
            
        super(ExportCustom, self).__init__(*args, **kwargs)
        self.ui = ExportCustom_Ui_Form()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.ExportCustomPull)

    def ExportCustomPull(self):
        ticker = self.lineEdit.text()
        days = self.lineEdit_2.text()
        strikes = self.lineEdit_3.text()
        expirations = self.lineEdit_4.text()
        
        Data.ExportCustomPull(ticker, days, strikes, expirations)
class ExportDay(QDialog, ExportCustomDay_Ui_Form):
        
    def __init__(self, parent = None, *args, **kwargs):
            
        super(ExportDay, self).__init__(*args, **kwargs)
        self.ui = ExportCustomDay_Ui_Form()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.ExportDayPull)

    def ExportDayPull(self):
        ticker = self.lineEdit.text()
        day = self.lineEdit_2.text()
        
        Data.ExportDayPull(ticker, day)
class SinglePull(QDialog, Ui_Form):
        
    def __init__(self, parent = None, *args, **kwargs):
            
        super(SinglePull, self).__init__(*args, **kwargs)
        self.ui = Ui_Form()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.Single_Pull)

    def Single_Pull(self):
        ticker = self.lineEdit.text()
   
        if self.checkBox.isChecked():
            csv = 'yes'
        else:
            csv = 'no'
        if self.checkBox_2.isChecked():
            sql = 'yes'
        else:
            sql = 'no'
        Data.Single_Pull(ticker, csv, sql)

class CustomPull(QDialog, CustomPull_Ui_Form):
        
    def __init__(self, parent = None, *args, **kwargs):
            
        super(CustomPull, self).__init__(*args, **kwargs)
        self.ui = CustomPull_Ui_Form()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.Custom_Pull)
        
    def Custom_Pull(self):
            
        tickers = self.lineEdit.text()
        expirations = self.lineEdit_2.text()
        strikes = self.lineEdit_3.text()
        
        if self.checkBox.isChecked():
            csv = 'yes'
        else:
            csv = 'no'
        if self.checkBox_2.isChecked():
            sql = 'yes'
        else:
            sql = 'no'
        
        Data.Custom_Pull(tickers, expirations, strikes, csv, sql)

class Mesh(QDialog, Mesh_Ui_Form):
        
    def __init__(self, parent = None, *args, **kwargs):
            
        super(Mesh, self).__init__(*args, **kwargs)
        self.ui = Mesh_Ui_Form()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.Create_Mesh)

    def Create_Mesh(self):

        ticker = self.lineEdit.text()
        day = self.lineEdit_2.text()
        target = self.lineEdit_3.text()
        min_strike = self.lineEdit_4.text()
        max_strike = self.lineEdit_5.text()
        
        if self.checkBox.isChecked():
            csv = 'yes'
        else:
            csv = 'no'
        if self.radioButton.isChecked():
            flag = 'Call'
        else:
            flag = 'Put'
        print(ticker, day, target, csv, flag)
        Data.Create_Mesh(ticker, day, target, csv, flag, min_strike, max_strike)

        
class UpdateDatabase(QDialog, UpdateDatabase_Ui_Form):
        
    def __init__(self, parent = None, *args, **kwargs):
            
        super(UpdateDatabase, self).__init__(*args, **kwargs)
        self.ui = UpdateDatabase_Ui_Form()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.Add)
        self.pushButton_2.clicked.connect(self.Delete)
        self.pushButton_3.clicked.connect(self.UpdateDatabase)
        
        engine = create_engine('sqlite:///C:\\OptionDB\\MAIN.db')
        conn = engine.connect()

        try:
            meta = MetaData(engine,reflect=True)
            table = meta.tables['DB_List']
            my_select = select([table])
        except:
            meta = MetaData(engine,reflect=True)
            DB_List = Table(
           'DB_List', meta, 
           Column('Ticker', String, primary_key = True), 
        )
            meta.create_all(engine)

        res = conn.execute(my_select)
        tickers = []
        for row in res:
                ticker = str(row.Ticker)
                tickers.append(ticker)
                
        self.comboBox.addItems(tickers)
        
    def UpdateDatabase(self):
            engine = create_engine('sqlite:///C:\\OptionDB\\MAIN.db')
            conn = engine.connect()
        
            meta = MetaData(engine,reflect=True)
            table = meta.tables['DB_List']
            my_select = select([table])

            res = conn.execute(my_select)
            tickers = []
            for row in res:
                    ticker = str(row.Ticker)
                    tickers.append(ticker)
            for ticker in tickers:
                    Data.Single_Pull(ticker, 'no', 'yes')
                    time.sleep(5)
                    

    def Add(self):
            engine = create_engine('sqlite:///C:\\OptionDB\\MAIN.db', echo = True)
            metadata = MetaData(engine)
            
            
            
            ticker = self.lineEdit.text()
            DB_List = Table('DB_List', metadata, autoload=True)
            i = DB_List.insert()
            i = i.values({"Ticker": ticker})
            i.execute(Ticker = ticker)
            
    def Delete(self):
            engine = create_engine('sqlite:///C:\\OptionDB\\MAIN.db', echo = True)
            connection = engine.connect()
            metadata = MetaData(engine)
            
            
            
            ticker = self.lineEdit.text()
            DB_List = Table('DB_List', metadata, autoload=True)
            print(ticker)
            i = delete(DB_List, DB_List.c.Ticker==ticker)
            connection.execute(i)
            
         

class MainWindow(QMainWindow, Main_Ui_Form):

        def __init__(self):

                super(MainWindow,self).__init__()
                self.ui = Main_Ui_Form()
                self.setupUi(self)
                self.Export_Day.clicked.connect(self.ExportDay)
                self.Export_Custom.clicked.connect(self.ExportCustom)
                self.API_Key.clicked.connect(self.Add_Tradier)
                self.CreateDB.clicked.connect(Set_Up.InitDB)
                self.Generate_Archive.clicked.connect(Set_Up.InitArchive)
                self.Single_Pull.clicked.connect(self.executeSinglePull)
                self.Custom_Pull.clicked.connect(self.executeCustomPull)
                self.UpdateDB.clicked.connect(self.executeUpdateDatabase)
                self.Mesh.clicked.connect(self.executeMesh)
                
           
        def ExportDay(self):
                dlg = ExportDay(self)
                dlg.exec_()
        def ExportCustom(self):
                dlg = ExportCustom(self)
                dlg.exec_()        
        def executeSinglePull(self):
                dlg = SinglePull(self)
                dlg.exec_()
        def executeCustomPull(self):
                dlg = CustomPull(self)
                dlg.exec_()
        def executeUpdateDatabase(self):
                dlg = UpdateDatabase(self)
                dlg.exec_()
        def executeMesh(self):
                dlg = Mesh(self)
                dlg.exec_()
  
        
        def Add_Tradier(self):
                text, ok = QInputDialog.getText(self, 'Input Dialog', 'API Key:')
                if ok:
                    key = str(text)
                    Set_Up.Add_Tradier(key)
                    
       
                    

                     

if __name__ == "__main__":
        App = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(App.exec())
        

