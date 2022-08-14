import SoapySDR
from SoapySDR import *  # SOAPY_SDR_ constants
import numpy as np  # use numpy for buffers
import pyfftw
from matplotlib import pyplot as plt
import keyboard


# apply initial settings to HackRF device
def initializeHackRF(fs, f_rx, gain):
    sdr.setSampleRate(SOAPY_SDR_RX, 0, fs)
    sdr.setFrequency(SOAPY_SDR_RX, 0, f_rx)
    sdr.setGain(SOAPY_SDR_RX, 0, gain)


def plotUpdate(ifig, ln, ibg, sig, frequencies, rxfreq, iax):
    ifig.canvas.restore_region(ibg)
    ln.set_ydata(np.abs(sig))
    ln.set_xdata((frequencies + rxfreq)/1e6)
    iax.draw_artist(ln)
    ifig.canvas.blit(ifig.bbox)
    ifig.canvas.flush_events()
    plt.gca().relim()
    plt.gca().autoscale_view()
    plt.pause(0.0000001)


def printMenu():
    print("Choose one from the options:")
    print("1 - Change RX frequency")
    print("2 - Enable max hold")
    print("3 - Disable max hold")
    print("4 - Enable moving average")
    print("5 - Disable moving average")
    print("6 - Change moving average ratio")
    print("7 - Clear plot")
    print("8 - Print menu again")
    print("9 - Quit")


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

samp_rate = 1e6
rx_freq = 315e6
buff_len = 512
RX_gain = 30
movingAverageRatio = 0.125

initializeHackRF(samp_rate, rx_freq, RX_gain)

# setup a stream (complex floats)
rxStream = sdr.setupStream(SOAPY_SDR_RX, SOAPY_SDR_CF32)
sdr.activateStream(rxStream)  # start streaming

# create a re-usable buffer for rx samples
buff = np.array([0] * buff_len, np.complex64)

# create the plot and the frequency vector
# freqs = np.fft.fftshift(np.fft.fftfreq(buff_len, d=1/samp_rate))
freqs = pyfftw.interfaces.numpy_fft.fftshift(pyfftw.interfaces.numpy_fft.fftfreq(buff_len, d=1/samp_rate))
fig, ax = plt.subplots()
(line, ) = ax.plot((freqs + rx_freq)/1e6, np.zeros(np.size(freqs)), animated=True)
plt.show(block=False)
plt.pause(0.00001)
plt.xlabel("Frequency (MHz)")
plt.ylabel("RSSI")

bg = fig.canvas.copy_from_bbox(fig.bbox)
ax.draw_artist(line)
fig.canvas.blit(fig.bbox)


# print menu
printMenu()

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
    buff = buff / np.max(buff)
    # print(sr.ret)  # num samples or error code
    # print(sr.flags)  # flags set by receive operation
    # print(sr.timeNs)  # timestamp for receive buffer
    # print(dft)  # print the values received

    # Perform dft on the samples
    # 1 - regular numpy fft
    # dft = np.fft.fftshift(np.fft.fft(buff, buff_len))
    # 2 - faster pyfftw package fft
    dft = pyfftw.interfaces.numpy_fft.fftshift(pyfftw.interfaces.numpy_fft.fft(buff, buff_len))
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
    plotUpdate(fig, line, bg, signal, freqs, rx_freq, ax)

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
        printMenu()
    elif keyboard.is_pressed("9"):
        print("\nYou chose to quit, ending loop")
        runBool = False


# shutdown the stream
sdr.deactivateStream(rxStream)  # stop streaming
sdr.closeStream(rxStream)



# temp