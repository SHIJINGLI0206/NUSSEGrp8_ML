from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from DataManagement.feature_ranking import FeatureRanking
from PyQt5.QtCore import QThread

class MLEngine():
    def __init__(self):
        self.feature_ranking = FeatureRanking()





if __name__ == '__main__':
    ml_engine = MLEngine()



