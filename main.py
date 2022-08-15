import SoapySDR
# from SoapySDR import *  # SOAPY_SDR_ constants
from SoapySDR import Device, SOAPY_SDR_RX, SOAPY_SDR_CF32, SOAPY_SDR_CS16, SOAPY_SDR_CU16
import numpy as np  # use numpy for buffers
from pyfftw import interfaces
from pyfftw.interfaces import numpy_fft as fastnumpyfft
from matplotlib import pyplot as plt
import keyboard
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys


def window():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(200, 200, 300, 300)
    win.setWindowTitle("soapySpectrum Menu")

    label = QtWidgets.QLabel(win)
    label.setText("myLabel")
    label.move(50, 50)

    win.show()


# apply initial settings to HackRF device
def initializeHackRF(fs, f_rx, bw, gain):
    sdr.setSampleRate(SOAPY_SDR_RX, 0, fs)
    sdr.setBandwidth(SOAPY_SDR_RX, 0, bw)
    sdr.setFrequency(SOAPY_SDR_RX, 0, f_rx)
    sdr.setGain(SOAPY_SDR_RX, 0, gain)


def plotUpdate(ln, sig, frequencies, rxfreq):
    ln.set_ydata(np.abs(sig))
    # ln.set_ydata(np.log10(np.abs(sig)))
    ln.set_xdata((frequencies + rxfreq)/1e6)
    # plt.ylim(0, 1200)
    plt.gca().relim()
    plt.gca().autoscale_view()
    plt.pause(0.01)


# setup a stream (complex floats)
def setStream(sdrDevice):
    stream = sdrDevice.setupStream(SOAPY_SDR_RX, SOAPY_SDR_CF32)
    print(sdr.getStreamMTU(stream))
    sdrDevice.activateStream(stream)  # start streaming
    return stream


# stop the stream and shutdown
def quitStream(sdrDevice, stream):
    sdrDevice.deactivateStream(stream)  # stop streaming
    sdrDevice.closeStream(stream)


# print the main menu for our spectrum analyzer
def printMenu():
    '''Choose one from the options:
    1 - Change RX frequency
    2 - Enable max hold
    3 - Disable max hold
    4 - Enable moving average
    5 - Disable moving average
    6 - Change moving average ratio
    7 - Clear plot
    8 - Print menu again
    9 - Quit'''


if __name__ == '__main__':
    # window()

    # enumerate devices
    results = SoapySDR.Device.enumerate()
    for result in results: print(result)

    # create device instance
    # args can be user defined or from the enumeration result
    args = dict(driver="hackrf")
    sdr = SoapySDR.Device(args)

    # query device info
    print(sdr.listAntennas(SOAPY_SDR_RX, 0))
    print(sdr.listGains(SOAPY_SDR_RX, 0))
    # freqs = sdr.getFrequencyRange(SOAPY_SDR_RX, 0)
    # for freqRange in freqs: print(freqRange)

    bandwidth = 1.75e6
    samp_rate = 4e6
    rx_freq = 315e6
    buff_len = 256
    RX_gain = 30
    movingAverageRatio = 0.125

    initializeHackRF(samp_rate, rx_freq, bandwidth, RX_gain)

    # setup a stream
    rxStream = setStream(sdr)

    # create a re-usable buffer for rx samples
    buff = np.zeros(buff_len, dtype=np.complex64)

    # create the plot and the frequency vector
    freqs = fastnumpyfft.fftshift(fastnumpyfft.fftfreq(buff_len, d=1/samp_rate))
    (line, ) = plt.plot((freqs + rx_freq)/1e6, np.zeros(np.size(freqs)))
    plt.xlabel("Frequency (MHz)")
    plt.ylabel("RSSI")

    # print menu
    print(printMenu.__doc__)

    dft = np.array(np.zeros(buff_len))
    dftMaxHold = np.array(np.zeros(buff_len))

    runBool = True
    maxHoldBool = False
    clearPlotBool = False
    movingAverageBool = False

    # receive samples
    while runBool:
        dftOld = dft
        # get the samples into the buffer
        sr = sdr.readStream(rxStream, [buff], len(buff))

        if np.max(buff) != 0:
            buff = buff / np.max(buff)
        # print(sr.ret)  # num samples or error code
        # print(sr.flags)  # flags set by receive operation
        # print(sr.timeNs)  # timestamp for receive buffer
        # print(dft)  # print the values received

        # Perform dft on the samples
        dft = fastnumpyfft.fftshift(fastnumpyfft.fft(buff, buff_len))
        dftMovingAverage = dft
        signal = dft

        if clearPlotBool:
            dftMaxHold = dft
            dftMovingAverage = dft
            clearPlotBool = False

        if movingAverageBool:
            startIndexOldDFT = buff_len - int(buff_len * movingAverageRatio)
            endIndexNewDFT = int(buff_len * movingAverageRatio)
            dftMovingAverage[:endIndexNewDFT] = 0.5 * (dftOld[startIndexOldDFT:] + dftMovingAverage[:endIndexNewDFT])

        if maxHoldBool and (not movingAverageBool):
            dftMaxHold = np.maximum(dft, dftMaxHold)
            signal = dftMaxHold
        elif (not maxHoldBool) and (not movingAverageBool):
            signal = dft
        if maxHoldBool and movingAverageBool:
            dftMaxHold = np.maximum(dftMovingAverage, dftMaxHold)
            signal = dftMaxHold
        elif (not maxHoldBool) and movingAverageBool:
            signal = dftMovingAverage

        # update the plot
        plotUpdate(line, signal, freqs, rx_freq)

        # print out the maximum value in the spectrum analyzer
        # print("Maximum received in: " + str((freqs[np.argmax(np.abs(signal))] + rx_freq) / 1e6) + " MHz")

        if keyboard.is_pressed("1"):
            rx_freq = int(float(input("\nEnter desired frequency (in MHz): ")) * 1e6)
            sdr.setFrequency(SOAPY_SDR_RX, 0, rx_freq)
            clearPlotBool = True
        elif keyboard.is_pressed("2"):
            print("\nMax Hold enabled")
            maxHoldBool = True
        elif keyboard.is_pressed("3"):
            print("\nMax Hold disabled")
            maxHoldBool = False
        elif keyboard.is_pressed("4"):
            print("\nMoving Average enabled")
            movingAverageBool = True
        elif keyboard.is_pressed("5"):
            print("\nMoving Average disabled")
            movingAverageBool = False
        elif keyboard.is_pressed("6"):
            movingAverageRatio = float(input("\nEnter desired moving average ratio (in divisions of 2): "))
        elif keyboard.is_pressed("7"):
            print("\nClearing plot...")
            clearPlotBool = True
        elif keyboard.is_pressed("8"):
            print(printMenu.__doc__)
        elif keyboard.is_pressed("9"):
            print("\nYou chose to quit, ending loop")
            runBool = False



    # shutdown the stream
    quitStream(sdr, rxStream)
