# SoapySDR is the API for the hackrf
import SoapySDR
from SoapySDR import Device, SOAPY_SDR_RX, SOAPY_SDR_CF32
# Using pyfftw instead of numpy to calculate fft faster
from pyfftw.interfaces import numpy_fft as fastnumpyfft
# use numpy for buffers
import numpy as np
import functions
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from threading import Thread
import time


# The main function. Here all the variables are setting when button clicks
def mainGUI(self):
    def update_chart(self):
        self.line.set_xdata((self.freqs + self.rx_freq)/1e6)  # update the data on x axis (if user changed frequency)
        if self.logScaleBool:
            self.line.set_ydata(np.log10(np.abs(self.signal)))
        else:
            self.line.set_ydata(np.abs(self.signal))  # update the data on y axis
        self.ax.relim()
        self.ax.autoscale()
        self.canvas.draw()
        # self.ax.pause(0.01)

    # If the user wants to clear the plot
    def clearPlot():
        if not np.argmax(np.abs(self.dft)) == 0:
            self.dftMaxHold, self.dftMovingAverage = functions.clearPlotFunc(self.dft)

    def errorMsg(errorString):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Error")
        msg.setText(errorString)
        msg.setStandardButtons(QMessageBox.Ok)
        appIcon = QIcon("icon.png")
        msg.setWindowIcon(appIcon)
        msg.exec_()

    # This is the Loop which running in Thread
    def loop(self):
        while self.running:
            # save old dft samples for later use
            self.dftOld = self.dft

            # get the samples into the buffer and normalize
            self.samples = functions.getSamples(self.sdr, self.stream, self.samplesPerRead, self.samplesPerIteration)

            # Perform dft on the received samples and normalize
            self.dft = fastnumpyfft.fftshift(fastnumpyfft.fft(self.samples, self.samplesPerIteration))
            self.dft = functions.normArr(self.dft)

            self.dftMovingAverage = self.dft

            # Applying Moving Average Function
            if self.movingAverageBool:
                self.dftMovingAverage =\
                    functions.movingAverageFunc(self.dftOld, self.dft,self.samplesPerIteration, self.movingAverageRatio)

            self.signal, self.dftMaxHold =\
                functions.assignAppropriateSignal(self.maxHoldBool, self.movingAverageBool, self.dft,
                                                  self.dftMaxHold, self.dftMovingAverage)

            update_chart(self)
            time.sleep(0.1)

    self.ui.btnStart.clicked.connect(lambda: updateSettings())
    self.ui.btnClear.clicked.connect(lambda: clearPlot())
    self.threadSM = Thread(target=loop, args=(self,))
    # show soapySDR devices available
    results = SoapySDR.Device.enumerate()
    print("Available devices:")
    for result in results: print(result)

    # create device instance
    # args can be user defined or from the enumeration result
    args = dict(driver="hackrf")
    self.sdr = SoapySDR.Device(args)
    self.dft = self.dftMaxHold = self.dftMovingAverage = np.zeros(4096)
    self.ui.btnClear.setEnabled(False)
    self.ui.chklog.setEnabled(False)
    self.ui.chkMax.setEnabled(False)
    self.ui.chkAvg.setEnabled(False)
    self.ui.avgRatio.setEnabled(False)
    self.ui.label_14.setEnabled(False)
    self.started = False
    self.ui.perRead.setCurrentIndex(2)
    self.ui.perIteration.setCurrentIndex(1)
    self.ui.avgRatio.setCurrentIndex(1)

    def updateSettings():
        basicErrStr = "cannot be blank / with illegal characters (letters and signs)"
        if self.ui.gain.text() != "" and self.ui.gain.text().isnumeric():
            if 0 <= int(self.ui.gain.text()) <= 90:
                if self.ui.rxFreq.text() != "" and self.ui.rxFreq.text().replace('.','',1).isdigit():
                    if 1 <= float(self.ui.rxFreq.text()) <= 6000:
                        if self.ui.sampleRate.text() != "" and self.ui.sampleRate.text().isnumeric():
                            if 2 <= int(self.ui.sampleRate.text()) <= 20:
                                self.rx_freq = float(self.ui.rxFreq.text()) * 1e6
                                self.samp_rate = float(self.ui.sampleRate.text()) * 1e6
                                self.gainRX = int(self.ui.gain.text())
                                self.bandwidthFilter = float(self.ui.bandwidthFilter.currentText())
                                self.movingAverageRatio = float(self.ui.avgRatio.currentText())
                                self.samplesPerRead = int(self.ui.perRead.currentText())
                                self.samplesPerIteration = int(self.ui.perIteration.currentText())
                                self.maxHoldBool = self.ui.chkMax.isChecked()
                                self.movingAverageBool = self.ui.chkAvg.isChecked()
                                self.logScaleBool = self.ui.chklog.isChecked()
                                self.freqs = fastnumpyfft.fftshift(fastnumpyfft.fftfreq(self.samplesPerIteration,
                                                                                        d=1/self.samp_rate))
                                functions.initializeHackRF(self.sdr, self.samp_rate, self.rx_freq, self.bandwidthFilter,
                                                           self.gainRX)
                                clearPlot()

                                if not self.threadSM.is_alive():
                                    self.ui.btnClear.setEnabled(True)
                                    self.ui.chklog.setEnabled(True)
                                    self.ui.chkMax.setEnabled(True)
                                    self.ui.chkAvg.setEnabled(True)
                                    self.ui.avgRatio.setEnabled(True)
                                    self.ui.label_14.setEnabled(True)
                                    self.stream = functions.setStream(self.sdr)
                                    self.threadSM.start()
                                    self.started = True
                            else: errorMsg("Sample rate must be between 2MS/sec and 20MS/sec")
                        else: errorMsg("Sample rate " + basicErrStr)
                    else: errorMsg("RX frequency must be between 1MHz and 6GHz")
                else: errorMsg("RX frequency " + basicErrStr)
            else: errorMsg("Gain must be bigger than 0 or smaller than 90")
        else: errorMsg("Gain " + basicErrStr)

