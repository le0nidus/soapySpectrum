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
    app.exec_()


# apply initial settings to HackRF device
def initializeHackRF(fs, f_rx, bw, gain):
    sdr.setSampleRate(SOAPY_SDR_RX, 0, fs)
    sdr.setBandwidth(SOAPY_SDR_RX, 0, bw)
    sdr.setFrequency(SOAPY_SDR_RX, 0, f_rx)
    sdr.setGain(SOAPY_SDR_RX, 0, gain)


#update the plot with new data
def plotUpdate(ln, sig, frequencies, rxfreq):
    ln.set_ydata(np.abs(sig)) # update the data on y axis
    # ln.set_ydata(np.log10(np.abs(sig)))
    ln.set_xdata((frequencies + rxfreq)/1e6)  # update the data on x axis (if user changed frequency)
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


# Apply moving average function
def movingAverageFunc(oldDFT, currentDFT, buffer_length, ratio):
    # start index in the array of the old dft
    start_index_old_fft = buffer_length - int(buffer_length * ratio)
    # end index in the array of the new dft
    end_index_new_fft = int(buffer_length * ratio)
    # Average of 2 arrays of samples (with same buff_len length)
    currentDFT[:end_index_new_fft] = 0.5 * (oldDFT[start_index_old_fft:] + currentDFT[:end_index_new_fft])
    return currentDFT


# Clear the arrays
def clearPlotFunc(newSamps):
    # clear max hold dft
    mxHldDFT = newSamps
    # clear moving average dft
    mvgAvgDFT = newSamps
    # stop clearing on next iteration
    clrPltBool = False
    return mxHldDFT, mvgAvgDFT, clrPltBool


def kbUsrChoice(mySDR, mxHldBool, mvgAvgBool, myRxFreq, clrPltBool, mvgAvgRt, rnBool):
    if keyboard.is_pressed("1"):
        myRxFreq = int(float(input("\nEnter desired frequency (in MHz): ")) * 1e6)
        mySDR.setFrequency(SOAPY_SDR_RX, 0, myRxFreq)
        clrPltBool = True
    elif keyboard.is_pressed("2"):
        if mxHldBool:
            print("\nMax Hold disabled")
            mxHldBool = False
        else:
            print("\nMax Hold enabled")
            mxHldBool = True
        time.sleep(cancelRePrintSleepTime)
    elif keyboard.is_pressed("3"):
        if mvgAvgBool:
            print("\nMoving Average disabled")
            mvgAvgBool = False
        else:
            print("\nMoving Average enabled")
            mvgAvgBool = True
        time.sleep(cancelRePrintSleepTime)
    elif keyboard.is_pressed("4"):
        mvgAvgRt = float(input("\nEnter desired moving average ratio (in divisions of 2): "))
    elif keyboard.is_pressed("5"):
        print("\nplot not yet implemented")
    elif keyboard.is_pressed("6"):
        print("\nClearing plot...")
        clrPltBool = True
        time.sleep(cancelRePrintSleepTime)
    elif keyboard.is_pressed("7"):
        print(printMenu.__doc__)
        time.sleep(cancelRePrintSleepTime)
    elif keyboard.is_pressed("8"):
        print("\nYou chose to quit, ending loop")
        rnBool = False
    return myRxFreq, mySDR, clrPltBool, mxHldBool, mvgAvgBool, mvgAvgRt, rnBool


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




# print the main menu for our spectrum analyzer
def printMenu():
    '''Choose one from the options:
    1 - Change RX frequency
    2 - Enable/Disable max hold
    3 - Enable/Disable moving average
    4 - Change moving average ratio
    5 - Change plot to dB scale
    6 - Clear plot
    7 - Print menu again
    8 - Quit'''


if __name__ == '__main__':
    # window()

    # show soapySDR devices available
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

    runBool = configfile.BOOL_RUN
    maxHoldBool = configfile.BOOL_MAX_HOLD
    clearPlotBool = configfile.BOOL_CLEAR_PLOT
    movingAverageBool = configfile.BOOL_MOOVING_AVERAGE

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
            dftMaxHold, dftMovingAverage,  clearPlotBool = clearPlotFunc(dft)

        # Applying Moving Average Function
        if movingAverageBool:
            dftMovingAverage = movingAverageFunc(dftOld, dftMovingAverage, buff_len, movingAverageRatio)

        signal, dftMaxHold = assignAppropriateSignal(maxHoldBool, movingAverageBool, dft, dftMaxHold, dftMovingAverage)

        # update the plot
        plotUpdate(line, signal, freqs, rx_freq)

        # print out the maximum value in the spectrum analyzer
        # print("Maximum received in: " + str((freqs[np.argmax(np.abs(signal))] + rx_freq) / 1e6) + " MHz")

        # if keyboard.is_pressed("1"):
        #     rx_freq = int(float(input("\nEnter desired frequency (in MHz): ")) * 1e6)
        #     sdr.setFrequency(SOAPY_SDR_RX, 0, rx_freq)
        #     clearPlotBool = True
        # elif keyboard.is_pressed("2"):
        #     if maxHoldBool:
        #         print("\nMax Hold disabled")
        #         maxHoldBool = False
        #     else:
        #         print("\nMax Hold enabled")
        #         maxHoldBool = True
        #     time.sleep(cancelRePrintSleepTime)
        # elif keyboard.is_pressed("3"):
        #     if movingAverageBool:
        #         print("\nMoving Average disabled")
        #         movingAverageBool = False
        #     else:
        #         print("\nMoving Average enabled")
        #         movingAverageBool = True
        #     time.sleep(cancelRePrintSleepTime)
        # elif keyboard.is_pressed("4"):
        #     movingAverageRatio = float(input("\nEnter desired moving average ratio (in divisions of 2): "))
        # elif keyboard.is_pressed("5"):
        #     print("\nplot not yet implemented")
        # elif keyboard.is_pressed("6"):
        #     print("\nClearing plot...")
        #     clearPlotBool = True
        #     time.sleep(cancelRePrintSleepTime)
        # elif keyboard.is_pressed("7"):
        #     print(printMenu.__doc__)
        #     time.sleep(cancelRePrintSleepTime)
        # elif keyboard.is_pressed("8"):
        #     print("\nYou chose to quit, ending loop")
        #     runBool = False

        rx_freq, sdr, clearPlotBool, maxHoldBool, movingAverageBool, movingAverageRatio, runBool = kbUsrChoice(sdr, maxHoldBool, movingAverageBool, rx_freq, clearPlotBool, movingAverageBool, runBool)




    # shutdown the stream
    quitStream(sdr, rxStream)
