#----------------------- DataManager -------------------#
# This class is the interface for dataset loading,      #
# feature scaling, manipulation, reshaping etc          #
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import Normalizer


class dataManager:

    def __init__(self):
        self._format = 'csv'
        self.X_train = None
        self.y_train = None
        self.X_test = None
        self.y_test = None

    def setFormat(self, format):
        self._format = format

    def categorizeMultiClass(self, data):
        self.outputData = data
        minValue = self.outputData.min()
        range = self.outputData.max() - self.outputData.min()
        numOfClasses = 10
        interval = range/numOfClasses
        self.outputData = self.outputData.sub(minValue).floordiv(interval)
        return self.outputData

    def loadPredictData(self,fileName, listOfLabelsToDrop, outputTag, percentTrain):
        self.fileName = fileName
        if self._format == 'csv':
            # load Dataset
            self.dataFrame = pd.read_csv(self.fileName)
            temp = self.dataFrame.copy()
            temp.drop(listOfLabelsToDrop, axis=1, inplace=True)
            #temp.drop(outputTag, axis=1, inplace=True)
            self.inputData = temp

            # Split into training and testing dataset
            self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.inputData, self.dataFrame[outputTag],
                                                                                    train_size=percentTrain)
        elif self._format == 'json':
            print('JSON format not supported')

    def loadRawData(self,fileName, rows):
        self.fileName = fileName
        _,ext = os.path.splitext(fileName)
        headers =[]
        list_feature= []
        if ext == '.csv':
            df = pd.read_csv(fileName,header=0)
            headers = list(df.columns.values)
            for rw in df.itertuples(index=0):
                list_feature.append(list(rw))
                rows -= 1
                if (rows<0):
                    break
        return headers, list_feature


    def loadData(self, fileName, listOfLabelsToDrop, outputTag, percentTrain):
        self.fileName = fileName
        if self._format == 'csv':
            # load Dataset
            self.dataFrame = pd.read_csv(self.fileName)
            temp = self.dataFrame.copy()

            #self.inputData = pd.read_csv(self.fileName, usecols=lambda x: x not in [outputTag])
            temp.drop(listOfLabelsToDrop, axis=1, inplace=True)

            # Categorize output into different classes
            #self.outputData = self.categorizeMultiClass(temp[outputTag])
            #print self.outputData

            self.outputData = temp[outputTag]
            temp.drop(outputTag, axis=1, inplace=True)
            self.inputData = temp
            #print self.inputData

            # Split into training and testing dataset
            self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.inputData, self.outputData, train_size=percentTrain)

        elif self._format == 'json':
            print ('JSON format not supported')
        else:
            print ('No format selected')

    def standardizeScaling(self, X=None):
        if X is None:
            self.scaler = StandardScaler().fit(self.X_train)  #scaler to be reapply on testing set later
            #print 'Mean\n'
            #print self.scaler.mean_
            #print 'Standard deviation\n'
            #print self.scaler.var_
            self.X_trainScaled = self.scaler.transform(self.X_train)
            return self.X_trainScaled
        else:
            return self.scaler.transform(X)

    def normalize(self, X=None):
        if X is None:
            self.scaler = Normalizer().fit(self.X_train)  #scaler to be reapply on testing set later
            self.X_trainScaled = self.scaler.transform(self.X_train)
            return self.X_trainScaled
        else:
            scaler = Normalizer().fit(X)
            return scaler.transform(X)




