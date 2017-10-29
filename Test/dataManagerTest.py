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

        #XscaledData = dt.standardizeScaling()
        # print '\n\n'
        # print 'ScaledTrainingData\n'
        # print XscaledData

        print ('\n\n')
        print ('Start training data in model (Linear Regression)')

        modelA = LinearRegModel(dt.X_train, dt.y_train)
        predictedY, RMSE, w0, w1 = modelA.predict(dt.X_test, dt.y_test)
        score = modelA.score(dt.X_test, dt.y_test)

        print ('\nScore')
        print (score)

        print ('\nPredicted prices vs Actual prices\n')
        for i in range(0, len(predictedY)):
            print(" Predicted = " + str(predictedY[i]) + " Value = " + str(dt.y_test.values[i]) + " Difference[%] = " + str(
                (dt.y_test.values[i] - predictedY[i]) * 100 / dt.y_test.values[i]))
            #print (" Predicted = " + str(predictedY[i]), dt.y_test.values[i])

        print("Mean squared error: %.2f" %RMSE)
        print("Intercept: %s" %w0)
        print("Coeff: %s" %w1)

        # Explained variance score: 1 is perfect prediction
        print('Variance score: %.2f' % r2_score(dt.y_test, predictedY))

    if 0:
        ###########################################################################
        #Test logistic regression
        ###########################################################################
        dt = dataManager()
        dt.loadData('..\\DataSet\\kc_house_data.csv', ['id', 'date'], 'price', 0.75)
        X_train = dt.normalize()
        y_train = dt.y_train
        X_test = dt.normalize(dt.X_test)
        y_test = dt.y_test
        print ('\n\n')
        print ('Start training data in logistic regression model')

        model_log = LogRegModel(X_train, y_train, X_test, y_test)
        model_log.train()
        y_pred, mse, w0, w1 = model_log.predict()
        score = model_log.score()

        print('\nPredicted prices vs Actual prices\n')
        print(y_pred, y_test.values)
        print('\nScore')
        print(score)

        print("Mean squared error: %.2f" % mse)
        print("Intercept: %s" % w0)
        print("Coeff: %s" % w1)

        # Explained variance score: 1 is perfect prediction
        print('Variance score: %.2f' % r2_score(y_test, y_pred))

if __name__ == '__main__':
    dt = dataManagerTest()