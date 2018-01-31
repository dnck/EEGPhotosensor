import os
import mne
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import mlab

def plotTrials(test=mne.io.Raw, triggerCodes=list, xlim=list, ylim=list):
    """
    Returns data structure with epoch data
    If len(triggerCodes) > 1,
        then returned data structure corresponds to the last item in trigger code list.
    Plots all trials on a single plot.
    If len(triggerCodes) > 1,
        then plots len(triggerCodes) plots.
    """
    test=test
    events = mne.find_events(test)
    triggerCodes=triggerCodes
    xlim=xlim
    ylim=ylim
    fig = plt.figure(figsize=(14, 4))
    for x in range(len(triggerCodes)):
        markerCode= str(triggerCodes[x])
        theEpochs = mne.Epochs(test, events, event_id=triggerCodes[x], tmin=0.0, tmax=1.0,  baseline=(0.0,0), picks=[1])
        #get the data from epochs
        dat0 = theEpochs.get_data()
        timePoints = dat0.shape[2]
        #
        subplotNums = [121, 122]
        #plot the data for the epochs on top of one another
        ax = plt.subplot(subplotNums[x]);
        for z in range(theEpochs.events.shape[0]):
            plt.plot(np.linspace(0, 1000, num=timePoints), dat0[z, 0, 0:])
        ax.set_xlim(xlim);
        ax.set_ylim(ylim);
        ax.set_title("All Trials - Trigger: "+markerCode, size='x-large');
        ax.set_xlabel(r'Time from trigger (ms)', size='x-large');
        if x == 0:
            ax.set_ylabel(r'Sensor Signal', size='xx-large');
    return dat0

def showAverageSensor(test=mne.io.Raw, triggerCode=10):
    events = mne.find_events(test)
    EEG = mne.Epochs(test, events, event_id=triggerCode, tmin=0.0, tmax=1.0,  baseline=(0.0,0))
    b = EEG.average()
    fig, ax = plt.subplots(1, 3, figsize=(14, 4))
    b.plot(axes=ax[0], show=False);# xlim=(-10, 200),
    b.plot(axes=ax[1], xlim=(-10, 20), show=False);#hline=[0.0], xlim=(-10, 50),
    EEG.plot_psd(ax=ax[2], fmax=500, show=False);
    for ax, title in zip(ax[:3], ['Average Sensor Signal\n Trig: '+str(triggerCode), 'Average Sensor Signal: '+str(triggerCode), 'PSD for Sensor']):
        ax.set_title(title)
    plt.show()

def plotSingleTrial(dat0=list, indexToPlot=list, xlim=list, ylim=list):
    dat0=dat0
    x = iter(indexToPlot)
    xlim=xlim
    ylim=ylim
    fig, ax = plt.subplots(1, 5, figsize=(14, 4))
    ax[0].plot(np.linspace(0,1000,2049), dat0[x.next()].reshape(2049))
    ax[0].set_xlim(xlim)
    ax[0].set_ylim(ylim)
    ax[0].set_ylabel("Sensor Signal Level")
    ax[0].set_xlabel("ms")
    ax[1].plot(np.linspace(0,1000,2049), dat0[x.next()].reshape(2049))
    ax[1].set_xlim(xlim)
    ax[1].set_ylim(ylim)
    ax[1].set_xlabel("ms")
    ax[2].plot(np.linspace(0,1000,2049), dat0[x.next()].reshape(2049))
    ax[2].set_xlim(xlim)
    ax[2].set_ylim(ylim)
    ax[2].set_xlabel("ms")
    ax[3].plot(np.linspace(0,1000,2049), dat0[x.next()].reshape(2049))
    ax[3].set_xlim(xlim)
    ax[3].set_ylim(ylim)
    ax[3].set_xlabel("ms")
    ax[4].plot(np.linspace(0,1000,2049), dat0[x.next()].reshape(2049))
    ax[4].set_xlim(xlim)
    ax[4].set_ylim(ylim)
    ax[4].set_xlabel("ms")

def plotSingleTrials(dat0=list, xlim=list, ylim=list, plotAll=True, subsetToPlot=list):
    """
    Assumes function + plotting structure of plotSingleTrial().
    Plots each trial in own plot.
    Plots five plots per row.
    """
    dat0=dat0
    xlim=xlim
    ylim=ylim
    plotAll=plotAll
    subsetToPlot=subsetToPlot
    indexSingleTrialsToPlot = np.arange(0,dat0.shape[0]+1).reshape((dat0.shape[0]+1) / 5,5)
    if plotAll == True:
        for i in range(dat0.shape[0]/5 - 1):
            plotSingleTrial(dat0=dat0, indexToPlot=indexSingleTrialsToPlot[i], xlim=xlim, ylim=ylim)
    else:
        for i in subsetToPlot:
             plotSingleTrial(dat0=dat0, indexToPlot=indexSingleTrialsToPlot[i], xlim=xlim, ylim=ylim)

