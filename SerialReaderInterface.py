##Will McGinnis
##WanderTechnologies.com
##7/15/2012
##Version 1.2.0
##
##SerialReader desktop application
##-Reads in serial data from Arduino devices
##-If data is in CSV format, with time or count in column 1, real time plotting is enabled
##    -Only supported for 4 channels at this time
##    -Use slower updates to ensure reliabiltiy (1 line per second or so)
   

#Imports required to package PyQTGraph
import myListdir

#The normal stuff
import sys
import os
import serial
import threading
import time
import numpy as np
import datetime as dt

from PyQt4.QtGui import (QMainWindow, QApplication, QFileDialog, QKeySequence, QAction, QIcon, QPixmap, QSplashScreen)
from PyQt4.QtCore import SIGNAL

from serialReaderGui import Ui_MainWindow

__version__="1.2.0";

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        #Start button
        self.pushButton.clicked.connect(self.startStream)
        self.pushButton.setDefault(True)
        self.pushButton.setEnabled(True)

        #Flag button
        self.pushButton_2.clicked.connect(self.addFlag)
        self.pushButton_2.setDefault(False)
        self.pushButton_2.setEnabled(False)

        #Stop Button
        #Currently disabled.  Current implimentation will place flag in middle of line.
        self.pushButton_3.clicked.connect(self.stop)
        self.pushButton_3.setDefault(False)
        self.pushButton_3.setEnabled(False)

        #Clear Button
        self.pushButton_4.clicked.connect(self.clearBrowser)
        self.pushButton_4.setDefault(False)
        self.pushButton_4.setEnabled(False)

        #Plotting Checkbox
        self.checkBox.stateChanged.connect(self.setPlotting)
        self.checkBox.setEnabled(True)

        #Plot One
        self.plotOne=self.graphicsView.getPlotItem()
        self.viewBoxOne=self.plotOne.getViewBox()
        self.viewBoxOne.enableAutoRange(axis=self.viewBoxOne.XYAxes, enable=True)
        self.plotOne.setLabel('left', text='Measure', units='Units', unitPrefix=None)
        self.plotOne.setLabel('right', text='Measure', units='Units', unitPrefix=None)
        self.plotOne.setLabel('bottom', text='Time', units='Seconds', unitPrefix=None)
        self.plotOne.setTitle(title='Series One')
        self.plotOne.showLabel('left', show=True)
        self.plotOne.showLabel('right', show=True)
        self.plotOne.showLabel('bottom', show=True)
        self.plotOne.showGrid(x=True, y=True, alpha=0.5)

        #Plot Two
        self.plotTwo=self.graphicsView_2.getPlotItem()
        self.viewBoxTwo=self.plotTwo.getViewBox()
        self.viewBoxTwo.enableAutoRange(axis=self.viewBoxTwo.XYAxes, enable=True)
        self.plotTwo.setLabel('left', text='Measure', units='Units', unitPrefix=None)
        self.plotTwo.setLabel('right', text='Measure', units='Units', unitPrefix=None)
        self.plotTwo.setLabel('bottom', text='Time', units='Seconds', unitPrefix=None)
        self.plotTwo.setTitle(title='Series Two')
        self.plotTwo.showLabel('left', show=True)
        self.plotTwo.showLabel('right', show=True)
        self.plotTwo.showLabel('bottom', show=True)
        self.plotTwo.showGrid(x=True, y=True, alpha=0.5)

        #Plot Three
        self.plotThree=self.graphicsView_3.getPlotItem()
        self.viewBoxThree=self.plotThree.getViewBox()
        self.viewBoxThree.enableAutoRange(axis=self.viewBoxThree.XYAxes, enable=True)
        self.plotThree.setLabel('left', text='Measure', units='Units', unitPrefix=None)
        self.plotThree.setLabel('right', text='Measure', units='Units', unitPrefix=None)
        self.plotThree.setLabel('bottom', text='Time', units='Seconds', unitPrefix=None)
        self.plotThree.setTitle(title='Series Three')
        self.plotThree.showLabel('left', show=True)
        self.plotThree.showLabel('right', show=True)
        self.plotThree.showLabel('bottom', show=True)
        self.plotThree.showGrid(x=True, y=True, alpha=0.5)
        self.viewBoxThree.setMouseMode(self.viewBoxThree.RectMode)
        
        #Plot Four
        self.plotFour=self.graphicsView_4.getPlotItem()
        self.viewBoxFour=self.plotFour.getViewBox()
        self.viewBoxFour.enableAutoRange(axis=self.viewBoxFour.XYAxes, enable=True)
        self.plotFour.setLabel('left', text='Measure', units='Units', unitPrefix=None)
        self.plotFour.setLabel('right', text='Measure', units='Units', unitPrefix=None)
        self.plotFour.setLabel('bottom', text='Time', units='Seconds', unitPrefix=None)
        self.plotFour.setTitle(title='Series Four')
        self.plotFour.showLabel('left', show=True)
        self.plotFour.showLabel('right', show=True)
        self.plotFour.showLabel('bottom', show=True)
        self.plotFour.showGrid(x=True, y=True, alpha=0.5)
        self.viewBoxFour.setMouseMode(self.viewBoxFour.RectMode)

        #Vectors for  plotting
        self.timeSeries=[]
        self.seriesOne=[]
        self.seriesTwo=[]
        self.seriesThree=[]
        self.seriesFour=[]
        self.plotting=False

        #Baud Rate selection
        self.comboBox.activated.connect(self.setBaud)
        #COMPORT selection
        self.comboBox_2.activated.connect(self.setCOM)
        
        self.flag=False
        self.run=True
        self.baudrate=9600
        self.comport=0
        self.filename="logfile.csv"
        self.lineEdit.textChanged.connect(self.setFileName)

        self.directory=os.getcwd()+'\\files\\'
        if not os.path.exists(self.directory):
                os.makedirs(self.directory)

    def setFileName(self):
        if self.lineEdit.text()=="":
            self.filename="logfile.csv"
        else:
            self.filename=self.lineEdit.text()+".csv"
        
    def setBaud(self, index):
        if index==0:
            self.baudrate=9600
        else:
            self.baudrate=int(self.comboBox.itemText(index))

    def setCOM(self, index):
        if index==0:
            self.comport=0
        else:
            self.comport=int(self.comboBox_2.itemText(index))-1
        
    def startStream(self):
        self.run=True
        self.pushButton_2.setEnabled(False)
        self.pushButton_3.setEnabled(True)
        self.pushButton_4.setEnabled(True)

        
        try:
            ser = serial.Serial(self.comport, self.baudrate, timeout=0)
        except serial.serialutil.SerialException:
            self.textBrowser.append('\n\nLooks sorta like you picked the wrong COM port')

            
        try:
            text_file = open(self.directory+self.filename, "w")
        except IOError:
            self.textBrowser.append('\n\nFile open in another program')
        start_time=time.clock();
        app.processEvents()
        while self.run:
            line = ser.readline()
            if line=="":
                continue
            text_file.write(line)
            self.textBrowser.insertPlainText(line)
            max_scale=int(self.textBrowser.verticalScrollBar().maximum())
            self.textBrowser.verticalScrollBar().setSliderPosition(max_scale)

            #first processing in case the plots dont change.
            app.processEvents()
            
            read_data=self.textBrowser.toPlainText()
            read_data=read_data.split('\n')
            csvlist=read_data[len(read_data)-2].split(',')
        
            #print read_data[len(read_data)-2]
            if self.plotting==True:
                if len(csvlist)>3:
                    try:
                        #saving the time vector and converting from ms to seconds
                        self.timeSeries.append(float(csvlist[0])/1000)
                    except ValueError:
                        print "time series error"
                        continue
                    
                    if len(csvlist)>1:
                        try:
                            self.seriesOne.append(float(csvlist[1]))
                            self.graphicsView.clear()
                            self.graphicsView.plot(np.array(self.timeSeries),np.array(self.seriesOne), pen=(1,4))
                        except ValueError:
                            print "series one error"
                            self.seriesOne.append(0.0)
                            
                    
                    if len(csvlist)>2:
                        try:
                            self.seriesTwo.append(float(csvlist[2]))
                            self.graphicsView_2.clear()
                            self.graphicsView_2.plot(np.array(self.timeSeries),np.array(self.seriesTwo), pen=(2,4))
                        except ValueError:
                            print "series two error"
                            self.seriesTwo.append(0.0)
                            
                    
                    if len(csvlist)>3:
                        try:
                            self.seriesThree.append(float(csvlist[3]))
                            self.graphicsView_3.clear()
                            self.graphicsView_3.plot(np.array(self.timeSeries),np.array(self.seriesThree), pen=(3,4))
                        except ValueError:
                            print "series three error"
                            self.seriesThree.append(0.0)
                            
                        
                    if len(csvlist)>4:
                        try:
                            #if this is the last entry, it will have a newline \n, which needs to be removed
                            temp=csvlist[4].split("\\")
                            self.seriesFour.append(float(temp[0]))
                            self.graphicsView_4.clear()
                            self.graphicsView_4.plot(np.array(self.timeSeries),np.array(self.seriesFour), pen=(4,4))
                        except ValueError:
                            print "series four error"
                            self.seriesFour.append(0.0)
        app.processEvents()               
        text_file.close()
        
    def addFlag(self):
        self.flag=True

    def closeEvent(self, event):
        self.stop()
        event.accept()
        
    def removeFlag(self):
        self.flag=False

    def stop(self):
        self.run=False
        self.textBrowser.append("Log file saved to "+self.filename);
        
    def clearBrowser(self):
        self.textBrowser.setText("")

    def setPlotting(self):
        if self.checkBox.checkState()==0:
            self.plotting=False
            self.timeSeries=[]
            self.seriesOne=[]
            self.seriesTwo=[]
            self.seriesThree=[]
            self.seriesFour=[]
            self.graphicsView.clear()
            self.graphicsView_2.clear()
            self.graphicsView_3.clear()
            self.graphicsView_4.clear()
            #Plot One
            self.plotOne=self.graphicsView.getPlotItem()
            self.viewBoxOne=self.plotOne.getViewBox()
            self.viewBoxOne.enableAutoRange(axis=self.viewBoxOne.XYAxes, enable=True)
            self.plotOne.setLabel('left', text='Measure', units='Units', unitPrefix=None)
            self.plotOne.setLabel('right', text='Measure', units='Units', unitPrefix=None)
            self.plotOne.setLabel('bottom', text='Time', units='Seconds', unitPrefix=None)
            self.plotOne.setTitle(title='Series One')
            self.plotOne.showLabel('left', show=True)
            self.plotOne.showLabel('right', show=True)
            self.plotOne.showLabel('bottom', show=True)
            self.plotOne.showGrid(x=True, y=True, alpha=0.5)

            #Plot Two
            self.plotTwo=self.graphicsView_2.getPlotItem()
            self.viewBoxTwo=self.plotTwo.getViewBox()
            self.viewBoxTwo.enableAutoRange(axis=self.viewBoxTwo.XYAxes, enable=True)
            self.plotTwo.setLabel('left', text='Measure', units='Units', unitPrefix=None)
            self.plotTwo.setLabel('right', text='Measure', units='Units', unitPrefix=None)
            self.plotTwo.setLabel('bottom', text='Time', units='Seconds', unitPrefix=None)
            self.plotTwo.setTitle(title='Series Two')
            self.plotTwo.showLabel('left', show=True)
            self.plotTwo.showLabel('right', show=True)
            self.plotTwo.showLabel('bottom', show=True)
            self.plotTwo.showGrid(x=True, y=True, alpha=0.5)

            #Plot Three
            self.plotThree=self.graphicsView_3.getPlotItem()
            self.viewBoxThree=self.plotThree.getViewBox()
            self.viewBoxThree.enableAutoRange(axis=self.viewBoxThree.XYAxes, enable=True)
            self.plotThree.setLabel('left', text='Measure', units='Units', unitPrefix=None)
            self.plotThree.setLabel('right', text='Measure', units='Units', unitPrefix=None)
            self.plotThree.setLabel('bottom', text='Time', units='Seconds', unitPrefix=None)
            self.plotThree.setTitle(title='Series Three')
            self.plotThree.showLabel('left', show=True)
            self.plotThree.showLabel('right', show=True)
            self.plotThree.showLabel('bottom', show=True)
            self.plotThree.showGrid(x=True, y=True, alpha=0.5)
            self.viewBoxThree.setMouseMode(self.viewBoxThree.RectMode)
            
            #Plot Four
            self.plotFour=self.graphicsView_4.getPlotItem()
            self.viewBoxFour=self.plotFour.getViewBox()
            self.viewBoxFour.enableAutoRange(axis=self.viewBoxFour.XYAxes, enable=True)
            self.plotFour.setLabel('left', text='Measure', units='Units', unitPrefix=None)
            self.plotFour.setLabel('right', text='Measure', units='Units', unitPrefix=None)
            self.plotFour.setLabel('bottom', text='Time', units='Seconds', unitPrefix=None)
            self.plotFour.setTitle(title='Series Four')
            self.plotFour.showLabel('left', show=True)
            self.plotFour.showLabel('right', show=True)
            self.plotFour.showLabel('bottom', show=True)
            self.plotFour.showGrid(x=True, y=True, alpha=0.5)
            self.viewBoxFour.setMouseMode(self.viewBoxFour.RectMode)
        else:
            self.plotting=True
    
        
if __name__=='__main__':
    import sys, time
    
    app=QApplication(sys.argv)
    splash_pix=QPixmap('logo3.png')
    splash=QSplashScreen(splash_pix)
    splash.setMask(splash_pix.mask())
    splash.show()
    app.processEvents()

    time.sleep(2)
    
    frame=MainWindow()
    frame.show()
    splash.finish(frame)
    app.exec_()
