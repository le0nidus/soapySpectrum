from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCharts import *
from threading import Thread
import time

i = 0  # For the Chart updating example

''' 
Update Chart function. You can draw chart changing this function
'''


def update_chart(self):
    # Here is an example
    global i
    i += 1
    self.ax.plot([0, 1, 2, 3, 4], [10, 1, 20, i, 40])
    self.canvas.draw()


''' 
This is the Loop which running in Thread
'''


def loop(self):
    while self.running:
        update_chart(self)
        time.sleep(0.1)


''' 
The main function. Here all the variables are setting when button clicks
'''
def mainGUI(self):
    self.ui.btnStart.clicked.connect(lambda: updateSettings())
    self.ui.btnClear.clicked.connect(lambda: clearPlot())
    self.threadSM = Thread(target=loop, args=(self,))

    def updateSettings():
        if self.ui.gain.text() != "":
            if (0 <= int(self.ui.gain.text()) <= 90):
                rx_freq = float(self.ui.rxFreq.text())
                samp_rate = float(self.ui.sampleRate.text())
                gainRX = int(self.ui.gain.text())
                bandwidthFilter = float(self.ui.bandwidthFilter.currentText())
                movingAverageRatio = float(self.ui.avgRatio.currentText())
                samplesPerRead = int(self.ui.perRead.currentText())
                samplesPerIteration = int(self.ui.perIteration.currentText())
                maxHoldBool = self.ui.chkMax.isChecked()
                movingAverageBool = self.ui.chkAvg.isChecked()
                logScaleBool = self.ui.chklog.isChecked()
                if not self.threadSM.is_alive():
                    self.threadSM.start()
            else:
                print("rxgain bigger than 90 or smaller than 0")

    def clearPlot():
        clearPlotBool = True
        self.ax.cla()
