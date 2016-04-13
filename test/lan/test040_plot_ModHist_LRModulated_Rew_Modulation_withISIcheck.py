'''
Evaluate cells whose activity differ by leftward vs rightward movement in a given time window (0.1 to 0.2 window after 'center-out') to see whether the activity for one-sided movement(in trials with one sound frequency) is modulated by reward.

Implemented different window size.Plots number of significantly and non-significantly modulated cells from modulation index of -1 to +1. Only using good quality cells (either all_cells file only contain good quality cells or has 'oneCell.quality' indicating whether it's a good cell) that are modulated by L vs R movement. Generates modulatedCellDB (mod sig <= 0.05) excluding ISI violations.
-Lan Guo 20160413
Write to a text file the cell name, cell ID (index in allcells file), frequency modulated, and modulation index (only for the significantly modulated ones). 
Implemented 'trialLimit' constraint to exclude blocks with few trials at the end of a behav session. 
'''

from jaratoolbox import loadbehavior
from jaratoolbox import settings_2 as settings
from jaratoolbox import ephyscore
import os
import shutil
import numpy as np
from jaratoolbox import loadopenephys
from jaratoolbox import spikesanalysis
from jaratoolbox import extraplots
#from jaratoolbox import celldatabase
from jaratoolbox.test.lan.Ephys import celldatabase_quality_vlan as celldatabase
from jaratoolbox.test.lan import test022_plot2afc_given_cell_rew_change as cellplotter
import matplotlib.pyplot as plt
import sys
import importlib

binWidth = 0.020 # Size of each bin in histogram in seconds

clusNum = 12 #Number of clusters that Klustakwik speparated into
numTetrodes = 8 #Number of tetrodes

################################################################################################
##############################-----Minimum Requirements------###################################
################################################################################################
qualityList = [1,6]#[1,4,5,6,7]#range(1,10)
minZVal = 3.0
maxISIviolation = 0.02
minPValue = 0.05
################################################################################################

#######################-----Key Parameters-----#####################################################################
alignment = 'center-out'
##Get countTimeRange from system arguments
if sys.argv[1]=='0':
    countTimeRange = [int(sys.argv[1]),float(sys.argv[2])]
elif sys.argv[2]=='0':
    countTimeRange = [float(sys.argv[1]),int(sys.argv[2])]
else:
    countTimeRange = [float(sys.argv[1]),float(sys.argv[2])]
subjectList = sys.argv[3:]   
##############################################################################

