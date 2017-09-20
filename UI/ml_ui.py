# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ml.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(2172, 1477)
        self.pte_content = QtWidgets.QPlainTextEdit(Dialog)
        self.pte_content.setGeometry(QtCore.QRect(290, 10, 1881, 1461))
        self.pte_content.setObjectName("pte_content")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(10, 520, 271, 291))
        self.groupBox.setObjectName("groupBox")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(20, 60, 201, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit.setGeometry(QtCore.QRect(20, 100, 241, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(20, 160, 181, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.cb_algorithm = QtWidgets.QComboBox(self.groupBox)
        self.cb_algorithm.setGeometry(QtCore.QRect(20, 220, 241, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.cb_algorithm.setFont(font)
        self.cb_algorithm.setObjectName("cb_algorithm")
        self.cb_algorithm.addItem("")
        self.cb_algorithm.addItem("")
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(11, 27, 209, 302))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pb_load = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pb_load.setFont(font)
        self.pb_load.setObjectName("pb_load")
        self.verticalLayout.addWidget(self.pb_load)
        self.pb_train = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pb_train.setFont(font)
        self.pb_train.setObjectName("pb_train")
        self.verticalLayout.addWidget(self.pb_train)
        self.pb_test = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pb_test.setFont(font)
        self.pb_test.setObjectName("pb_test")
        self.verticalLayout.addWidget(self.pb_test)

        self.retranslateUi(Dialog)
        self.cb_algorithm.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Machine Learning"))
        self.groupBox.setTitle(_translate("Dialog", "Setting"))
        self.label.setText(_translate("Dialog", "Training Size"))
        self.lineEdit.setText(_translate("Dialog", "70%"))
        self.label_2.setText(_translate("Dialog", "Algorithm"))
        self.cb_algorithm.setItemText(0, _translate("Dialog", "Linear Regression"))
        self.cb_algorithm.setItemText(1, _translate("Dialog", "Logistic Regression"))
        self.pb_load.setText(_translate("Dialog", "Load Data"))
        self.pb_train.setText(_translate("Dialog", "Train"))
        self.pb_test.setText(_translate("Dialog", "Test"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

