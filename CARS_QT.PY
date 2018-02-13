
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

###   homemade package

from Cars_Class import  CARS, KK_ALS_Spectral

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

        self.fileName = ''

        
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
        self.initalUI_tab_2()

    def initalUI_tab_1(self):
        #################### Create Plot cavas widget ###################################################
                                                         # Create first tab
        self.tab1_layout = QHBoxLayout(self)             # create a Layout, which will be setted for tab_2

        self.tab1_layout_L = QVBoxLayout(self)

        self.button_openBackgroundfile = QPushButton('Open Background File')           # Just some button connected to `plot` method
        self.button_openBackgroundfile.clicked.connect(self.openFileNameDialog) 
        self.button_openSignalfile = QPushButton('Open Signal File')           # Just some button connected to `plot` method
        self.button_openSignalfile.clicked.connect(self.openFileNameDialog) 
        
        self.tab1_layout_L.addWidget(self.button_openBackgroundfile)
        self.tab1_layout_L.addWidget(self.button_openSignalfile)

        self.tab1_layout_R = QVBoxLayout(self)

        self.plotUp = plt.figure("Background")

        axes_Up = self.plotUp.add_subplot(111)

        self.add_plotfigure(self.plotUp, self.tab1_layout_R)
        
        self.buttonPlotUp = QPushButton('Plot')           #  Just some button connected to `plot` method 
        self.buttonPlotUp.clicked.connect(self.test_fun(axes_Up, "background"))
        self.tab1_layout_R.addWidget(self.buttonPlotUp)

        self.plotDown = plt.figure("Signal")
        axes_Down = self.plotDown.add_subplot(111)

        self.add_plotfigure(self.plotDown, self.tab1_layout_R)
        
        self.buttonPlotDown = QPushButton('Plot')           # Just some button connected to `plot` method 
        self.buttonPlotDown.clicked.connect(self.test_fun(axes_Down, "signal")) 
        self.tab1_layout_R.addWidget(self.buttonPlotDown)


        self.tab1_layout.addLayout(self.tab1_layout_L)
        #self.tab1_layout.addStretch()
        self.tab1_layout.addLayout(self.tab1_layout_R)

        self.tab1.setLayout(self.tab1_layout)              # set tab1.layout to be the layout of tab_1 

    def initalUI_tab_2(self):
        #################### Create Plot cavas widget ###################################################
                                                         # Create first tab
        self.tab2_layout = QVBoxLayout(self)             # create a Layout, which will be setted for tab_2


        self.tab2PlotUp = plt.figure("Background and Singal")
        self.add_plotfigure(self.tab2PlotUp, self.tab2_layout)
        tab2Axes_Up = self.tab2PlotUp.add_subplot(111)

        self.tab2buttonPlotUp = QPushButton('Plot Back + Siganl')           #  Just some button connected to `plot` method 
        self.tab2buttonPlotUp.clicked.connect(self.test_fun(tab2Axes_Up, "Background and Singal"))


        self.button_CARS2SPET = QPushButton('CARS --> SPET')           # Just some button connected to `plot` method
        self.button_CARS2SPET.clicked.connect(self.CARS2SPET) 
        
        self.tab2_layout.addWidget(self.tab2buttonPlotUp)
        self.tab2_layout.addWidget(self.button_CARS2SPET)


        self.tab2.setLayout(self.tab2_layout)              # set tab1.layout to be the layout of tab_1 

    def openFileNameDialog(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if self.fileName:
            print(self.fileName)
        

    def test_fun(self, axes, dataName):

        def inner_test_fun():
            
            print("dataName", dataName)

            # save the background data and signal data, which will be used to get the spectrume.
            if dataName == "background" or dataName == "signal":
                ## read the file that you just open
                self.readfile()

                if dataName == "background":
                    #print("background")
                    self.background = self.dicDataNorm["averageIntensity"]
                    #print(self.background)
                elif dataName == "signal":
                    #print("signal")
                    self.signal = self.dicDataNorm["averageIntensity"]
                    #print(self.signal)

                for key, value in self.dicDataNorm.items():
                    if (key != "wavenumber" and key != "wavelength"):
                        print(key)
                        axes.plot(self.WN, value, label = key)

            elif dataName == "Background and Singal":

                axes.plot(self.WN, self.signal, label = "signal")
                axes.plot(self.WN, self.background, label = "background")

                pass
            
            
            axes.legend()
            axes.set_xlabel('Wavenumber (cm$^{-1}$)')
            axes.set_ylabel('Spectrum (au)')

        return inner_test_fun

    def CARS2SPET(self):

        self.finalPlot = plt.figure("CARS2SPET")

        self.finalAxes = self.finalPlot.add_subplot(111)
        self.finalAxes.plot(self.backgroundData)

        #self.finalAxes.figure.canvas.draw()
        #plt.draw()

        #print(self.backgroundData)
        #print(self.signal)

    
    def readfile(self):
            ## read the data 
            app = CARS()
            self.dicData, self.dicDataNorm = app.loadData(self.fileName)

            self.WN = self.dicDataNorm["wavenumber"]
            averageIntensity =  0.0 * self.dicDataNorm["wavenumber"]

            ## then plot the data
            for key, value in self.dicDataNorm.items():
                if (key != "wavenumber" and key != "wavelength"):
                    averageIntensity += value
                
            # there are two list that are not the intensity data  
            # dicDataNorm["wavenumber"] and dicDataNorm["wavelength"]
            # add the "averageIntensity" to dicDataNorm,  which will be used to calculate the spectrum
            self.dicDataNorm["averageIntensity"] = averageIntensity/(len(self.dicDataNorm) - 2)
            #print("averageIntensity is ", self.dicDataNorm["averageIntensity"])


        #dicSignal, dicSignalNorm = app.loadData('spectra_signal.xlsx')
        #return dicBackground, dicBackgroundNorm
    
    
    def showdialog(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText("This is a message box")
        msg.setInformativeText("This is additional information")
        msg.setWindowTitle("MessageBox demo")
        msg.setDetailedText("The details are as follows:")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)


    def add_plotfigure(self, figureName, plot_layout):
        #self.figureName = plt.figure()                      # a figure instance to plot on
                                                            #if put "plt.ion" on the head, which will make two more figures idependently.

        # this is the Canvas Widget that displays the `figure`, it takes the `figure` instance as a parameter to __init__
        canvas_figureName = FigureCanvas(figureName)
        toolbar_figureName = NavigationToolbar(canvas_figureName, self) # this is the Navigation widget, it takes the Canvas widget and a parent
        
        plot_layout.addWidget(toolbar_figureName)         # this also needed to show the Navigation of plot
        plot_layout.addWidget(canvas_figureName)          # add Canvas Widget(plot widget) onto tab_2

    def plotFigure(self):
        app = CARS()
        app.plotPredata(self.dicBackground, self.plotUp)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    print("the last step!")
    sys.exit(app.exec_())

