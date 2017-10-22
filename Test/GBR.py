import numpy as np
import pandas as pd
import random

columnNames = ['id', 'date', 'price', 'bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'floors', 'waterfront',
               'view', 'condition', 'grade', 'sqft_above', 'sqft_basement', 'yr_built', 'yr_renovated', 'zipcode',
               'lat', 'long', 'sqft_living15', 'sqft_lot15']

df = pd.read_csv('kc_house_data.csv', skiprows=1, names=columnNames)

# Now we have to split the datasets into training and validation. The training
# data will be used to generate the trees that will constitute the final
# averaged model.

X = df.loc[:, df.columns != 'price']
Y = df['price']
rows = random.sample(list(df.index), int(len(df) * .80))
x_train, y_train = X.ix[rows], Y.ix[rows]
x_test, y_test = X.drop(rows), Y.drop(rows)

# We then fit a Gradient Tree Boosting model to the data using the
# `scikit-learn <http://scikit-learn.org/stable/>`_ package. We will use 500 trees
# with each tree having a depth of 6 levels. In order to get results similar to
# those in the book we also use the `Huber loss function <http://en.wikipedia.org/wiki/Huber_loss_function>`_ .

from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import GradientBoostingRegressor

params = {'n_estimators': 500, 'max_depth': 6,
          'learning_rate': 0.1, 'loss': 'huber', 'alpha': 0.95}
clf = GradientBoostingRegressor(**params).fit(x_train, y_train)

# For me, the Mean Squared Error wasn't much informative and used instead the
# :math:`R^2` **coefficient of determination**. This measure is a number
# indicating how well a variable is able to predict the other. Numbers close to
# 0 means poor prediction and numbers close to 1 means perfect prediction. In the
# book, they claim a 0.84 against a 0.86 reported in the paper that created the
# dataset using a highly tuned algorithm. I'm getting a good 0.83 without much
# tunning of the parameters so it's a good out of the box technique.

mse = mean_squared_error(y_test, clf.predict(x_test))
r2 = r2_score(y_test, clf.predict(x_test))

print("MSE: %.4f" % mse)
print("R2: %.4f" % r2)

# Let's plot how does it behave the training and testing error

import matplotlib.pyplot as plt

# compute test set deviance
test_score = np.zeros((params['n_estimators'],), dtype=np.float64)

for i, y_pred in enumerate(clf.staged_predict(x_test)):
    test_score[i] = clf.loss_(y_test, y_pred)

plt.figure(figsize=(12, 6))
plt.subplot(1, 1, 1)
plt.title('Deviance')
plt.plot(np.arange(params['n_estimators']) + 1, clf.train_score_, 'b-',
         label='Training Set Deviance')
plt.plot(np.arange(params['n_estimators']) + 1, test_score, 'r-',
         label='Test Set Deviance')
plt.legend(loc='upper right')
plt.xlabel('Boosting Iterations')
plt.ylabel('Deviance')

# As you can see in the previous graph, although the train error keeps going
# down as we add more trees to our model, the test error remains more or less
# constant and doesn't incur in overfitting. This is mainly due to the shrinkage
# parameter and one of the good features of this algorithm.


# When doing data mining as important as finding a good model is being able to
# interpret it, because based on that analysis and interpretation preemptive
# actions can be performed. Although base trees are easily interpretable when
# you are adding several of those trees interpretation is more difficult. You
# usually rely on some measures of the predictive power of each feature. Let's
# plot feature importance in predicting the House Value.

feature_importance = clf.feature_importances_
# make importances relative to max importance
feature_importance = 100.0 * (feature_importance / feature_importance.max())
sorted_idx = np.argsort(feature_importance)
pos = np.arange(sorted_idx.shape[0]) + .5
plt.figure(figsize=(12, 6))
plt.subplot(1, 1, 1)
plt.barh(pos, feature_importance[sorted_idx], align='center')
plt.yticks(pos, X.columns[sorted_idx])
plt.xlabel('Relative Importance')
plt.title('Variable Importance')
plt.show()

# Once variable importance has been identified we could try to investigate how
# those variables interact between them. For instance, we can plot the
# dependence of the target variable with another variable has been averaged over
# the values of the other variables not being taken into consideration. Some
# variables present a clear monotonic dependence with the target value, while
# others seem not very related to the target variable even when they ranked high
# in the previous plot. This could be signaling an interaction between variables
# that could be further studied.

from sklearn.ensemble.partial_dependence import plot_partial_dependence

fig, axs = plot_partial_dependence(clf, x_train,
                                   features=[3, 2, 7, 6],
                                   feature_names=x_train.columns,
                                   n_cols=2)

fig.show()


