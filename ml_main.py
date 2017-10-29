import sys
import ctypes
from PyQt5 import (QtWidgets, QtGui, QtCore)
from PyQt5.QtCore import *
from PyQt5.QtWidgets import (QMainWindow, QFileDialog)
from PyQt5.QtGui import *
from PyQt5.Qt import (QWidget, QLabel,QSizePolicy,QVBoxLayout, QProgressDialog, QPixmap)
from UI.ml_ui import Ui_MainWindow
#from DataManagement.feature_ranking import FeatureRanking
from DataManagement.dataManager import *
from DataManagement.featureModel import *
import math
from Models.LearnModels import *
import numpy as np

class FeatureRankingThread(QThread):
    def __init__(self,x_train,y_train):
        QThread.__init__(self)
        self.x_train = x_train
        self.y_train = y_train
        self.feature_importance = []

    def __del__(self):
        self.quit()

    def run(self):
        # calculate feature importance use user se
        try:
            model_gbr = GradientBoostingRegressor(self.x_train, self.y_train, 400, 5, 2, 0.1, 'ls')
            self.feature_importance.clear()
            self.feature_importance = model_gbr.feature_importance()
            # make importances relative to max importance
            self.feature_importance = 100.0 * (self.feature_importance / self.feature_importance.max())
        except Exception as e:
            print('Error: ',e)

class BuildModelThread(QThread):
    def __init__(self,x_train,y_train):
        QThread.__init__(self)
        self.x_train = x_train
        self.y_train = y_train
        self.prediction_model = None

    def __del__(self):
        self.quit()
        self.wait()

    def run(self):
        #build machine learning model
        try:
            self.prediction_model = GradientBoostingRegressor(self.x_train, self.y_train, 400, 5, 2, 0.1, 'ls')
        except Exception as e:
            print('Error: ',e)

