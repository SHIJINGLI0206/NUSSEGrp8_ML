#----------------------- DataManager -------------------#
# This class is the interface for dataset loading,      #
# feature scaling, manipulation, reshaping etc          #

import pandas as pd

class dataManager:

    def __init__(self):
        self._format = 'csv'

    def setFormat(self, format):
        self._format = format

    def loadData(self, fileName, outputTag, percentTrain):
        self.fileName = fileName
        if self._format == 'csv':
            # load Dataset
            self.dataFrame = pd.read_csv(self.fileName)
            self.inputData = pd.read_csv(self.fileName, usecols=lambda x: x not in [outputTag])
            self.outputData = pd.read_csv(self.fileName, usecols=[outputTag])

            # Split into training and testing dataset

        elif self._format == 'json':
            print 'JSON format not supported'
        else:
            print 'No format selected'





