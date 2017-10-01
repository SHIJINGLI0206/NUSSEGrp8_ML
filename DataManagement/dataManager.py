#----------------------- DataManager -------------------#
# This class is the interface for dataset loading,      #
# feature scaling, manipulation, reshaping etc          #

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import Normalizer

class dataManager:

    def __init__(self):
        self._format = 'csv'

    def setFormat(self, format):
        self._format = format

    def loadData(self, fileName, listOfLabelsToDrop, outputTag, percentTrain):
        self.fileName = fileName
        if self._format == 'csv':
            # load Dataset
            self.dataFrame = pd.read_csv(self.fileName)
            temp = self.dataFrame.copy()
            #self.inputData = pd.read_csv(self.fileName, usecols=lambda x: x not in [outputTag])
            temp.drop(listOfLabelsToDrop, axis=1, inplace=True)
            self.outputData = temp[outputTag]
            #print self.outputData

            temp.drop(outputTag, axis=1, inplace=True)
            self.inputData = temp
            #print self.inputData


            # Split into training and testing dataset
            self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.inputData, self.outputData, train_size=percentTrain)

        elif self._format == 'json':
            print ('JSON format not supported')
        else:
            print ('No format selected')

    def standardizeScaling(self):
        self.scaler = StandardScaler().fit(self.X_train)  #scaler to be reapply on testing set later
        #print 'Mean\n'
        #print self.scaler.mean_
        #print 'Standard deviation\n'
        #print self.scaler.var_
        self.X_trainScaled = self.scaler.transform(self.X_train)

    def normalize(self):
        self.scaler = Normalizer().fit(self.X_train)  #scaler to be reapply on testing set later
        self.X_trainScaled = self.scaler.transform(self.X_train)





