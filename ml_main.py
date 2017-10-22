import sys
import ctypes
from PyQt5 import (QtWidgets, QtGui, QtCore)
from PyQt5.QtCore import *
from PyQt5.QtWidgets import (QMainWindow, QFileDialog)
from PyQt5.QtGui import *
from PyQt5.Qt import (QWidget, QLabel,QSizePolicy,QVBoxLayout, QProgressDialog, QPixmap)
from UI.ml_ui import Ui_MainWindow
from DataManagement.feature_ranking import FeatureRanking
from DataManagement.dataManager import *
from DataManagement.featureModel import *

class PopUp(QWidget):
    def __init__(self):
        QWidget.__init__(self)

    def paintEvent(self, QPaintEvent):
        doc = QPainter(self)
        doc.drawLine(0,0,100,100)

    def showEvent(self, QShowEvent):
        self.movie_screen = QLabel()
        self.movie_screen.setSizePolicy(QSizePolicy.Expanding,
            QSizePolicy.Expanding)
        self.movie_screen.setAlignment(Qt.AlignCenter)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.movie_screen)
        self.setLayout(main_layout)

        self.moive = QMovie('Images\\loading.gif', QByteArray(),self)
        self.movie.setCacheMode(QMovie.CacheAll)
        self.movie.setSpeed(100)
        self.movie_screen.setMovie(self.movie)
        self.movie.start()




class ML(QMainWindow):
    def __init__(self, parent=None):
        super(ML,self).__init__(parent=None)
        self.init_ui()

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

        self.showMaximized()

        # connect signal with slot
        self.ui.pb_load.clicked.connect(self.load_data)
        self.ui.pb_train.clicked.connect(self.train)
        self.ui.pb_test.clicked.connect(self.get_res)
        self.show()


    @pyqtSlot()
    def load_data(self):
        self.ui.sw_content.setCurrentIndex(0)
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        fileName, _ = QFileDialog.getOpenFileName(self, "Load Training Data", "",
                                                  "All (*.*);;Excel (*.csv);", options=options)
        if fileName:
            self.ui.lb_filename.setText('Load File: ' + fileName)
            self.load_house_data(fileName)

            pixmap = QPixmap('Images\\feature_ranking.jpg')
            w = 1200
            h = 600
            self.ui.lb_feature_rank.setPixmap(pixmap.scaled(w,h))

    def load_house_data(self,filename):
        dm = dataManager()
        header_data, list_data = dm.loadRawData(filename, 4)
        model_data = HousePriceModel(self, header_data, list_data)
        self.ui.view_data.setModel(model_data)

        headers_feature = ['', 'Features']
        list_feature = [[0,item] for item in header_data]
        model_feature = FeatureModel(self, headers_feature, list_feature)
        self.ui.view_feature.setModel(model_feature)
        self.ui.view_feature.setColumnWidth(0, 50)

    def load_feature_importance(self,filename):
        pass



    @pyqtSlot()
    def train(self):
        self.ui.sw_content.setCurrentIndex(1)

        self.progressDlg = QProgressDialog(self)
        self.progressDlg.setCancelButton("&Cancel")
        self.progressDlg.setRange(0,100)
        for i in range(0,100):
            self.progressDlg.setValue(i)
            self.progressDlg.setLabelText("Training ... ")
            QCoreApplication.processEvents()
            if self.progressDlg.wasCanceled():
                break
            QThread.sleep(1)

       # self.progressDlg.close()



        '''self.w = PopUp()
        self.w.setGeometry(QRect(800,500,300,300))
        self.w.setWindowFlag(Qt.FramelessWindowHint)
        self.w.show()'''


    def list_features(self):
        pass

    @pyqtSlot()
    def get_res(self):
        self.ui.sw_content.setCurrentIndex(2)
        # pixmap = QPixmap('image.jpg')
       # self.ui.lb_img.setPixmap(pixmap)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = ML()
    sys.exit(app.exec_())



