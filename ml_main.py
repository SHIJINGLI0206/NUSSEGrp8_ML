import sys
import ctypes
from PyQt5 import (QtWidgets, QtGui)
from PyQt5.QtCore import *
from PyQt5.QtWidgets import (QMainWindow, QFileDialog)
from PyQt5.QtGui import (QPainter,QMovie)
from PyQt5.Qt import (QWidget, QLabel,QSizePolicy,QVBoxLayout, QProgressDialog, QPixmap)
from UI.ml_ui import Ui_MainWindow
from DataManagement.feature_ranking import FeatureRanking

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
       # addDockWidget(Qt.RightDockWidgetArea,self.ui.dockWidget)

        # init widget size
        screen_width = ctypes.windll.user32.GetSystemMetrics(0)
        screen_height = ctypes.windll.user32.GetSystemMetrics(1)
        self.ui.dw_right.setMinimumWidth(screen_width - self.ui.dw_left.width() - 10)
        self.ui.sw_content.setMinimumWidth(screen_width - self.ui.dw_left.width() - 40)
        self.ui.sw_content.setMinimumHeight(screen_height - 230)

        self.ui.lb_filename.setMinimumWidth(self.ui.sw_content.width() - 30)
        self.ui.lb_features.setMinimumWidth(self.ui.sw_content.width() - 30)
        self.ui.lb_features.setMinimumHeight(self.ui.sw_content.height() - 200)
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
                                                  "All Files (*);;Excel (*.csv);;Text (*.txt)", options=options)
        if fileName:
            self.ui.lb_filename.setText('Load File: ' + fileName)
            feature_ranking = FeatureRanking(fileName)
           # feature_ranking.do_rank()

            pixmap = QPixmap('Images\\feature_ranking.jpg')
            w = 1200
            h = 800
            self.ui.lb_features.setPixmap(pixmap.scaled(w,h))



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




    @pyqtSlot()
    def get_res(self):
        self.ui.sw_content.setCurrentIndex(2)
        # pixmap = QPixmap('image.jpg')
       # self.ui.lb_img.setPixmap(pixmap)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = ML()
    sys.exit(app.exec_())



