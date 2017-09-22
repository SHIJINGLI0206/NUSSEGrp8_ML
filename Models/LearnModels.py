from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score

class LinearRegModel:

    def __init__(self, X, y):
        self.regr = linear_model.LinearRegression()
        self.regr.fit(X,y.as_matrix())

    def predict(self, X, yTrue):
        yPredicted = self.regr.predict(X)
        RMSE = mean_squared_error(yTrue, yPredicted)
        return yPredicted, RMSE, self.regr.intercept_, self.regr.coef_

    def score(self, X, y):
        return self.regr.score(X, y.as_matrix())

class AnotherLinearRegModel:

    def __init__(self, X, y):
        self.regr = linear_model.LinearRegression()
        self.regr.fit(X,y)

    def predict(self, X):
        return self.regr.predict(X) #return predicted values

    def score(self, X, y):
        return self.regr.score(X, y)

    def toString(self):
        print self.regr.get_params()
        print self.regr.coef_
        print self.regr.intercept_
