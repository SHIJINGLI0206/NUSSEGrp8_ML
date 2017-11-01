from DataManagement.dataManager import dataManager
import numpy as np
from sklearn.svm import SVR
from Models.LearnModels import *

dt = dataManager()
dt.loadData('..\\DataSet\\kc_house_data.csv', ['id', 'date'], 'price', 0.75)
print ('\n\n')
print ('Start training data in SVR model\n')
dt.normalize()
X = dt.normalize(dt.X_test)
clf = GradientDescentModel(dt.X_trainScaled, dt.y_train)
predictedY = clf.predict(X)

print "\nGradientDescentModel score = " + str(clf.score(X, dt.y_test))
print ('\nPredicted prices vs Actual prices')
for i in range(0, len(predictedY)):
    print(" Predicted = " + str(predictedY[i]) + " Value = " + str(dt.y_test.values[i]) + " Difference[%] = " + str(
        (dt.y_test.values[i] - predictedY[i]) * 100 / dt.y_test.values[i]))


