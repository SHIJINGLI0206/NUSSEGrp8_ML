from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QFileDialog
from ml_ui import Ui_Dialog
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class ML(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(ML,self).__init__(parent=None)
        self.init_ui()

    def init_ui(self):
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.pb_load.clicked.connect(self.load_data)
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
        pass

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = ML()
    sys.exit(app.exec_())



