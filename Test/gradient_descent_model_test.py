from DataManagement.dataManager import dataManager
from Models.LearnModels import *
from sklearn.linear_model import *


def gradient_descent_model_test():
    dt = dataManager()
    dt.loadData('..\\DataSet\\kc_house_data.csv', ['id', 'date'], 'price', 0.75)
    X_train = dt.normalize(dt.X_train)

    y_train = dt.y_train
    X_test = dt.normalize(dt.X_test)

    y_test = dt.y_test
    print('\n\n')
    print('Start training data in SGD regression model')

    model_sgd = GradientDescentModel(n_iter=1000, eta0=0.3, penalty='l1')
    model_sgd.train(X_train, y_train)
    y_pred , mse= model_sgd.predict(X_test, y_test)
    score = model_sgd.score(X_test, y_test)

    print('\nScore')
    print(score)

    print('\nPredicted prices vs Actual prices\n')
    for i in range(0, 5):
        print(" Predicted = " + str(y_pred[i]) + " Value = " + str(dt.y_test.values[i]) + " Difference[%] = " + str(
            (dt.y_test.values[i] - y_pred[i]) * 100 / dt.y_test.values[i]))



if __name__ == '__main__':
    gradient_descent_model_test()