'''
Evaluate sound responsiveness
'''
import allcells_test086 as allcells
from jaratoolbox import loadbehavior
from jaratoolbox import settings
from jaratoolbox import ephyscore
import os
import numpy as np
from jaratoolbox import loadopenephys
from jaratoolbox import spikesanalysis
from jaratoolbox import extraplots
import matplotlib.pyplot as plt


SAMPLING_RATE=30000.0
soundTriggerChannel = 0 # channel 0 is the sound presentation, 1 is the trial
binWidth = 0.010 # Size of each bin in histogram in seconds

timeRange = [-0.2,0.8] # In seconds. Time range for rastor plot to plot spikes (around some event onset as 0)

ephysRootDir = settings.EPHYS_PATH

experimenter = 'santiago'
paradigm = '2afc'

outputDir = '/home/billywalker/Pictures/ZVal_Plots/old/'

numOfCells = len(allcells.cellDB) #number of cells that were clustered on all sessions clustered

for cellID in range(0,numOfCells):
    oneCell = allcells.cellDB[cellID]

    subject = oneCell.animalName
    behavSession = oneCell.behavSession
    ephysSession = oneCell.ephysSession
    ephysRoot = os.path.join(ephysRootDir,subject)

    # -- Load Behavior Data --
    behaviorFilename = loadbehavior.path_to_behavior_data(subject,experimenter,paradigm,behavSession)
    bdata = loadbehavior.BehaviorData(behaviorFilename)

    # -- Load event data and convert event timestamps to ms --
    ephysDir = os.path.join(ephysRoot, ephysSession)
    eventFilename=os.path.join(ephysDir, 'all_channels.events')
    events = loadopenephys.Events(eventFilename) # Load events data
    eventTimes=np.array(events.timestamps)/SAMPLING_RATE #get array of timestamps for each event and convert to seconds by dividing by sampling rate (Hz). matches with eventID and 

    soundOnsetEvents = (events.eventID==1) & (events.eventChannel==soundTriggerChannel)

    # -- Load Spike Data From Certain Cluster --
    spkData = ephyscore.CellData(oneCell)
    spkTimeStamps = spkData.spikes.timestamps

    eventOnsetTimes = eventTimes[soundOnsetEvents]
    
    possibleFreq = np.unique(bdata['targetFrequency'])
    Freq = possibleFreq[1]
    oneFreqTrials = bdata['targetFrequency'] == Freq

    oneFreqEventOnsetTimes = eventOnsetTimes[oneFreqTrials] #Choose only the trials with this frequency


    (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
        spikesanalysis.eventlocked_spiketimes(spkTimeStamps,oneFreqEventOnsetTimes,timeRange)

    plt.clf()
    ax1=plt.subplot(2,1,1)
    plt.plot(spikeTimesFromEventOnset,trialIndexForEachSpike,'.')
    #plt.show()

    # -- Calculate sound responsiveness --

    baseRange = [-0.050,-0.025]              # Baseline range (in seconds)
    rangeLength = np.diff(baseRange)         # Time-bin size
    binEdges = np.arange(-8,24)*rangeLength  # Edges of bins to calculate response (in seconds)

    #baseRange = [-0.1, 0]              # Baseline range (in seconds)
    #binEdges = [-0.1,0, 0.1, 0.2]
    [zStat,pValue,maxZ] = spikesanalysis.response_score(spikeTimesFromEventOnset,indexLimitsEachTrial,baseRange,binEdges)

    print 'Max absolute z-score: {0}'.format(maxZ)

    ax2=plt.subplot(2,1,2,sharex=ax1)
    plt.axhline(0,ls='-',color='0.5')
    plt.axhline(+3,ls='--',color='0.5')
    plt.axhline(-3,ls='--',color='0.5')
    plt.step(binEdges[:-1],zStat,where='post',lw=2)
    plt.ylabel('z-score')
    plt.xlabel('time (sec)')
    #plt.show()

    nameFreq = str(Freq)
    tetrodeClusterName = 'T'+str(oneCell.tetrode)+'c'+str(oneCell.cluster)
    plt.gcf().set_size_inches((8.5,11))
    figformat = 'png'
    filename = 'ZVal_%s_%s_%s_%s.%s'%(subject,behavSession,tetrodeClusterName,nameFreq,figformat)
    fulloutputDir = outputDir+subject+'/'
    fullFileName = os.path.join(fulloutputDir,filename)

    directory = os.path.dirname(fulloutputDir)
    if not os.path.exists(directory):
        os.makedirs(directory)
    print 'saving figure to %s'%fullFileName
    plt.gcf().savefig(fullFileName,format=figformat)
