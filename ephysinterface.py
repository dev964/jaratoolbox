'''
2015-08-01 Nick Ponvert

This module will provide a frontend for plotting data during an ephys experiment

The job of the module will be to take session names, get the data, and then pass the data to the correct plotting function
'''

# from jaratest.nick.database import dataloader
# from jaratest.nick.database import dataplotter
# reload(dataplotter)
# reload(dataloader)
# import os
# from matplotlib import pyplot as plt
# import numpy as np

import imp

class EphysInterface(object):

    def __init__(self, filepath):

        self.filepath = filepath
        self.inforec = self.load_inforec()

        # self.animalName = animalName
        # self.date = date
        # self.experimenter = experimenter
        # self.defaultParadigm = defaultParadigm
        # self.defaultTetrodes=defaultTetrodes

        # self.loader = dataloader.DataLoader('online', animalName, date, experimenter, defaultParadigm)

        # self.serverUser = serverUser
        # self.serverName = serverName
        # self.serverBehavPathBase = serverBehavPathBase
        # self.experimenter = experimenter
        # self.serverBehavPath = os.path.join(self.serverBehavPathBase, self.experimenter, self.animalName)
        # self.remoteBehavLocation = '{0}@{1}:{2}'.format(self.serverUser, self.serverName, self.serverBehavPath)

    def load_inforec(self):
        #TODO: make this reload
        inforec = imp.load_source('module.name', self.filepath)
        return inforec

    #Get the behavior from jarahub
    # def get_behavior(self):
    #     transferCommand = ['rsync', '-a', '--progress', self.remoteBehavLocation, self.localBehavPath]
    #     print ' '.join(transferCommand)
    #     subprocess.call(transferCommand)

    def plot_session_raster(self, session, tetrode, cluster = None, sortArray = [], timeRange=[-0.5, 1], replace=0, ms=4, colorEachCond=None):

        self.inforec = self.load_inforec()
        print self.inforec.experiments[-1]
        pass

        #TODO: the data below should come from the inforec
        # plotTitle = self.loader.get_session_filename(session)
        # spikeData= self.loader.get_session_spikes(session, tetrode)
        # eventData = self.loader.get_session_events(session)
        # eventOnsetTimes = self.loader.get_event_onset_times(eventData)
        # spikeTimestamps=spikeData.timestamps

        if cluster:
            spikeTimestamps = spikeTimestamps[spikeData.clusters==cluster]

        if replace:
            plt.cla()
        else:
            plt.figure()

        dataplotter.plot_raster(spikeTimestamps, eventOnsetTimes, sortArray = sortArray, timeRange=timeRange, ms=ms, colorEachCond=colorEachCond)

    
    def plot_session_PSTH(self, session, tetrode, cluster = None, sortArray = [], timeRange = [-0.5, 1], replace=0, lw=3, colorEachCond=None):
        plotTitle = self.loader.get_session_filename(session)
        spikeData= self.loader.get_session_spikes(session, tetrode)
        eventData = self.loader.get_session_events(session)
        eventOnsetTimes = self.loader.get_event_onset_times(eventData)
        spikeTimestamps=spikeData.timestamps

        if cluster:
            spikeTimestamps = spikeTimestamps[spikeData.clusters==cluster]
        if replace:
            plt.cla()
        else:
            plt.figure()
        
        dataplotter.plot_psth(spikeTimestamps, eventOnsetTimes, sortArray = sortArray, timeRange=timeRange, lw=lw, colorEachCond=colorEachCond)

    def get_processed_session_data(self, session, tetrode, cluster=None):
        spikeData= self.loader.get_session_spikes(session, tetrode)
        eventData = self.loader.get_session_events(session)
        eventOnsetTimes = self.loader.get_event_onset_times(eventData)
        spikeTimestamps=spikeData.timestamps

        if cluster:
            spikeTimestamps = spikeTimestamps[spikeData.clusters==cluster]

        return (spikeTimestamps, eventOnsetTimes)


    def plot_am_tuning(self, session, tetrode, behavSuffix, replace=0, timeRange=[-0.2, 0.8], ms=1, lw=3, colorEachCond=None):

        '''Helper fxn to plot AM modulation tuning rasters'''
        if replace:
            plt.cla()
        else:
            plt.figure()
        bdata=self.loader.get_session_behavior(behavSuffix)
        freqEachTrial = bdata['currentFreq']
        plt.subplot(211)
        self.plot_session_raster(session, tetrode, sortArray=freqEachTrial, replace=1, timeRange=timeRange, ms=ms, colorEachCond=colorEachCond)
        plt.subplot(212)
        self.plot_session_PSTH(session, tetrode, sortArray=freqEachTrial, replace=1, timeRange=timeRange, lw=lw, colorEachCond=colorEachCond)
        #plt.show()
        
    def plot_am_freq_tuning(self, freqsession, amsession, freqBehavSuffix, amBehavSuffix, tetrode, freqTimeRange = [-0.1, 0.3], amTimeRange = [-0.2, 0.8], colorEachCond=None, replace=1, ms=1, lw=3):
        '''Fxn to easier assess both characteristic frequency and best AM rate
        
        Takes as input two separate behaviour files and sessions (freq tuning and am tuning)'''
        if replace:
            plt.cla()
        else:
            plt.figure()
        bdata =self.loader.get_session_behavior(freqBehavSuffix)
        freqEachTrial = bdata['currentFreq']
        bdata2=self.loader.get_session_behavior(amBehavSuffix)
        rateEachTrial = bdata2['currentFreq']
        plt.subplot(221)
        self.plot_session_raster(amsession, tetrode, sortArray=rateEachTrial, replace=1, timeRange=amTimeRange, ms=ms, colorEachCond=colorEachCond)
        plt.xlabel('Time from event onset (sec)')
        plt.ylabel('Modulation rate (Hz)')
        plt.subplot(223)
        self.plot_session_PSTH(amsession, tetrode, sortArray=rateEachTrial, replace=1, timeRange=amTimeRange, lw=lw, colorEachCond=colorEachCond)
        plt.xlabel('Time from event onset (sec)')
        plt.ylabel('Firing rate (Hz)')
        plt.subplot(222)
        self.plot_session_raster(freqsession, tetrode, sortArray=freqEachTrial, replace=1, timeRange=freqTimeRange, ms=ms)
        plt.xlabel('Time from event onset (sec)')
        plt.ylabel('Frequency (Hz)')
        plt.subplot(224)
        self.plot_session_freq_tuning(freqsession, tetrode, sortArray=freqEachTrial, replace=1, timeRange=[0, 0.1])
        plt.xlabel('Frequency (kHz)')
        plt.ylabel('Average number of spikes in range [0, 0.1]')
        plt.suptitle('TT{}'.format(tetrode))

    def plot_session_freq_tuning(self, session, tetrode, sortArray=[], replace=0, timeRange=[0,0.1]):
        if replace:
            plt.cla()
        else:
            plt.figure()
        eventData = self.loader.get_session_events(session)
        eventOnsetTimes = self.loader.get_event_onset_times(eventData)
        plotTitle = self.loader.get_session_filename(session)
        freqEachTrial = sortArray
        freqLabels = ["%.1f"%freq for freq in np.unique(freqEachTrial)/1000]
        spikeData = self.loader.get_session_spikes(session, tetrode)
        spikeTimestamps = spikeData.timestamps
        dataplotter.one_axis_tc_or_rlf(spikeTimestamps, eventOnsetTimes, freqEachTrial, timeRange=timeRange)
        ax = plt.gca()
        ax.set_xticks(range(len(freqLabels)))
        ax.set_xticklabels(freqLabels, rotation='vertical')
    
    def plot_array_freq_tuning(self, session, behavSuffix, replace=0, tetrodes=None, timeRange=[0, 0.1]):

        if not tetrodes:
            tetrodes=self.defaultTetrodes

        numTetrodes = len(tetrodes)
        eventData = self.loader.get_session_events(session)
        eventOnsetTimes = self.loader.get_event_onset_times(eventData)
        plotTitle = self.loader.get_session_filename(session)
        bdata=self.loader.get_session_behavior(behavSuffix)
        freqEachTrial = bdata['currentFreq']
        freqLabels = ["%.1f"%freq for freq in np.unique(freqEachTrial)/1000]

        if replace:
            fig = plt.gcf()
            plt.clf()
        else:
            fig = plt.figure()


        for ind , tetrode in enumerate(tetrodes):

            spikeData = self.loader.get_session_spikes(session, tetrode)

            if ind == 0:
                ax = fig.add_subplot(numTetrodes,1,ind+1)
            else:
                ax = fig.add_subplot(numTetrodes,1,ind+1, sharex = fig.axes[0], sharey = fig.axes[0])

            spikeTimestamps = spikeData.timestamps
            dataplotter.one_axis_tc_or_rlf(spikeTimestamps, eventOnsetTimes, freqEachTrial, timeRange=timeRange)

            ax.set_xticks(range(len(freqLabels)))

            if ind == numTetrodes-1:
                ax.set_xticklabels(freqLabels, rotation='vertical')
                plt.xlabel('Frequency (kHz)')
            else:
                plt.setp(ax.get_xticklabels(), visible=False)


            plt.ylabel('TT {}'.format(tetrode))


        plt.figtext(0.05, 0.5, 'Average number of spikes in range {}'.format(timeRange), rotation='vertical', va='center', ha='center')
        plt.show()



    def plot_array_raster(self, session, replace=0, sortArray=[], timeRange = [-0.5, 1], tetrodes=None, ms=4, electrodeName='Tetrode'):
        '''
        This is the much-improved version of a function to plot a raster for each tetrode. All rasters
        will be plotted using standardized plotting code, and we will simply call the functions.
        In this case, we get the event data once, and then loop through the tetrodes, getting the
        spike data and calling the plotting code for each tetrode.
        '''
        if not tetrodes:
            tetrodes=self.defaultTetrodes
        numTetrodes = len(tetrodes)
        eventData = self.loader.get_session_events(session)
        eventOnsetTimes = self.loader.get_event_onset_times(eventData)
        plotTitle = self.loader.get_session_filename(session)
        if replace:
            fig = plt.gcf()
            plt.clf()
        else:
            fig = plt.figure()
        for ind , tetrode in enumerate(tetrodes):
            spikeData = self.loader.get_session_spikes(session, tetrode, electrodeName=electrodeName)
            if ind == 0:
                ax = fig.add_subplot(numTetrodes,1,ind+1)
            else:
                ax = fig.add_subplot(numTetrodes,1,ind+1, sharex = fig.axes[0], sharey = fig.axes[0])
            spikeTimestamps = spikeData.timestamps
            dataplotter.plot_raster(spikeTimestamps, eventOnsetTimes, sortArray=sortArray, ms=ms, timeRange = timeRange)
            if ind == 0:
                plt.title(plotTitle)
            plt.ylabel('TT {}'.format(tetrode))
        plt.xlabel('time (sec)')
        plt.show()

    def plot_sorted_tuning_raster(self, session, tetrode, behavSuffix, cluster = None, replace=0, timeRange = [-0.5, 1], ms = 1):
        '''
        Plot the tuning of a tetrode as a sorted tuning raster
        '''
        bdata = self.loader.get_session_behavior(behavSuffix)
        plotTitle = self.loader.get_session_filename(session)
        eventData = self.loader.get_session_events(session)
        spikeData = self.loader.get_session_spikes(session, tetrode, cluster)

        eventOnsetTimes = self.loader.get_event_onset_times(eventData)
        spikeTimestamps=spikeData.timestamps

        freqEachTrial = bdata['currentFreq']
        intensityEachTrial = bdata['currentIntensity']

        possibleFreq = np.unique(freqEachTrial)
        possibleIntensity = np.unique(intensityEachTrial)
        freqLabels = ['{0:.1f}'.format(freq/1000.0) for freq in possibleFreq]
        intensityLabels = ['{:.0f} dB'.format(intensity) for intensity in possibleIntensity]
        xLabel="Time from sound onset (sec)"

        dataplotter.two_axis_sorted_raster(spikeTimestamps,
                                           eventOnsetTimes,
                                           freqEachTrial,
                                           intensityEachTrial,
                                           freqLabels,
                                           intensityLabels,
                                           xLabel,
                                           plotTitle,
                                           flipFirstAxis=False,
                                           flipSecondAxis=True,
                                           timeRange=timeRange,
                                           ms=ms)

    def plot_two_axis_sorted_raster(self, session, tetrode, firstSortArray, secondSortArray, cluster = None, replace=0, timeRange = [-0.5, 1], ms = 1, firstLabels=None, secondLabels=None, yLabel=None, plotTitle=None):
        '''
        Plot rasters sorted by 2 arrays
        '''
        if not plotTitle:
            plotTitle = self.loader.get_session_filename(session)

        eventData = self.loader.get_session_events(session)
        spikeData = self.loader.get_session_spikes(session, tetrode, cluster=cluster)

        eventOnsetTimes = self.loader.get_event_onset_times(eventData)
        spikeTimestamps=spikeData.timestamps

        if not firstLabels:
            possibleFirst = np.unique(firstSortArray)
            firstLabels = ['{}'.format(val) for val in possibleFirst]
            # firstLabels = ['{0:.1f}'.format(val) for val in possibleFirst]

        if not secondLabels:
            possibleSecond = np.unique(secondSortArray)
            secondLabels = ['{}'.format(val) for val in possibleSecond]
            # secondLabels = ['{:.0f} dB'.format(val) for val in possibleSecond]

        xLabel="Time from sound onset (sec)"

        if replace:
            fig = plt.gcf()
            plt.clf()
        else:
            fig = plt.figure()

        dataplotter.two_axis_sorted_raster(spikeTimestamps,
                                           eventOnsetTimes,
                                           firstSortArray,
                                           secondSortArray,
                                           firstLabels,
                                           secondLabels,
                                           xLabel,
                                           yLabel,
                                           plotTitle,
                                           flipFirstAxis=False,
                                           flipSecondAxis=True,
                                           timeRange=timeRange,
                                           ms=ms)

        plt.show()

    #Relies on external TC heatmap plotting functions
    def plot_session_tc_heatmap(self, session, tetrode, behavSuffix, replace=True, timeRange=[0, 0.1]):
        bdata = self.loader.get_session_behavior(behavSuffix)
        plotTitle = self.loader.get_session_filename(session)
        eventData = self.loader.get_session_events(session)
        spikeData = self.loader.get_session_spikes(session, tetrode)

        spikeTimestamps = spikeData.timestamps

        eventOnsetTimes = self.loader.get_event_onset_times(eventData)

        freqEachTrial = bdata['currentFreq']
        intensityEachTrial = bdata['currentIntensity']

        possibleFreq = np.unique(freqEachTrial)
        possibleIntensity = np.unique(intensityEachTrial)

        if replace:
            fig = plt.gcf()
            plt.clf()
        else:
            fig = plt.figure()


        xlabel='Frequency (kHz)'
        ylabel='Intensity (dB SPL)'

        freqLabels = ["%.1f" % freq for freq in possibleFreq/1000.0] #FIXME: This should be outside this function
        intenLabels = ['{}'.format(inten) for inten in possibleIntensity]

        dataplotter.two_axis_heatmap(spikeTimestamps,
                                     eventOnsetTimes,
                                     intensityEachTrial,
                                     freqEachTrial,
                                     intenLabels,
                                     freqLabels,
                                     xlabel,
                                     ylabel,
                                     plotTitle,
                                     flipFirstAxis=True,
                                     flipSecondAxis=False,
                                     timeRange=timeRange)

        plt.show()


    #Relies on module for clustering multiple sessions
    #Also relies on methods for plotting rasters and cluster waveforms
    def cluster_session(self, session, tetrode):
        from jaratoolbox import spikesorting

        print 'Clustering tetrode {}'.format(tetrode)
        sessionString = self.loader.get_session_filename(session)
        oneTT = spikesorting.TetrodeToCluster(self.animalName, sessionString, tetrode)
        oneTT.load_waveforms()
        oneTT.create_fet_files()
        oneTT.run_clustering()
        oneTT.save_report()

    def cluster_array(self, session, tetrodes=[1, 2, 3, 4, 5, 6, 7, 8]):
        for tetrode in tetrodes:
            self.cluster_session(session, tetrode)

    def flip_cluster_tuning(self, session, behavSuffix, tetrode, rasterRange=[-0.5, 1]):

        from jaratoolbox import extraplots

        sessions = []
        tetrodes = []
        behavSuffixs = []
        clusters = []

        bdata = self.loader.get_session_behavior(behavSuffix)
        currentFreq = bdata['currentFreq']
        currentIntensity = bdata['currentIntensity']

        spikeData = self.loader.get_session_spikes(session, tetrode)
        if spikeData.clusters is None:
            self.cluster_session(session, tetrode)
            spikeData = self.loader.get_session_spikes(session, tetrode)

        possibleClusters = np.unique(spikeData.clusters)

        for cluster in possibleClusters:
            sessions.append(session)
            tetrodes.append(tetrode)
            behavSuffixs.append(behavSuffix)
            clusters.append(cluster)

        dataList = zip(sessions, tetrodes, behavSuffixs, clusters)
        flipper = extraplots.FlipThrough(self.plot_sorted_tuning_raster, dataList)
        return flipper

    # def _cluster_tuning(self, session, tetrode, behavSuffix, cluster):

    #     #session, tetrode, behavSuffix, cluster = dataTuple
    #     self.plot_sorted_tuning_raster(session, tetrode, behavSuffix, cluster)

    def flip_tetrode_tuning(self, session, behavSuffix, tetrodes=None , rasterRange=[-0.5, 1], tcRange=[0, 0.1]):

        if not tetrodes:
            tetrodes=self.defaultTetrodes

        plotTitle = self.loader.get_session_filename(session)

        spikesList=[]
        eventsList=[]
        freqList=[]
        rasterRangeList=[]
        tcRangeList=[]

        bdata = self.loader.get_session_behavior(behavSuffix)
        freqEachTrial = bdata['currentFreq']
        eventData = self.loader.get_session_events(session)
        eventOnsetTimes = self.loader.get_event_onset_times(eventData)

        for tetrode in tetrodes:
            spikeData = self.loader.get_session_spikes(session, tetrode)
            spikeTimestamps = spikeData.timestamps

            spikesList.append(spikeTimestamps)
            eventsList.append(eventOnsetTimes)
            freqList.append(freqEachTrial)
            rasterRangeList.append(rasterRange)
            tcRangeList.append(tcRange)

        dataList = zip(sessions, tetrodes, behavSuffixs, clusters)
        flipper = extraplots.FlipThrough(self.plot_sorted_tuning_raster, dataList)
        return flipper
        
    def flip_freq_am_tuning(self, freqsession, amsession, freqBehavSuffix, amBehavSuffix, tetrodes=[1,2,3,4,5,6,7,8], freqRange = [-0.1, 0.3], amRange = [-0.2, 0.8], colorEachCond=None):
        freqsessionList=[]
        amsessionList=[]
        freqBehavSuffixList=[]
        amBehavSuffixList=[]
        tetrodeList=[]
        amRangeList=[]
        freqRangeList=[]
        colorList=[]
        
        from jaratoolbox import extraplots

        for tetrode in tetrodes:
            freqsessionList.append(freqsession)
            amsessionList.append(amsession)
            freqBehavSuffixList.append(freqBehavSuffix)
            amBehavSuffixList.append(amBehavSuffix)
            tetrodeList.append(tetrode)
            amRangeList.append(amRange)
            freqRangeList.append(freqRange)
            colorList.append(colorEachCond)

        dataList=zip(freqsessionList, amsessionList, freqBehavSuffixList, amBehavSuffixList, tetrodeList, freqRangeList, amRangeList, colorList)
        flipper=extraplots.FlipThrough(self.plot_am_freq_tuning, dataList)
        return flipper

    # @dataplotter.FlipThroughData
    @staticmethod
    def _tetrode_tuning(dataTuple):

        '''
        The data tuple must be exactly this: (spikeTimestamps, eventOnsetTimes, freqEachTrial, tetrode, rasterRange, tcRange)
        '''

        #Unpack the data tuple (Watch out - make sure things from the above method are in the right order)
        spikeTimestamps, eventOnsetTimes, freqEachTrial, tetrode, rasterRange, tcRange = dataTuple

        possibleFreq=np.unique(freqEachTrial)
        freqLabels = ['{0:.1f}'.format(freq/1000.0) for freq in possibleFreq]
        fig = plt.gcf()

        ax1=plt.subplot2grid((3, 3), (0, 0), rowspan=3, colspan=2)
        dataplotter.plot_raster(spikeTimestamps, eventOnsetTimes, sortArray = freqEachTrial, ms=1, labels=freqLabels, timeRange=rasterRange)
        plt.title("Tetrode {}".format(tetrode))
        ax1.set_ylabel('Freq (kHz)')
        ax1.set_xlabel('Time from sound onset (sec)')

        ax2=plt.subplot2grid((3, 3), (0, 2), rowspan=3, colspan=1)
        dataplotter.one_axis_tc_or_rlf(spikeTimestamps, eventOnsetTimes, freqEachTrial, timeRange=tcRange)

        ax2.set_ylabel("Avg spikes in range {}".format(tcRange))
        ax2.set_xticks(range(len(freqLabels)))
        ax2.set_xticklabels(freqLabels, rotation='vertical')
        ax2.set_xlabel('Freq (kHz)')

    def plot_LFP_tuning(self, session, channel, behavSuffix): #FIXME: Time range??

        bdata = self.loader.get_session_behavior(behavSuffix)
        plotTitle = self.loader.get_session_filename(session)
        eventData = self.loader.get_session_events(session, convertToSeconds=False)

        contData = self.loader.get_session_cont(session, channel)

        startTimestamp = contData.timestamps[0]

        eventOnsetTimes = self.loader.get_event_onset_times(eventData, diffLimit=False)

        freqEachTrial = bdata['currentFreq']
        intensityEachTrial = bdata['currentIntensity']

        possibleFreq = np.unique(freqEachTrial)
        possibleIntensity = np.unique(intensityEachTrial)

        secondsEachTrace = 0.1
        meanTraceEachSetting = np.empty((len(possibleIntensity), len(possibleFreq), secondsEachTrace*self.loader.EPHYS_SAMPLING_RATE))


        for indFreq, currentFreq in enumerate(possibleFreq):
            for indIntensity, currentIntensity in enumerate(possibleIntensity):

                #Determine which trials this setting was presented on.
                trialsThisSetting = np.flatnonzero((freqEachTrial == currentFreq) & (intensityEachTrial == currentIntensity))

                #Get the onset timestamp for each of the trials of this setting.
                timestampsThisSetting = eventOnsetTimes[trialsThisSetting]

                #Subtract the starting timestamp value to get the sample number
                sampleNumbersThisSetting = timestampsThisSetting - startTimestamp

                #Preallocate an array to store the traces for each trial on which this setting was presented.
                traces = np.empty((len(sampleNumbersThisSetting), secondsEachTrace*self.loader.EPHYS_SAMPLING_RATE))

                #Loop through all of the trials for this setting, extracting the trace after each presentation
                for indSamp, sampNumber in enumerate(sampleNumbersThisSetting):
                    trace = contData.samples[sampNumber:sampNumber + secondsEachTrace*self.loader.EPHYS_SAMPLING_RATE]
                    trace = trace - trace[0]
                    traces[indSamp, :] = trace

                #Take the mean of all of the samples for this setting, and store it according to the freq and intensity
                mean_trace = np.mean(traces, axis = 0)
                meanTraceEachSetting[indIntensity, indFreq, :] = mean_trace

        maxVoltageAllSettings = np.max(np.max(meanTraceEachSetting, axis = 2))
        minVoltageAllSettings = np.min(np.min(meanTraceEachSetting, axis = 2))

        #Plot all of the mean traces in a grid according to frequency and intensity
        for intensity in range(len(possibleIntensity)):
            #Subplot2grid plots from top to bottom, but we need to plot from bottom to top
            #on the intensity scale. So we make an array of reversed intensity indices.
            intensPlottingInds = range(len(possibleIntensity))[::-1]
            for frequency in range(len(possibleFreq)):
                plt.subplot2grid((len(possibleIntensity), len(possibleFreq)), (intensPlottingInds[intensity], frequency))
                plt.plot(meanTraceEachSetting[intensity, frequency, :], 'k-')
                plt.ylim([minVoltageAllSettings, maxVoltageAllSettings])
                plt.axis('off')

        #This function returns the location of the text labels
        #We have to mess with the ideal locations due to the geometry of the plot
        def getXlabelpoints(n):
            rawArray = np.array(range(1, n+1))/float(n+1) #The positions in a perfect (0,1) world
            diffFromCenter = rawArray - 0.6
            partialDiffFromCenter = diffFromCenter * 0.175 #Percent change has to be determined empirically
            finalArray = rawArray - partialDiffFromCenter
            return finalArray

        #Not sure yet if similar modification to the locations will be necessary.
        def getYlabelpoints(n):
            rawArray = np.array(range(1, n+1))/float(n+1) #The positions in a perfect (0,1) world
            return rawArray

        freqLabelPositions = getXlabelpoints(len(possibleFreq))
        for indp, position in enumerate(freqLabelPositions):
            plt.figtext(position, 0.075, "%.1f"% (possibleFreq[indp]/1000), ha = 'center')

        intensLabelPositions = getYlabelpoints(len(possibleIntensity))
        for indp, position in enumerate(intensLabelPositions):
            plt.figtext(0.075, position, "%d"% possibleIntensity[indp])

        plt.figtext(0.525, 0.025, "Frequency (kHz)", ha = 'center')
        plt.figtext(0.025, 0.5, "Intensity (dB SPL)", va = 'center', rotation = 'vertical')
        plt.show()
