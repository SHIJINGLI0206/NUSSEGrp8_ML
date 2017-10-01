from DataManagement.dataManager import dataManager
from Models.LearnModels import *


class dataManagerTest():
    def __init__(self):
        dt = dataManager()
        dt.loadData('..\\DataSet\\kc_house_data.csv', ['id', 'date'], 'price', 0.75)
        # print 'Training Data\n'
        # print dt.X_train
        #
        # print '\nTraining Output\n'
        # print dt.y_train
        #
        # print 'Testing Data\n'
        # print dt.X_test
        #
        # print '\nTesting Output\n'
        # print dt.y_test

        XscaledData = dt.standardizeScaling()
        # print '\n\n'
        # print 'ScaledTrainingData\n'
        # print XscaledData

        print '\n\n'
        print 'Start training data in model'
        modelA = LinearRegModel(XscaledData, dt.y_train)
        predictedY, RMSE, w0, w1 = modelA.predict(dt.standardizeScaling(dt.X_test), dt.y_test)
        score = modelA.score(dt.X_test, dt.y_test)

        print '\nPredicted prices vs Actual prices\n'
        print predictedY, dt.y_test.values
        print '\nScore'
        print score

        print("Mean squared error: %.2f" %RMSE)
        print("Intercept: %s" %w0)
        print("Coeff: %s" %w1)

        # Explained variance score: 1 is perfect prediction
        print('Variance score: %.2f' % r2_score(dt.y_test, predictedY))
if __name__ == '__main__':
    dt = dataManagerTest()