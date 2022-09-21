# SoapySDR is the API for the hackrf
import SoapySDR
from SoapySDR import Device, SOAPY_SDR_RX, SOAPY_SDR_CF32
# Using pyfftw instead of numpy to calculate fft faster
from pyfftw import interfaces
from pyfftw.interfaces import numpy_fft as fastnumpyfft
# use numpy for buffers
import numpy as np
import functions
import sys
# use time for creating delays (remove re-prints)
import time
# use the defaults from variable file
# import configfile


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
        self.dftMaxHold, self.dftMovingAverage = functions.clearPlotFunc(self.dft)

    # This is the Loop which running in Thread
    def loop(self):
        self.dft = np.zeros(self.samplesPerIteration)
        self.dftOld = np.zeros(self.samplesPerIteration)
        self.dftMaxHold = np.zeros(self.samplesPerIteration)
        self.dftMovingAverage = np.zeros(self.samplesPerIteration)
        while self.running:
            # save old dft samples for later use
            self.dftOld = self.dft

            # get the samples into the buffer and normalize
            self.samples = functions.getSamples(self.sdr, self.stream, self.samplesPerRead, self.samplesPerIteration)

            # Perform dft on the received samples and normalize
            self.dft = fastnumpyfft.fftshift(fastnumpyfft.fft(self.samples, self.samplesPerIteration))
            self.dft = functions.normArr(self.dft)

            self.dftMovingAverage = self.dft
            sig = self.dft

            # Applying Moving Average Function
            if self.movingAverageBool:
                self.dftMovingAverage = functions.movingAverageFunc(self.dftOld, self.dft, self.samplesPerIteration, self.movingAverageRatio)


            sig, self.dftMaxHold = functions.assignAppropriateSignal(self.maxHoldBool, self.movingAverageBool, self.dft, self.dftMaxHold,
                                                         self.dftMovingAverage)
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
                functions.initializeHackRF(self.sdr, self.samp_rate, self.rx_freq, self.bandwidthFilter, self.gainRX)

                if not self.threadSM.is_alive():
                    self.stream = functions.setStream(self.sdr)
                    self.threadSM.start()

            else:
                print("rxgain bigger than 90 or smaller than 0")





