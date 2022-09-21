# SoapySDR is the API for the hackrf
import SoapySDR
from SoapySDR import Device, SOAPY_SDR_RX, SOAPY_SDR_CF32
# Using pyfftw instead of numpy to calculate fft faster
from pyfftw import interfaces
from pyfftw.interfaces import numpy_fft as fastnumpyfft
# use numpy for buffers
import numpy as np
# use pyplot for plotting
from matplotlib import pyplot as plt
# use PyQt5 for GUI
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
# use keyboard for getting menu choices from the user
import keyboard
# use time for creating delays (remove re-prints)
import time
# use the defaults from variable file
# import configfile


from threading import Thread
import time

i = 0  # For the Chart updating example

''' 
Update Chart function. You can draw chart changing this function
'''



# setup a stream (complex floats)
def setStream(sdrDevice):
    stream = sdrDevice.setupStream(SOAPY_SDR_RX, SOAPY_SDR_CF32)
    sdrDevice.activateStream(stream)  # start streaming
    return stream


# stop the stream and shutdown
def quitStream(sdrDevice, stream):
    sdrDevice.deactivateStream(stream)  # stop streaming
    sdrDevice.closeStream(stream)


def initializeHackRF(isdr, fs, f_rx, bw, gain):
    isdr.setSampleRate(SOAPY_SDR_RX, 0, fs)
    isdr.setBandwidth(SOAPY_SDR_RX, 0, bw)
    isdr.setFrequency(SOAPY_SDR_RX, 0, f_rx)
    isdr.setGain(SOAPY_SDR_RX, 0, gain)


# Get samples from sdr, but in a loop (read small number of samples every time)
def getSamples(device, stream, samplesPerScan, numOfRequestedSamples):
    samples = np.zeros(numOfRequestedSamples, dtype=np.complex64)
    iterations = int(numOfRequestedSamples / samplesPerScan)
    for j in range(iterations):
        sr = device.readStream(stream, [samples[((j-1)*samplesPerScan):]], samplesPerScan)
    # normalize the sample values
    # sr = device.readStream(stream, [samples], numOfRequestedSamples)
    samples = normArr(samples)
    return samples

# The main function. Here all the variables are setting when button clicks
def mainGUI(self):
    def update_chart(self):
        # Here is an example
        num = self.gainRX
        global i
        i += 1
        self.ax.plot([0 + num, 1 + num, 2 + num, 3 + num, 4 + num], [10, 1, 20, i, 40])
        self.canvas.draw()

    # This is the Loop which running in Thread
    def loop(self):
        while self.running:
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



    def updateSettings():
        if self.ui.gain.text() != "":
            if (0 <= int(self.ui.gain.text()) <= 90):
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
                initializeHackRF(self.sdr, self.samp_rate, self.rx_freq, self.bandwidthFilter, self.gainRX)

                if not self.threadSM.is_alive():
                    self.stream = setStream(self.sdr)
                    self.threadSM.start()

            else:
                print("rxgain bigger than 90 or smaller than 0")

    def clearPlot():
        clearPlotBool = True
        self.ax.cla()


