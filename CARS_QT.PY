
from __future__ import unicode_literals
import sys
import os
import random
import time

import numpy as np
from numpy import arange, sin, pi

import scipy
import scipy.signal
import matplotlib.pyplot as plt

from openpyxl import Workbook
from openpyxl import load_workbook
import als_methods as als
import pre as crikit

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QInputDialog, QPushButton, QMainWindow, QApplication, QSpinBox, QLabel
from PyQt5.QtWidgets import QWidget, QAction, QTabWidget,QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QGroupBox, QDialog,QGridLayout
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QFileDialog
 
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

import matplotlib
# Make sure that we are using QT5BB
matplotlib.use('Qt5Agg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import matplotlib.animation as animation

progname = os.path.basename(sys.argv[0])
progversion = "0.1"



class App(QMainWindow):
 
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 tabs - pythonspot.com'
        self.left = 0
        self.top = 0
        self.width = 1000
        self.height = 800
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        self.table_widget = MyTableWidget(self)   # creat a Widgat.
        self.setCentralWidget(self.table_widget)  # set the Widget to be CentralWidget of QMainWindow.
 
        self.show()

class MyTableWidget(QWidget):        
 
    def __init__(self, parent):   
        super(QWidget, self).__init__(parent)
        
        self.layout = QVBoxLayout(self)           # create a Layout, which will be setted for self

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()   
        self.tab2 = QWidget()
        #self.tabs.resize(800,600) 
        
        self.tabs.addTab(self.tab1,"Tab 1")       # Add tabs
        self.tabs.addTab(self.tab2,"Tab 2")
 
        self.layout.addWidget(self.tabs)          # Add tabs to widget

        self.setLayout(self.layout)

        self.initalUI_tab_1()
        #self.initalUI_tab_2()

    def initalUI_tab_1(self):
        #################### Create Plot cavas widget ###################################################
                                                         # Create first tab
        self.tab1_layout = QHBoxLayout(self)             # create a Layout, which will be setted for tab_2

        self.tab1_layout_L = QVBoxLayout(self)

        self.button_openfile = QPushButton('Open file')           # Just some button connected to `plot` method
        self.button_openfile.clicked.connect(self.openFileNameDialog) 

        self.button_readfile = QPushButton('Read file')           # Just some button connected to `plot` method
        self.button_readfile.clicked.connect(self.readfile)
        
        self.display_inf = QPushButton("Display Inf.")
        self.display_inf.clicked.connect(self.showdialog)

        self.tab1_layout_L.addWidget(self.button_openfile)
        self.tab1_layout_L.addWidget(self.button_readfile)



        self.tab1_layout_R = QVBoxLayout(self)
        self.tab1_layout_R.addWidget(self.display_inf)

        self.tab1_layout.addLayout(self.tab1_layout_L)
        self.tab1_layout.addStretch()
        self.tab1_layout.addLayout(self.tab1_layout_R)

        self.tab1.setLayout(self.tab1_layout)              # set tab2.layout to be the layout of tab_2 

    #def initalUI_tab_2(self):
    #    pass
    def openFileNameDialog(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if self.fileName:
            print(self.fileName)
        
    def test_fun(self):
        pass

    def readfile(self):
        ##  --------------------------------------               Import the xlsx file
        W = load_workbook(self.fileName)
        p = W.get_sheet_by_name(name = 'Sheet1')

        a=[]

        for row in p.iter_rows():
            for k in row:
                a.append(k.internal_value)

        data = np.resize(a, [int(len(a)/15), 15])

        print("The dictionary name list is:\n", data[0,:])


        ##   --------------------------                       Function defination
        def nm2wavenumber(pump, antistokes):
            return 10**7*(1/np.array(antistokes) - 1/pump)
        def area(x):
            return np.sum(x)


        ##   -------------------------                       reshape the data to dictionary, and normalized the data which makes the area of each plot to unit 1;
        dic ={}
        for i in range(15):
            dic[data[0,i]] = data[1:2001,i].astype(np.float)


        dic_norm = {}  ## nornalized data dictionary
        for i in dic:
            #print(area(dic[i]))
            dic_norm[i] = dic[i]/area(dic[i])
        dic_norm["wavenumber"] = nm2wavenumber(1064, dic[data[0,0]])

        WN = dic_norm["wavenumber"]   ## wavenumber


                    ## the data list that we are intrested in, after delete bad data.
        background_list = ["background_1", "background_2", "background_3", "background_4", "background_5", 
        "background_6", "background_7", "background_8", "background_9"]

        signal_list = ["signal_1", "signal_2", "signal_3", "signal_4", "signal_5"]

        background =  0.0*dic_norm["background_1"]
        for i in background_list:
            background += dic_norm[i]
        background = background/len(background_list)     ## The average of background_list, which will be used as the background data.

        signal =  0.0*dic_norm["signal_1"]
        for i in signal_list:
            signal += dic_norm[i]
        signal = signal/len(signal_list)

        print("Number of background data is:", len(background_list))
        print("background is:", background)
        print("Number of signal data is:", len(signal_list))
        print("signal is:", signal)
    
    def showdialog(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText("This is a message box")
        msg.setInformativeText("This is additional information")
        msg.setWindowTitle("MessageBox demo")
        msg.setDetailedText("The details are as follows:")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.buttonClicked.connect(self.msgbtn)
            
        retval = msg.exec_()
        print("value of pressed message box button:", retval)
    def msgbtn(i):
        print ("Button pressed is:",i.text())


        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    print("the last step!")
    sys.exit(app.exec_())

