import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mpl_toolkits
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LinearRegression

from sklearn import ensemble
from sklearn.preprocessing import scale
from sklearn.preprocessing import normalize
from sklearn.decomposition import PCA

data = pd.read_csv("kc_house_data.csv")

train1 = data.drop(['id', 'price'],axis=1)

reg = LinearRegression()

labels = data['price']
conv_dates = [1 if values == 2014 else 0 for values in data.date ]
data['date'] = conv_dates

train1 = data.drop(['id','price'],axis=1)

x_train , x_test , y_train , y_test = train_test_split(train1 , labels , test_size = 0.3,random_state =2)

clf = ensemble.GradientBoostingRegressor(n_estimators = 400, max_depth = 5, min_samples_split = 2, learning_rate = 0.1, loss = 'ls')
clf.fit(x_train, y_train)
print clf.score(x_test,y_test)


# test Result #

y_test = y_test[:5]
x_test = x_test[:5]
print "price!!!!!"
print y_test
print "predictprice!!!!!"
print clf.predict(x_test)


