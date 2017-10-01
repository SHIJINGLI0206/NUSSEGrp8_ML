from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from datetime import datetime

class LinearRegModel:

    def __init__(self, X, y):
        self.regr = linear_model.LinearRegression()
        self.regr.fit(X,y.as_matrix())

    def predict(self, X, yTrue):
        yPredicted = self.regr.predict(X)
        RMSE = mean_squared_error(yTrue, yPredicted)**0.5
        return yPredicted, RMSE, self.regr.intercept_, self.regr.coef_

    def score(self, X, y):
        return self.regr.score(X, y.as_matrix())


class GradientDescentModel:
    def __init__(self, X, y, coef_init=None, intercept_init=None):
        self.regr = linear_model.SGDRegressor(n_iter=1000, eta0=0.003)
        self.regr.fit(X,y, coef_init, intercept_init)

    def predict(self, X):
        #return predicted values
        return self.regr.predict(X)

    def score(self, X, y):
        return self.regr.score(X, y)

    def toString(self):
        print (self.regr.n_iter)
        print (self.regr.coef_)
        print (self.regr.intercept_)


class LogRegModel:
    def __init__(self, x_train, y_train, x_test, y_test):
        self.x_train = x_train
        self.y_train = y_train.as_matrix()
        self.x_test = x_test
        self.y_test = y_test.as_matrix()

        self.log_reg = linear_model.LogisticRegression(C=1e6)

    def train(self):
        t_curr = str(datetime.now())
        print('\nLogistic Regression Start Training: %s' % t_curr)
        self.log_reg.fit(self.x_train, self.y_train)
        t_curr = str(datetime.now())
        print('\nLogistic Regression End Training: %s ' % t_curr)


    def predict(self):
        y_pred = self.log_reg.predict(self.x_test)
        mse = mean_squared_error(self.y_test, y_pred) ** 0.5
        return y_pred, mse, self.log_reg.intercept_, self.log_reg.coef_

    def score(self):
        return self.log_reg.score(self.x_test, self.y_test)



