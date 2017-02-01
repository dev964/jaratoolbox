'''
List of all isolated units from one animal
'''

from jaratoolbox import celldatabase
eSession = celldatabase.EphysSessionInfo  # Shorter name to simplify code


cellDB = celldatabase.CellDatabase()


oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-04_15-41-31',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160204a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-07_15-27-13',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160207a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-11_17-18-34',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160211a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-15_15-40-25',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160215a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-17_16-15-41',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160217a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-19_10-42-16',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160219a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-22_17-55-18',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160222a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-24_17-21-23',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160224a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-25_17-13-16',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160225a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-29_15-55-06',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160229a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-03-01_14-12-01',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160301a')
cellDB.append_session(oneES)