for subject in subjectList:
    allcellsFileName = 'allcells_'+subject
    sys.path.append(settings.ALLCELLS_PATH)
    allcells = importlib.import_module(allcellsFileName)

    numOfCells = len(allcells.cellDB) #number of cells that were clustered on all sessions clustered

    outputDir = '/home/languo/data/ephys/'+subject+'/'

    CellInfo = celldatabase.CellInfo  #This is for creating subdatabase for responsive and modulated cells
    responsiveCellDB = celldatabase.CellDatabase()
    modulatedCellDB = celldatabase.CellDatabase()
    allCellDB= celldatabase.CellDatabase()


    ###################Choose alignment and time window to plot mod Index histogram#######################
    processedDir = os.path.join(outputDir,subject+'_stats')
    #alignment = 'center-out'
    #put here alignment choice!!choices are 'sound', 'center-out', 'side-in'.
    #countTimeRange = [-0.1,0]
    window = str(countTimeRange[0])+'to'+str(countTimeRange[1])+'sec_window_'
    nameOfmodSFile = 'modSig_'+alignment+'_'+window+subject+'.txt'
    nameOfmodIFile = 'modIndex_'+alignment+'_'+window+subject+'.txt'
    
    nameOfmovementmodSFile = 'modSig_'+'LvsR_movement_'+window+subject+'.txt'
    nameOfmovementmodIFile = 'modIndex_'+'LvsR_movement_'+window+subject+'.txt'
    
    modIFilename = os.path.join(processedDir,nameOfmodIFile)
    modSFilename = os.path.join(processedDir,nameOfmodSFile)

    movementmodIFilename = os.path.join(processedDir,nameOfmovementmodIFile)
    movementmodSFilename = os.path.join(processedDir,nameOfmovementmodSFile)

    #############################################################################

    subject = allcells.cellDB[0].animalName
    behavSession = ''

    maxZFilename = os.path.join(processedDir,'maxZVal_'+subject+'.txt')
    ISIFilename = os.path.join(processedDir,'ISI_Violations_'+subject+'.txt')
    #modIFilename = os.path.join(processedDir,'modIndex_alignedToSound_'+subject+'.txt')
    #modSFilename = os.path.join(processedDir,'modSig_alignedToSound_'+subject+'.txt')

    class nestedDict(dict):#This is for maxZDict
        def __getitem__(self, item):
            try:
                return super(nestedDict, self).__getitem__(item)
            except KeyError:
                value = self[item] = type(self)()
                return value

    maxZFile = open(maxZFilename, 'r')
    ISIFile = open(ISIFilename, 'r')
    modIFile = open(modIFilename, 'r')
    modSFile = open(modSFilename, 'r')
    movementmodIFile=open(movementmodIFilename, 'r')
    movementmodSFile=open(movementmodSFilename, 'r')

    ################################
    
    ISIDict = {}
    behavName = ''
    for line in ISIFile:
        #ehavLine = line.split(':')
        #reqLine = line.split()
        if (line.split(':')[0] == 'Behavior Session'):
            behavName = line.split(':')[1][:-1]
        else:
            ISIDict[behavName] = [float(x) for x in line.split(',')[0:-1]]
    

    modIDict = nestedDict() #stores all the modulation indices
    modSigDict = nestedDict() #stores the significance of the modulation of each cell
    movementmodIDict = {}
    movementmodSigDict = {}
    #modDirectionScoreDict = {} #stores the score of how often the direction of modulation changes
    behavName = ''
   
    for line in movementmodIFile:
        if (line.split(':')[0] == 'Behavior Session'):
            behavName = line.split(':')[1][:-1]  
        else:
            movementmodIDict[behavName] = [float(x) for x in line.split(',')[0:-1]]

    for line in movementmodSFile:
        if (line.split(':')[0] == 'Behavior Session'):
            behavName = line.split(':')[1][:-1] 
        else:
            movementmodSigDict[behavName] = [float(x) for x in line.split(',')[0:-1]]
    
    for line in modIFile:
        behavLine = line.split(':')
        freqLine = line.split()
        if (behavLine[0] == 'Behavior Session'):
            behavName = behavLine[1][:-1]
        else:
            modIDict[behavName][freqLine[0]] = [float(x) for x in freqLine[1].split(',')[0:-1]]

    for line in modSFile:
        behavLine = line.split(':')
        freqLine = line.split()
        if (behavLine[0] == 'Behavior Session'):
            behavName = behavLine[1][:-1]
        else:
            modSigDict[behavName][freqLine[0]] = [float(x) for x in freqLine[1].split(',')[0:-1]]


    allCellDict={}

    sigModIDict={}
    ISIFile.close()
    maxZFile.close()
    modIFile.close()
    modSFile.close()
    movementmodIFile.close()
    movementmodSFile.close()
    ########################CHOOSE WHICH CELLS TO PLOT################################################
    modIndexArray = []
    for cellID in range(0,numOfCells):
        oneCell = allcells.cellDB[cellID]

        subject = oneCell.animalName
        behavSession = oneCell.behavSession
        ephysSession = oneCell.ephysSession
        tetrode = oneCell.tetrode
        cluster = oneCell.cluster
        clusterQuality = oneCell.quality
        trialLimit = oneCell.trialLimit

        if clusterQuality not in qualityList:
            continue
        elif behavSession not in modIDict:
            continue
        elif behavSession not in ISIDict:
            continue
        else:
            clusterNumber = (tetrode-1)*clusNum+(cluster-1)
            
            for freq in modIDict[behavSession]:
              ######Only evaluate cells whose activity differ by leftward vs rightward movement in this time window to see whether the activity for one-sided movement is modulated by reward######
                if (movementmodSigDict[behavSession][clusterNumber]<=minPValue) and (ISIDict[behavSession][clusterNumber]<= maxISIviolation):
                    modIndexArray.append([modIDict[behavSession][freq][clusterNumber],modSigDict[behavSession][freq][clusterNumber]])
                    if oneCell not in allCellDB:
                        allCellDB.append(oneCell)
                    cellName=subject+'_'+behavSession+'_'+str(tetrode)+'_'+str(cluster)
                    
                    if (modSigDict[behavSession][freq][clusterNumber]<=minPValue):
                        modIndexThisCell=modIDict[behavSession][freq][clusterNumber]
                        sigModIDict.update({cellName:[cellID,freq,modIndexThisCell]})
                        if oneCell not in modulatedCellDB:
                            modulatedCellDB.append(oneCell)

                else:
                    continue
        
            cellNum=len(allCellDB)
            modCellNum=len(modulatedCellDB)

    ##########################THIS IS TO PLOT HISTOGRAM################################################
    modIndBinVec = np.arange(-1,1,binWidth)
    binModIndexArraySig = np.empty(len(modIndBinVec))
    binModIndexArrayNonSig = np.empty(len(modIndBinVec))
    maxMI=0
    for binInd in range(len(modIndBinVec)-1):
        binTotalSig = 0
        binTotalNonSig = 0
        for modIndSig in modIndexArray:
            if ((modIndSig[0] >= modIndBinVec[binInd]) and (modIndSig[0] < modIndBinVec[binInd+1]) and (modIndSig[1] <= minPValue)):
                binTotalSig += 1
            elif ((modIndSig[0] >= modIndBinVec[binInd]) and (modIndSig[0] < modIndBinVec[binInd+1])):
                binTotalNonSig += 1
            maxMI = max(maxMI,abs(modIndSig[0]))
        binModIndexArraySig[binInd] = binTotalSig
        binModIndexArrayNonSig[binInd] = binTotalNonSig
    binModIndexArraySig[-1] = 0  #why is this??
    binModIndexArrayNonSig[-1] = 0 #why is this??
    sigNum=int(sum(binModIndexArraySig))
    comparisonNum=len(modIndexArray)
    print 'number of comparisons: ',comparisonNum

    plt.clf() 

    plt.bar(modIndBinVec,binModIndexArraySig,width = binWidth, color = 'b')
    plt.bar(modIndBinVec,binModIndexArrayNonSig,width = binWidth, color = 'g',bottom = binModIndexArraySig)

    plt.xlim((-(maxMI+binWidth),maxMI+binWidth))
    ylim=plt.ylim()[1]
    plt.xlabel('Modulation Index')
    plt.ylabel('Number of Cells')
    plt.text(-0.5*(maxMI+binWidth),0.5*ylim,'Plotting %s comparisons, %s significantly modulated' %(comparisonNum,sigNum))
    plt.text(-0.5*(maxMI+binWidth),0.25*ylim,'%s movement-responsive cells, %s cells modulated' %(cellNum,modCellNum))
    plt.title(alignment+window+'movement-responsive modulated cells')
    
    plt.gcf().set_size_inches((8.5,11))
    figformat = 'png'
    filename = 'modIndex_movementResponsive_ISIchecked_%s_%s_%s.%s'%(alignment,window,subject,figformat)
    fulloutputDir = processedDir
    fullFileName = os.path.join(fulloutputDir,filename)

    directory = os.path.dirname(fulloutputDir)
    if not os.path.exists(directory):
        os.makedirs(directory)
    print 'saving figure to %s'%fullFileName
    plt.gcf().savefig(fullFileName,format=figformat)


    plt.show()

    ####Write all significantly modulated cells and their mod index in a text file###
    sigModIFilename='movementResponsive_sigMod_'+alignment+'_'+window+'ISIchecked'
    sigModI_file = open('%s/%s.txt' % (fulloutputDir,sigModIFilename), 'w')
    for (key,value) in sorted(sigModIDict.items()):
        sigModI_file.write('%s:' %key)
        if len(value)==3:
            sigModI_file.write('%d %s %f\n' %(value[0],value[1],value[2]))
        elif len(value)==2:
            sigModI_file.write('%d %f\n' %(value[0],value[1]))
    sigModI_file.close()


