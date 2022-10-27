from SoapySDR import Device, SOAPY_SDR_RX, SOAPY_SDR_CF32
# use numpy for buffers
import numpy as np

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
    if numOfRequestedSamples == samplesPerScan:
        # normalize the sample values
        sr = device.readStream(stream, [samples], numOfRequestedSamples)
    else:
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
        if np.size(mxHldDFT) != np.size(currDFT):
            mxHldDFT = np.zeros(np.size(currDFT))
        sig = mxHldDFT = np.maximum(currDFT, mxHldDFT)
    elif (not mxHldBool) and (not mvgAvgBool):
        # User did not apply any function
        # Output would be the new dft samples
        sig = currDFT
    if mxHldBool and mvgAvgBool:
        # User applied Max Hold **AND** Moving Average
        # Output would be max from the new samples after movingAverage function and old max hold samples
        if np.size(mvgAvgDFT) != np.size(currDFT):
            mvgAvgDFT = np.zeros(np.size(currDFT))
        if np.size(mxHldDFT) != np.size(currDFT):
            mxHldDFT = np.zeros(np.size(currDFT))
        sig = mxHldDFT = np.maximum(mvgAvgDFT, mxHldDFT)
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


# Clear the arrays
def clearPlotFunc(newSamps):
    # clear max hold dft
    mxHldDFT = newSamps
    # clear moving average dft
    mvgAvgDFT = newSamps
    return mxHldDFT, mvgAvgDFT
