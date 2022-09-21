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

# According to given user choices, show an appropriate signal
def assignAppropriateSignal(mxHldBool, mvgAvgBool, currDFT, mxHldDFT, mvgAvgDFT):
    '''According to user choice, if he chose
    Moving Average / Max Hold / Both
    The code will return the appropriate signal'''
    if mxHldBool and (not mvgAvgBool):
        # User applied Max Hold without Moving Average
        # Output would be max from the new samples and old max hold samples
        mxHldDFT = np.maximum(currDFT, mxHldDFT)
        sig = mxHldDFT
    elif (not mxHldBool) and (not mvgAvgBool):
        # User did not apply any function
        # Output would be the new dft samples
        sig = currDFT
    if mxHldBool and mvgAvgBool:
        # User applied Max Hold **AND** Moving Average
        # Output would be max from the new samples after movingAverage function and old max hold samples
        mxHldDFT = np.maximum(mvgAvgDFT, mxHldDFT)
        sig = mxHldDFT
    elif (not mxHldBool) and mvgAvgBool:
        # User applied Moving Average without Max Hold
        # Output would be the new samples after movingAverage function
        sig = mvgAvgDFT
    return sig, mxHldDFT


# Apply moving average function
def movingAverageFunc(oldDFT, currentDFT, buffer_length, ratio):
    # start index in the array of the old dft
    start_index_old_fft = buffer_length - int(buffer_length * ratio)
    # end index in the array of the new dft
    end_index_new_fft = int(buffer_length * ratio)
    # Average of 2 arrays of samples (with same samplesPerIteration length)
    currentDFT[:end_index_new_fft] = 0.5 * (oldDFT[start_index_old_fft:] + currentDFT[:end_index_new_fft])
    return currentDFT


# Normalize values in given array to be in range [-1,1]
def normArr(arr):
    if np.max(np.abs(arr)) != 0:
        arr = arr / np.max(np.abs(arr))
    return arr


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


    # This is the Loop which running in Thread
    def loop(self):
        dft = np.zeros(self.samplesPerIteration)
        dftOld = np.zeros(self.samplesPerIteration)
        dftMaxHold = np.zeros(self.samplesPerIteration)
        dftMovingAverage = np.zeros(self.samplesPerIteration)
        signal = np.zeros(self.samplesPerIteration)
        while self.running:
            # save old dft samples for later use
            dftOld = dft

            # get the samples into the buffer and normalize
            samples = getSamples(self.sdr, self.stream, self.samplesPerRead, self.samplesPerIteration)

            # Perform dft on the received samples and normalize
            dft = fastnumpyfft.fftshift(fastnumpyfft.fft(samples, self.samplesPerIteration))
            dft = normArr(dft)

            dftMovingAverage = dft
            sig = dft

            # Applying Moving Average Function
            if self.movingAverageBool:
                dftMovingAverage = movingAverageFunc(dftOld, dft, self.samplesPerIteration, self.movingAverageRatio)


            sig, dftMaxHold = assignAppropriateSignal(self.maxHoldBool, self.movingAverageBool, dft, dftMaxHold,
                                                         dftMovingAverage)
            self.signal = sig

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
                self.freqs = fastnumpyfft.fftshift(fastnumpyfft.fftfreq(self.samplesPerIteration, d=1 / self.samp_rate))
                initializeHackRF(self.sdr, self.samp_rate, self.rx_freq, self.bandwidthFilter, self.gainRX)

                if not self.threadSM.is_alive():
                    self.stream = setStream(self.sdr)
                    self.threadSM.start()

            else:
                print("rxgain bigger than 90 or smaller than 0")

    def clearPlot():
        clearPlotBool = True



