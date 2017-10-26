import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mpl_toolkits
import Models.LearnModels as lm
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LinearRegression

from sklearn import ensemble
from sklearn.preprocessing import scale
from sklearn.preprocessing import normalize
from sklearn.decomposition import PCA

data = pd.read_csv("..\\DataSet\\kc_house_data.csv")

train1 = data.drop(['id', 'price'],axis=1)

labels = data['price']
conv_dates = [1 if values == 2014 else 0 for values in data.date ]
data['date'] = conv_dates
train1 = data.drop(['id', 'price'],axis=1)

x_train , x_test , y_train , y_test = train_test_split(train1 , labels , test_size = 0.30,random_state =2)

"""
learningrate = 0.01
for i in range(1, 100):

    gra = lm.GradientBoostingRegressor(x_train,y_train, 400, 5, 2, learningrate, 'ls')
    print learningrate
    print "GradientBoostingRegressor score= " + str(gra.score(x_test,y_test))
    learningrate +=0.01


mn_estimators = 100
for i in range(1, 10):

    gra = lm.GradientBoostingRegressor(x_train,y_train, 500, 5, 2, 0.1, 'ls')
    print mn_estimators
    print "GradientBoostingRegressor score= " + str(gra.score(x_test,y_test))
    mn_estimators +=100
"""

gra = lm.GradientBoostingRegressor(x_train, y_train, 400, 5, 2, 0.1, 'ls')
print "GradientBoostingRegressor score= " + str(gra.score(x_test, y_test))

""""
y_test = y_test[:5]
x_test = x_test[:5]
"""
predicted = gra.predict(x_test)


for i in range(0, len(x_test)):
    print " Predicted = " + str(predicted[i]) + " Value = " + str(y_test.values[i]) + " delta = " + str( (y_test.values[i] - predicted[i]) * 100 / y_test.values[i] )


