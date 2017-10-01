import sys
import ctypes
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import (QMainWindow, QFileDialog)
from PyQt5.QtGui import *
from UI.ml_ui import Ui_MainWindow


class ML(QMainWindow):
    def __init__(self, parent=None):
        super(ML,self).__init__(parent=None)
        self.init_ui()

    def init_ui(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
       # addDockWidget(Qt.RightDockWidgetArea,self.ui.dockWidget)

        screen_width = ctypes.windll.user32.GetSystemMetrics(0)
        self.ui.dw_right.setMinimumWidth(screen_width - self.ui.dw_left.width())
        self.showMaximized()

        self.ui.pb_load.clicked.connect(self.load_data)
        self.ui.pb_test.clicked.connect(self.get_res)
        self.show()


    @pyqtSlot()
    def load_data(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Load Training Data", "",
                                                  "All Files (*);;Excel (*.csv);;Text (*.txt)", options=options)
        if fileName:
            self.ui.pte_content.appendHtml(fileName)

    @pyqtSlot()
    def train(self):
        pass

    @pyqtSlot()
    def get_res(self):
        pixmap = QPixmap('image.jpg')
        self.ui.lb_img.setPixmap(pixmap)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = ML()
    sys.exit(app.exec_())



