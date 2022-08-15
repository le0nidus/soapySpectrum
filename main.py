# SoapySDR is the API for the hackrf
import SoapySDR
from SoapySDR import Device, SOAPY_SDR_RX, SOAPY_SDR_CF32, SOAPY_SDR_CS16, SOAPY_SDR_CU16
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
import configfile


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

    bandwidth = configfile.BANDWIDTH
    samp_rate = configfile.SAMPLE_RATE
    rx_freq = configfile.RX_FREQ
    buff_len = configfile.BUFFER_LENGTH
    RX_gain = configfile.RX_GAIN
    movingAverageRatio = configfile.MOVING_AVERAGE_RATIO

    #in keyboard is_pressed it re-prints if the function won't sleep
    cancelRePrintSleepTime = configfile.CANCEL_REPRINT_SLEEP_TIME

    initializeHackRF(samp_rate, rx_freq, bandwidth, RX_gain)

    # setup a stream
    rxStream = setStream(sdr)

    # create a re-usable buffer for rx samples
    buff = np.zeros(buff_len, dtype=np.complex64)

    # create the frequency vector, it depends on buff_len and samp_rate
    freqs = fastnumpyfft.fftshift(fastnumpyfft.fftfreq(buff_len, d=1/samp_rate))

    # initiate the plot
    (line, ) = plt.plot((freqs + rx_freq)/1e6, np.zeros(np.size(freqs)))
    plt.xlabel("Frequency (MHz)")
    plt.ylabel("RSSI")

    # print menu
    print(printMenu.__doc__)

    dft = np.zeros(buff_len)
    dftMaxHold = np.zeros(buff_len)

    runBool = configfile.BOOL_RUN
    maxHoldBool = configfile.BOOL_MAX_HOLD
    clearPlotBool = configfile.BOOL_CLEAR_PLOT
    movingAverageBool = configfile.BOOL_MOOVING_AVERAGE

    # receive samples
    while runBool:
        # save old dft samples for later use
        dftOld = dft

        # get the samples into the buffer
        sr = sdr.readStream(rxStream, [buff], len(buff))

        # normalize the values
        if np.max(np.abs(buff)) != 0:
            buff = buff / np.max(np.abs(buff))

        # print(sr.ret)  # num samples or error code
        # print(sr.flags)  # flags set by receive operation
        # print(sr.timeNs)  # timestamp for receive buffer
        # print(dft)  # print the values received

        # Perform dft on the samples
        dft = fastnumpyfft.fftshift(fastnumpyfft.fft(buff, buff_len))
        dftMovingAverage = dft
        signal = dft

        # If the user wants to clear the plot
        if clearPlotBool:
            dftMaxHold = dft # Reset Max Hold values to current values
            dftMovingAverage = dft # Reset moving Average values to current values
            clearPlotBool = False

        # Applying Moving Average Function
        if movingAverageBool:
            # start index in the array of the old dft
            startIndexOldDFT = buff_len - int(buff_len * movingAverageRatio)
            # end index in the array of the old dft
            endIndexNewDFT = int(buff_len * movingAverageRatio)
            # Average of 2 arrays of samples (with same buff_len length)
            dftMovingAverage[:endIndexNewDFT] = 0.5 * (dftOld[startIndexOldDFT:] + dftMovingAverage[:endIndexNewDFT])

        if maxHoldBool and (not movingAverageBool):
            # User applied Max Hold without Moving Average
            # Output would be max from the new samples and old max hold samples
            dftMaxHold = np.maximum(dft, dftMaxHold)
            signal = dftMaxHold
        elif (not maxHoldBool) and (not movingAverageBool):
            # User did not apply any function
            # Output would be the new dft samples
            signal = dft
        if maxHoldBool and movingAverageBool:
            # User applied Max Hold **AND** Moving Average
            # Output would be max from the new samples after movingAverage function and old max hold samples
            dftMaxHold = np.maximum(dftMovingAverage, dftMaxHold)
            signal = dftMaxHold
        elif (not maxHoldBool) and movingAverageBool:
            # User applied Moving Average without Max Hold
            # Output would be the new samples after movingAverage function
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
            time.sleep(cancelRePrintSleepTime)
        elif keyboard.is_pressed("3"):
            print("\nMax Hold disabled")
            maxHoldBool = False
            time.sleep(cancelRePrintSleepTime)
        elif keyboard.is_pressed("4"):
            print("\nMoving Average enabled")
            movingAverageBool = True
            time.sleep(cancelRePrintSleepTime)
        elif keyboard.is_pressed("5"):
            print("\nMoving Average disabled")
            movingAverageBool = False
            time.sleep(cancelRePrintSleepTime)
        elif keyboard.is_pressed("6"):
            movingAverageRatio = float(input("\nEnter desired moving average ratio (in divisions of 2): "))
        elif keyboard.is_pressed("7"):
            print("\nClearing plot...")
            clearPlotBool = True
            time.sleep(cancelRePrintSleepTime)
        elif keyboard.is_pressed("8"):
            print(printMenu.__doc__)
            time.sleep(cancelRePrintSleepTime)
        elif keyboard.is_pressed("9"):
            print("\nYou chose to quit, ending loop")
            runBool = False



    # shutdown the stream
    quitStream(sdr, rxStream)