'''
####Copy plots of modulated cells to a new folder inside the stats folder and rename them
numOfModulatedCells = len(modulatedCellDB)
for cellID in range(0,numOfModulatedCells):
    oneCell = modulatedCellDB[cellID]
    
    #####make new plots######
    dstDir = processedDir+'/all_cells_SoundOnset_sig_modulated/'
    if not os.path.exists(dstDir):
        os.makedirs(dstDir)

    figname='{0}_{1}_TT{2}_c{3}_{4}'.format(oneCell.animalName,oneCell.behavSession,oneCell.tetrode,oneCell.cluster,'sound-onset')
    full_fig_path=os.path.join(dstDir, figname)
    if not os.path.exists(full_fig_path):
        cellplotter.plot_rew_change_per_cell(oneCell,trialLimit=oneCell.trialLimit,alignment='sound')
        plt.savefig(full_fig_path, format = 'png')
    
    
    figname='{0}_{1}_TT{2}_c{3}_{4}_{5}'.format(oneCell.animalName,oneCell.behavSession,oneCell.tetrode,oneCell.cluster,'sound-onset','right')
    full_fig_path=os.path.join(dstDir, figname)

    if not os.path.exists(full_fig_path):
        cellplotter.plot_rew_change_byblock_per_cell(oneCell,trialLimit=oneCell.trialLimit,alignment='sound',choiceSide='right')
        plt.savefig(full_fig_path, format = 'png')

   
    figname='{0}_{1}_TT{2}_c{3}_{4}_{5}'.format(oneCell.animalName,oneCell.behavSession,oneCell.tetrode,oneCell.cluster,'sound-onset','left')
    full_fig_path=os.path.join(dstDir, figname)
    if not os.path.exists(full_fig_path):
        cellplotter.plot_rew_change_byblock_per_cell(oneCell,trialLimit=oneCell.trialLimit,alignment='sound',choiceSide='left')
        plt.savefig(full_fig_path, format = 'png')
'''


    
