import SoapySDR
from SoapySDR import *  # SOAPY_SDR_ constants
import numpy as np  # use numpy for buffers
import pyfftw
from matplotlib import pyplot as plt
import keyboard


# apply initial settings to HackRF device
def initializeHackRF(fs, f_rx, bw, gain):
    sdr.setSampleRate(SOAPY_SDR_RX, 0, fs)
    sdr.setBandwidth(SOAPY_SDR_RX, 0, bw)
    sdr.setFrequency(SOAPY_SDR_RX, 0, f_rx)
    sdr.setGain(SOAPY_SDR_RX, 0, gain)


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
buff_len = 1024
RX_gain = 30

initializeHackRF(samp_rate, rx_freq, bandwidth,RX_gain)

# setup a stream (complex floats)
rxStream = sdr.setupStream(SOAPY_SDR_RX, SOAPY_SDR_CF32)
print(sdr.getStreamMTU(rxStream))
sdr.activateStream(rxStream)  # start streaming

# create a re-usable buffer for rx samples
buff = np.array([0] * buff_len, np.complex64)

# create the plot and the frequency vector
# freqs = np.fft.fftshift(np.fft.fftfreq(buff_len, d=1/samp_rate))
freqs = pyfftw.interfaces.numpy_fft.fftshift(pyfftw.interfaces.numpy_fft.fftfreq(buff_len, d=1/samp_rate))
(line, ) = plt.plot((freqs + rx_freq)/1e6, np.zeros(np.size(freqs)))
plt.xlabel("Frequency (MHz)")
plt.ylabel("RSSI")

print("Choose one from the options:\n")
print("1 - Change RX frequency\n2 - Enable Max Hold\n3 - Disable Max Hold\n4 - Clear plot\n5 - Quit\n")

dft = np.array(np.zeros(buff_len))
dftMaxHold = np.array(np.zeros(buff_len))

runBool = True
maxHoldBool = False
clearPlotBool = False

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
    if clearPlotBool:
        dftMaxHold = dft
        clearPlotBool = False
    if maxHoldBool:
        dftMaxHold = np.maximum(dft, dftMaxHold)
    else:
        dftMaxHold = dft

    # update the plot
    line.set_ydata(np.abs(dftMaxHold))
    # line.set_ydata(np.log10(np.abs(dftMaxHold)))
    line.set_xdata((freqs + rx_freq)/1e6)
    # plt.ylim(0, 1200)
    plt.gca().relim()
    plt.gca().autoscale_view()
    plt.pause(0.01)

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
        print("\nClearing plot...")
        clearPlotBool = True
    elif keyboard.is_pressed("5"):
        print("\nYou chose to quit, ending loop")
        runBool = False



# shutdown the stream
sdr.deactivateStream(rxStream)  # stop streaming
sdr.closeStream(rxStream)