def getPeak(x=list, y=list, localMax=list):
    for i in localMax:
        if np.round(y[i],2)>0:
            return x[i]
        else:
            if np.abs(np.round(y[i],2))>0:
                return x[i]
"""
def getPeak(x=list, y=list, localMax=list):
    spot = [None, None]
    for i in localMax:
        if np.round(y[i],2)>0:
            spot[0] = x[i]
    for i in localMax:
        if np.abs(np.round(y[i],2))>0:
            spot[1] = x[i]
    print spot
    if spot[0] == None:
        return spot[1]
    else:
        return spot[0]
"""

def getPeaks(dat0=list, epochN=int, msFromOnset=int):
    dat0=dat0
    sampleLenInMs = 1000/2049.
    sliceOfSample = int(msFromOnset/sampleLenInMs)

    # trial data with some peaks:
    x = np.linspace(0,sliceOfSample,sliceOfSample)
    y = dat0[epochN,0,0:sliceOfSample]

    #
    #a = np.diff(np.sign(np.diff(data))).nonzero()[0] + 1 # local min+max
    localMax = (np.diff(np.sign(np.diff(y))) < 0).nonzero()[0] + 1 # local max

    #convert x from sample rate to ms
    x=x*sampleLenInMs

    return localMax, x, y

def plotSingleTrialPeak(epochN=list, dat0=list, msFromOnset=25, xlim=list, ylim=list, plotAll=True):
    """
    dat0 must have three dimensions
    epochN is the epoch i.e. the first dimension (epochN, 0, 0:timesToConsider)
    """
    epochN = epochN
    if plotAll==True:
        fig, ax = plt.subplots(1, 5, figsize=(14, 4))

    localMax, x, y = getPeaks(dat0=dat0, epochN=epochN[0], msFromOnset=msFromOnset)
    x1=getPeak(x=x, y=y, localMax=localMax)

    if plotAll==True:
        ax[0].plot(x,y)
        ax[0].plot(x[np.where(x==x1)[0][0]], y[np.where(x==x1)[0][0]], "o", label="max")
        ax[0].set_title("Peak at: " + str(np.round(x[np.where(x==x1)[0][0]], 2 ) ))
        ax[0].set_xlabel("ms")
        ax[0].set_ylabel("sensor signal")
        ax[0].set_xlim(xlim)
        ax[0].set_ylim(ylim)

    localMax, x, y = getPeaks(dat0=dat0, epochN=epochN[1], msFromOnset=msFromOnset)
    x2=getPeak(x=x, y=y, localMax=localMax)

    if plotAll==True:
        ax[1].plot(x,y)
        ax[1].plot(x[np.where(x==x2)[0][0]], y[np.where(x==x2)[0][0]], "o", label="max")
        ax[1].set_title("Peak at: " + str(np.round(x[np.where(x==x2)[0][0]], 2 ) ))
        ax[1].set_xlabel("ms")
        ax[1].set_ylabel("sensor signal")
        ax[1].set_xlim(xlim)
        ax[1].set_ylim(ylim)

    localMax, x, y = getPeaks(dat0=dat0, epochN=epochN[2], msFromOnset=msFromOnset)
    x3=getPeak(x=x, y=y, localMax=localMax)

    if plotAll==True:
        ax[2].plot(x,y)
        ax[2].plot(x[np.where(x==x3)[0][0]], y[np.where(x==x3)[0][0]], "o", label="max")
        ax[2].set_title("Peak at: " + str(np.round(x[np.where(x==x3)[0][0]], 2 ) ))
        ax[2].set_xlabel("ms")
        ax[2].set_ylabel("sensor signal")
        ax[2].set_xlim(xlim)
        ax[2].set_ylim(ylim)

    localMax, x, y = getPeaks(dat0=dat0, epochN=epochN[3], msFromOnset=msFromOnset)
    x4=getPeak(x=x, y=y, localMax=localMax)

    if plotAll==True:
        ax[3].plot(x,y)
        ax[3].plot(x[np.where(x==x4)[0][0]], y[np.where(x==x4)[0][0]], "o", label="max")
        ax[3].set_title("Peak at: " + str(np.round(x[np.where(x==x4)[0][0]], 2 ) ))
        ax[3].set_xlabel("ms")
        ax[3].set_ylabel("sensor signal")
        ax[3].set_xlim(xlim)
        ax[3].set_ylim(ylim)

    localMax, x, y = getPeaks(dat0=dat0, epochN=epochN[4], msFromOnset=msFromOnset)
    x5=getPeak(x=x, y=y, localMax=localMax)

    if plotAll==True:
        ax[4].plot(x,y)
        ax[4].plot(x[np.where(x==x5)[0][0]], y[np.where(x==x5)[0][0]],"o", label="max")
        ax[4].set_title("Peak at: " + str(np.round(x[np.where(x==x5)[0][0]], 2 ) ))
        ax[4].set_xlabel("ms")
        ax[4].set_ylabel("sensor signal")
        ax[4].set_xlim(xlim)
        ax[4].set_ylim(ylim)

    return [x1,x2,x3,x4,x5]

