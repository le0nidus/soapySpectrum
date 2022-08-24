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


# update the plot with new data - one way
def plotUpdateOne(ln, sig, frequencies, rxfreq, lgSclBool):
    ln.set_xdata((frequencies + rxfreq)/1e6)  # update the data on x axis (if user changed frequency)
    if lgSclBool:
        ln.set_ydata(np.log10(np.abs(sig)))
    else:
        ln.set_ydata(np.abs(sig)) # update the data on y axis
    # plt.ylim(0, 1200)
    plt.gca().relim()
    plt.gca().autoscale_view()
    plt.pause(0.01)


# update the plot with new data - second way
def plotUpdateTwo(ifig, ln, ibg, sig, frequencies, rxfreq, iax, lgSclBool):
    ln.set_xdata((frequencies + rxfreq)/1e6)  # update the data on x axis (if user changed frequency)
    if lgSclBool:
        ln.set_ydata(np.log10(np.abs(sig)))
    else:
        ln.set_ydata(np.abs(sig)) # update the data on y axis
    ifig.canvas.restore_region(ibg)
    iax.draw_artist(ln)
    ifig.canvas.blit(ifig.bbox)
    ifig.canvas.flush_events()
    plt.gca().relim()
    plt.gca().autoscale_view()
    plt.pause(0.0000001)


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
    # Average of 2 arrays of samples (with same samplesPerIteration length)
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


def normArr(arr):
    if np.max(np.abs(arr)) != 0:
        arr = arr / np.max(np.abs(arr))
    return arr


def kbUsrChoice(mySDR, myRXFreq, myRXSampleRate, mvgAvgRt,
                mxHldBool, mvgAvgBool, snkLoBool, lgSclBool, chngSmpRtBool, clrPltBool, rnBool):
    if keyboard.is_pressed("1"):
        myRXSampleRate = int(float(input("\nEnter desired sample rate (in MHz): ")) * 1e6)
        mySDR.setSampleRate(SOAPY_SDR_RX, 0, myRXSampleRate)
        chngSmpRtBool = True
        clrPltBool = True
    if keyboard.is_pressed("2"):
        myRXFreq = int(float(input("\nEnter desired frequency (in MHz): ")) * 1e6)
        mySDR.setFrequency(SOAPY_SDR_RX, 0, myRXFreq)
        clrPltBool = True
    elif keyboard.is_pressed("3"):
        if mxHldBool:
            print("\nMax Hold disabled")
            mxHldBool = False
            clrPltBool = True
        else:
            print("\nMax Hold enabled")
            mxHldBool = True
        time.sleep(cancelRePrintSleepTime)
    elif keyboard.is_pressed("4"):
        if mvgAvgBool:
            print("\nMoving Average disabled")
            mvgAvgBool = False
        else:
            print("\nMoving Average enabled")
            mvgAvgBool = True
        time.sleep(cancelRePrintSleepTime)
    elif keyboard.is_pressed("5"):
        mvgAvgRt = float(input("\nEnter desired moving average ratio (in divisions of 2): "))
    elif keyboard.is_pressed("6"):
        if snkLoBool:
            print("\nSneak from LO mode disabled (not yet implemented)")
            snkLoBool = False
        else:
            print("\nSneak from LO mode enabled (not yet implemented)")
            snkLoBool = True
        time.sleep(cancelRePrintSleepTime)
    elif keyboard.is_pressed("7"):
        if logScaleBool:
            print("\nLog scale plot disabled")
            lgSclBool = False
            clrPltBool = True
        else:
            print("\nLog scale plot enabled")
            lgSclBool = True
            clrPltBool = True
        time.sleep(cancelRePrintSleepTime)
    elif keyboard.is_pressed("8"):
        print("\nClearing plot...")
        clrPltBool = True
        time.sleep(cancelRePrintSleepTime)
    elif keyboard.is_pressed("9"):
        print(printMenu.__doc__)
        time.sleep(cancelRePrintSleepTime)
    elif keyboard.is_pressed("0"):
        print("\nYou chose to quit, ending loop")
        rnBool = False
    return myRXFreq, myRXSampleRate, mySDR, mvgAvgRt,\
           chngSmpRtBool, clrPltBool, mxHldBool, mvgAvgBool, rnBool, lgSclBool, snkLoBool



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


def sneakFromLOFunc(dft):
    return dft


def getSamples(device, stream, samplesPerScan, numOfRequestedSamples):
    samples = np.zeros(numOfRequestedSamples, dtype=np.complex64)
    iterations = int(numOfRequestedSamples / samplesPerScan)
    for j in range(iterations):
        sr = device.readStream(stream, [samples[((j-1)*samplesPerScan):]], samplesPerScan)
        # time.sleep(0.005)
    # normalize the sample values
    samples = normArr(samples)
    return device, stream, samples

