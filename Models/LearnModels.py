from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score

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
        print self.regr.n_iter
        print self.regr.coef_
        print self.regr.intercept_