def reshapeDat0(dat0=list):
    """
    this is special because we designed the code to take an multiple of 5 trials.
    essentially, we are dropping the first x amount of trials from the data, where x will make
    the shape of the epoched data a multiple of 5
    """
    dat0 = dat0
    if dat0.shape[0]%5 > 0:
        dat0 = dat0[(dat0.shape[0]%5):]
        dat0 = dat0[1:]
    return dat0

def plotSingleTrialPeaks(dat0=list, msFromOnset=25, xlim=list, ylim=list, plotAll=True):
    """
    Assumes function + plotting structure of plotSingleTrial().
    Plots each trial in own plot.
    Plots five plots per row.
    """
    dat0=dat0
    xlim=xlim
    ylim=ylim
    plotAll=plotAll
    onsetTimes=[]
    indexSingleTrialsToPlot = np.arange(0,dat0.shape[0]+1).reshape((dat0.shape[0]+1) / 5,5)
    if plotAll == True:
        for i in range(dat0.shape[0]/5):
            onsets=plotSingleTrialPeak(epochN=indexSingleTrialsToPlot[i], dat0=dat0, msFromOnset=45, xlim=xlim, ylim=ylim,  plotAll=True)
            onsetTimes.append(onsets)
    else:
        for i in range(dat0.shape[0]/5):
            onsets = plotSingleTrialPeak(indexSingleTrialsToPlot[i], dat0=dat0, msFromOnset=msFromOnset, xlim=xlim, ylim=ylim, plotAll=False)
            onsetTimes.append(onsets)
    onsetTimes=printStats(onsetTimes=onsetTimes)
    return onsetTimes

def printStats(onsetTimes=list):
    onsetTimes = [i for x in onsetTimes for i in x]
    onsetTimes = [i for i in onsetTimes if i!=None]
    onsetTimes = np.array(onsetTimes)
    print "Mean of Peak Onset: ", onsetTimes.mean(), "ms"
    print "SD of Peak Onset: ", onsetTimes.std(), "std"
    return onsetTimes

def peakHistogram(onsetTimes=list, num_bins=int):
    onsetTimes= onsetTimes
    num_bins=num_bins
    measure="ms"
    title="Peak Luminance from Trigger at 0ms"
    font_dict = {'fontsize': 20,'fontweight' : "bold"}
    fig, ax = plt.subplots(1, figsize=(10, 4))
    mu = onsetTimes.mean()  # mean of distribution
    sigma = onsetTimes.std()  # standard deviation of distribution
    n, bins, patches = ax.hist(onsetTimes, num_bins, normed=True, log=False, color="black")
    # add a 'best fit' line
    y = mlab.normpdf(bins, mu, sigma)
    ax.plot(bins, y, '--', color="red")
    ax.set_xlabel('%s' %(measure))
    ax.set_ylabel('Probability density')
    ax.set_title('Histogram and PDF \n %s: \n $\mu=%s$, $\sigma=%s$' %(title, np.round(mu,2),np.round(sigma,2)),fontdict=font_dict)
    msPerSample = 1000/2049.

def plotPeakOfAverageSignal(dat0=list, msFromOnset=int, xlim=[0, 20], ylim=[-0.5, 1.5]):
    dat0=dat0
    averageSignal = np.array([dat0[0:, 0, i].mean() for i in range(dat0.shape[2])])
    localMax, x, y = getPeaks(averageSignal.reshape(1,1,2049), epochN=0, msFromOnset=msFromOnset)
    x1=getPeak(x=x, y=y, localMax=localMax)
    plt.plot(x,y)
    plt.plot(x[np.where(x==x1)[0][0]], y[np.where(x==x1)[0][0]], "o", label="max")
    plt.xlabel("ms")
    plt.ylabel("sensor signal")
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.title("Average peak signal at: " + "\n"+ str(x1) +" ms")
