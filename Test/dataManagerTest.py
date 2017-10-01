from DataManagement.dataManager import dataManager

class dataManagerTest():
    def __init__(self):
        dt = dataManager()
        dt.loadData('..\\DataSet\\kc_house_data_Reduced.csv', ['id', 'date'], 'price', 0.75)
        print ('Training Data\n')
        print (dt.X_train)

        print ('\nTraining Output\n')
        print (dt.y_train)

        print ('Testing Data\n')
        print (dt.X_test)

        print ('\nTesting Output\n')
        print (dt.y_test)

        dt.standardizeScaling()
        print ('\n\n')
        print ('ScaledTrainingData\n')
        print (dt.X_trainScaled)
if __name__ == '__main__':
    dt = dataManagerTest()