class ML(QMainWindow):
    def __init__(self, parent=None):
        super(ML,self).__init__(parent=None)
        self.init_ui()

        self.raw_features = []
        self.selected_features = []
        self.drop_features = []
        self.x_test = []
        self.y_test = []
        self.y_pred = []
        self.thread_feature_ranking = None
        self.thread_model_building = None
        self.prediction_model = None

        self.file_name = ''
        self.init_connection()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.thread_feature_ranking.exit()


    def init_ui(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('Images\\house.png'))
       # addDockWidget(Qt.RightDockWidgetArea,self.ui.dockWidget)

        # init widget size
        screen_width = ctypes.windll.user32.GetSystemMetrics(0)
        screen_height = ctypes.windll.user32.GetSystemMetrics(1)
        self.ui.dw_right.setMinimumWidth(screen_width - self.ui.dw_left.width() - 10)
        self.ui.sw_content.setMinimumWidth(screen_width - self.ui.dw_left.width() - 40)
        self.ui.sw_content.setMinimumHeight(screen_height - 200)

        # page 1 content size
        self.ui.lb_filename.setMinimumWidth(self.ui.sw_content.width() - 30)
        self.ui.view_data.setMinimumWidth(self.ui.sw_content.width() - 20)
        self.ui.view_data.setMinimumHeight(700)

        self.ui.view_feature.setMinimumHeight( self.ui.sw_content.height() - self.ui.view_data.height() - 70 )
        self.ui.view_feature.setMinimumWidth(300)
        self.ui.lb_feature_rank.setMinimumHeight(self.ui.view_feature.height())
        self.ui.lb_feature_rank.setMinimumWidth(self.ui.sw_content.width() - self.ui.view_feature.width() - 30)

        # page 2 content size
        self.ui.lb_train.setMinimumWidth( self.ui.sw_content.width() - 20 )
        self.ui.lb_train.setMinimumHeight(500)

        # page 3 content size
        self.ui.lb_score.setMinimumWidth(self.ui.sw_content.width() - 20)
        #self.ui.lb_deviance.setMinimumWidth(self.ui.sw_content.width() - 20)
        #self.ui.lb_deviance.setMinimumHeight(800)
        self.ui.view_prediction_res.setMinimumHeight(1500)
        self.ui.view_prediction_res.setMinimumWidth(self.ui.sw_content.width() - 20)

        # page 4 content size
        self.ui.view_prediction.setMinimumWidth(self.ui.sw_content.width() - 20)
        self.ui.view_prediction.setMinimumHeight(1400)

        self.showMaximized()
        self.show()

    def init_connection(self):
        # connect signal with slot
        self.ui.pb_load.clicked.connect(self.load_data)
        self.ui.pb_feature_rank.clicked.connect(self.do_feature_ranking)
        self.ui.pb_train.clicked.connect(self.build_model)
        self.ui.pb_test.clicked.connect(self.validate_model)
        self.ui.pb_predict.clicked.connect(self.house_price_prediction)
        self.ui.pb_predict_one.clicked.connect(self.calc_price)

    def show_animate(self):
        currentFrame = self.movie.currentPixmap()
        if self.ui.sw_content.currentIndex() == 0:
            self.ui.lb_feature_rank.setPixmap(currentFrame)
        elif self.ui.sw_content.currentIndex() == 1:
            self.ui.lb_train.setPixmap(currentFrame)

    @pyqtSlot()
    def load_data(self):
        self.ui.sw_content.setCurrentIndex(0)
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        fileName, _ = QFileDialog.getOpenFileName(self, "Load Training Data", "",
                                                  "All (*.*);;Excel (*.csv);", options=options)
        if fileName:
            # load house data
            self.file_name = fileName
            self.ui.lb_filename.setText('Load File: ' + fileName)
            self.load_house_data(fileName)

    def load_house_data(self,filename):
        dm = dataManager()
        self.raw_features, list_data = dm.loadRawData(filename, 9)
        model_data = HousePriceModel(self, self.raw_features, list_data)
        self.ui.view_data.setModel(model_data)

        headers_feature = ['', 'Features']
        list_feature = [[1,item] for item in self.raw_features]
        self.model_feature = FeatureModel(self, headers_feature, list_feature)
        self.ui.view_feature.setModel(self.model_feature)
        self.ui.view_feature.setColumnWidth(0, 50)

    @pyqtSlot()
    def finish_feature_ranking(self):
        # stop waiting indicator and show feature importance
        feature_importance = self.thread_feature_ranking.feature_importance
        sorted_idx = np.argsort(feature_importance)
        pos = np.arange(sorted_idx.shape[0]) + .5
        plt.barh(pos, feature_importance[sorted_idx], align='center')

        feature_names = np.array(self.selected_features)

        plt.yticks(pos, feature_names[sorted_idx])
        plt.xlabel('Relative Importance')
        plt.title('Feature Importance Ranking')
        plt.savefig('Images\\feature_ranking.jpg')
        plt.close()

        self.thread_feature_ranking.quit()
        self.movie.frameChanged.disconnect()
        self.movie.stop()
        self.ui.lb_feature_rank.clear()
        pixmap = QPixmap('Images\\feature_ranking.jpg')
        self.ui.lb_feature_rank.setPixmap(pixmap.scaled(1200, 800))

    def start_waiting_indicator(self):
        # show waiting indicator
        self.movie = QMovie('Images//loading.gif')
        self.movie.frameChanged.connect(self.show_animate)
        self.movie.start()

    @pyqtSlot()
    def do_feature_ranking(self):
        if len(self.file_name) == 0:
            return

        self.start_waiting_indicator()

        #check user selected features
        self.drop_features.clear()
        self.selected_features.clear()
        for i in range(len(self.model_feature.list_feature)):
            if self.model_feature.list_feature[i][0]:
                self.selected_features.append(self.model_feature.list_feature[i][1])
            else:
                self.drop_features.append(self.model_feature.list_feature[i][1])

        # start a new thread to do feature ranking
        dt = dataManager()
        radio = int(self.ui.sb_train_ratio.value()) / 100
        dt.loadPredictData(self.file_name, self.drop_features, 'price',  radio)
        self.thread_feature_ranking = FeatureRankingThread(dt.X_train, dt.y_train)
        self.thread_feature_ranking.finished.connect(self.finish_feature_ranking)
        self.thread_feature_ranking.start()

    @pyqtSlot()
    def finish_model_building(self):
        self.prediction_model = self.thread_model_building.prediction_model
        self.thread_model_building.quit()
        self.movie.frameChanged.disconnect()
        self.movie.stop()
        self.ui.lb_train_tip.setText('Model has been built. Validate model next step.')

    @pyqtSlot()
    def build_model(self):
        if len(self.file_name) == 0:
            return
        self.ui.sw_content.setCurrentIndex(1)

        self.start_waiting_indicator()

        #check user selected features
        self.drop_features.clear()
        self.selected_features.clear()
        for i in range(len(self.model_feature.list_feature)):
            if self.model_feature.list_feature[i][0]:
                self.selected_features.append(self.model_feature.list_feature[i][1])
            else:
                self.drop_features.append(self.model_feature.list_feature[i][1])

        # start a new thread to do training
        dt = dataManager()
        radio = int(self.ui.sb_train_ratio.value()) / 100
        dt.loadPredictData(self.file_name, self.drop_features, 'price',  radio)
        self.x_test = dt.X_test
        self.y_test = dt.y_test
        self.thread_model_building = BuildModelThread(dt.X_train, dt.y_train)
        self.thread_model_building.finished.connect(self.finish_model_building)
        self.thread_model_building.start()


    @pyqtSlot()
    def validate_model(self):
        if len(self.selected_features) == 0 or not self.prediction_model :
            return
        # calc y_pred and score
        self.ui.sw_content.setCurrentIndex(2)
        self.y_pred = self.prediction_model.predict(self.x_test)
        score = self.prediction_model.score(self.x_test,self.y_test)
        self.ui.lb_score.setText('Prediction Score : %.2f' % float(score))

        # do not display deviance figure
        if 0:
            # compute test set deviance
            test_score = self.prediction_model.test_score(self.x_test, self.y_test)
            train_score = self.prediction_model.train_score()

            plt.title('Deviance')
            plt.plot(np.arange(self.prediction_model.mn_estimators) + 1, train_score, 'b-',
                     label='Training Set Deviance')
            plt.plot(np.arange(self.prediction_model.mn_estimators) + 1, test_score, 'r-',
                     label='Test Set Deviance')
            plt.legend(loc='upper right')
            plt.xlabel('Boosting Iterations')
            plt.ylabel('Deviance')
            plt.savefig('Images\\divance.jpg')

            pixmap = QPixmap('Images\\divance.jpg')
            self.ui.lb_deviance.setPixmap(pixmap.scaled(1200, 800))

        #prediction data
        headers = ['House Price', 'Prediction Price', 'Difference', 'Diff Percentage']
        list_data = []
        for i in range(20):
            list_data.append([self.y_test.values[i], self.y_pred[i]])
        model_validation = ValidationModel(self,headers,list_data)
        self.ui.view_prediction_res.setModel(model_validation)

    @pyqtSlot()
    def house_price_prediction(self):
        self.ui.sw_content.setCurrentIndex(3)

        headers = ['Predicted Price',]
        for x in self.selected_features:
            headers.append(x)

        print(headers)

        list_data = [''] * len(headers)
        model_prediction = PredictionModel(self, headers,list_data)
        self.ui.view_prediction.setModel(model_prediction)
        self.ui.view_prediction.setColumnWidth(0,200)

    @pyqtSlot()
    def calc_price(self):
        m = self.ui.view_prediction.model()
        user_data = m.list_data[1:]
        x_test_user = pd.DataFrame([user_data],columns=self.selected_features)
        y_pred_user = self.prediction_model.predict(x_test_user)
        m.update_predicted_price(y_pred_user[0])








if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = ML()
    sys.exit(app.exec_())