# print the main menu for our spectrum analyzer
def printMenu():
    '''Choose one from the options:
    1 - Change sample rate
    2 - Change RX frequency
    3 - Enable/Disable max hold
    4 - Enable/Disable moving average
    5 - Change moving average ratio
    6 - Sneak from LO mode
    7 - Change plot to dB scale
    8 - Clear plot
    9 - Print menu again
    0 - Quit'''


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
    samplesPerIteration = configfile.SAMPLES_PER_ITERATION
    samplesPerRead = configfile.SAMPLES_PER_READ
    RX_gain = configfile.RX_GAIN
    movingAverageRatio = configfile.MOVING_AVERAGE_RATIO

    runBool = configfile.BOOL_RUN
    maxHoldBool = configfile.BOOL_MAX_HOLD
    clearPlotBool = configfile.BOOL_CLEAR_PLOT
    movingAverageBool = configfile.BOOL_MOOVING_AVERAGE
    logScaleBool = configfile.BOOL_LOG_SCALE
    sneakLOBool = configfile.BOOL_SNEAK_FROM_LO
    changeSampleRateBool = configfile.BOOL_CHANGE_SAMPLE_RATE

    #in keyboard is_pressed it re-prints if the function won't sleep
    cancelRePrintSleepTime = configfile.CANCEL_REPRINT_SLEEP_TIME

    initializeHackRF(samp_rate, rx_freq, bandwidth, RX_gain)

    # setup a stream
    rxStream = setStream(sdr)

    # create the frequency vector, it depends on samplesPerIteration and samp_rate
    freqs = fastnumpyfft.fftshift(fastnumpyfft.fftfreq(samplesPerIteration, d=1/samp_rate))

    # initiate the plot

    # one way of plotting and updating
    (line, ) = plt.plot((freqs + rx_freq)/1e6, np.zeros(np.size(freqs)))

    # # second way of plotting
    # fig, ax = plt.subplots()
    # (line,) = ax.plot((freqs + rx_freq) / 1e6, np.zeros(np.size(freqs)), animated=True)
    # plt.show(block=False)
    # plt.pause(0.00001)
    # bg = fig.canvas.copy_from_bbox(fig.bbox)
    # ax.draw_artist(line)
    # fig.canvas.blit(fig.bbox)

    plt.xlabel("Frequency (MHz)")
    plt.ylabel("RSSI")

    # print menu
    print(printMenu.__doc__)

    dft = np.zeros(samplesPerIteration)
    dftMaxHold = np.zeros(samplesPerIteration)

    # receive samples
    while runBool:
        # save old dft samples for later use
        dftOld = dft

        # get the samples into the buffer and normalize
        sdr, rxStream, samples = getSamples(sdr, rxStream, samplesPerRead, samplesPerIteration)

        # print(sr.ret)  # num samples or error code
        # print(sr.flags)  # flags set by receive operation
        # print(sr.timeNs)  # timestamp for receive buffer

        # Perform dft on the received samples and normalize
        dft = fastnumpyfft.fftshift(fastnumpyfft.fft(samples, samplesPerIteration))
        dft = normArr(dft)

        if changeSampleRateBool:
            freqs = fastnumpyfft.fftshift(fastnumpyfft.fftfreq(samplesPerIteration, d=1 / samp_rate))
            # plotUpdateOne(line, signal, freqs, rx_freq, logScaleBool)
            changeSampleRateBool = False


        dftMovingAverage = dft
        signal = dft

        # If the user wants to clear the plot
        if clearPlotBool:
            dftMaxHold, dftMovingAverage, clearPlotBool = clearPlotFunc(dft)

        # If the user wants to sneak from LO
        if sneakLOBool:
            dftSneakedSig = sneakFromLOFunc(dft)

        # Applying Moving Average Function
        if movingAverageBool:
            dftMovingAverage = movingAverageFunc(dftOld, dft, samplesPerIteration, movingAverageRatio)



        signal, dftMaxHold = assignAppropriateSignal(maxHoldBool, movingAverageBool, dft, dftMaxHold, dftMovingAverage)

        # update the plot - one way
        plotUpdateOne(line, signal, freqs, rx_freq, logScaleBool)

        # # update the plot - second way
        # plotUpdateTwo(fig, line, bg, signal, freqs, rx_freq, ax, logScaleBool)

        # print out the maximum value in the spectrum analyzer
        # print("Maximum received in: " + str((freqs[np.argmax(np.abs(signal))] + rx_freq) / 1e6) + " MHz")
        rx_freq, samp_rate, sdr, movingAverageRatio, \
        changeSampleRateBool, clearPlotBool, maxHoldBool, movingAverageBool, runBool, logScaleBool, sneakLOBool = \
            kbUsrChoice(sdr, rx_freq, samp_rate, movingAverageRatio, maxHoldBool, movingAverageBool, sneakLOBool,
                        logScaleBool, changeSampleRateBool, clearPlotBool, runBool)


    # shutdown the stream
    quitStream(sdr, rxStream)
