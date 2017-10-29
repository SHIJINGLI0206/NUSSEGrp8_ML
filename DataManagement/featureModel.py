from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtGui, QtCore

class HousePriceModel(QAbstractTableModel):
    def __init__(self,parent,headers, list_house_data, *args):
        QAbstractTableModel.__init__(self,parent,*args)
        self.list_data = list_house_data
        self.headers = headers

    def setData(self, QModelIndex, Any, role=None):
        pass

    def headerData(self, p_int, orientation, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headers[p_int]
        return None

    def data(self, index, role=None):
        if not index.isValid():
            return None
        value = str(self.list_data[index.row()][index.column()])
        if role == QtCore.Qt.DisplayRole:
            return value

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.list_data)

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self.headers)

    def setDataList(self, list):
        self.list_data = list
        self.layoutAboutToBeChanged.emit()
        self.dataChanged.emit(self.createIndex(0,0), self.createIndex(self.rowCount(0), self.columnCount(0)))
        self.layoutChanged.emit()


class FeatureModel(QAbstractTableModel):
    def __init__(self,parent, headers, list_feature, *args):
        QAbstractTableModel.__init__(self,parent,*args)
        self.list_feature = list_feature
        self.headers = headers

    def headerData(self, p_int, Orientation, role=None):
        if Orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headers[p_int]
        return None

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.list_feature)

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self.headers)

    def data(self, index, role=None):
        if not index.isValid():
            return None
        value = None
        if role == Qt.CheckStateRole and index.column() == 0:
            return QtCore.QVariant(self.list_feature[index.row()][0])
        if role == Qt.DisplayRole and index.column() == 1:
            value = str(self.list_feature[index.row()][1]).strip()
        return value

    def setData(self, index, value, role=None):
        if role == Qt.CheckStateRole and index.column() == 0 :
            self.list_feature[index.row()][0] = 1 - self.list_feature[index.row()][0]
            self.dataChanged.emit(index,index)
            return True
        return False

    def flags(self, index):
        if index.column() == 0:
            return Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsUserCheckable | Qt.ItemIsSelectable
        else:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable



class ValidationModel(QAbstractTableModel):
    def __init__(self,parent, headers, list_data, *args):
        QAbstractTableModel.__init__(self,parent,*args)
        self.list_data = list_data
        self.headers = headers

    def headerData(self, p_int, Orientation, role=None):
        if Orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headers[p_int]
        return None

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.list_data)

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self.headers)

    def data(self, index, role=None):
        if not index.isValid():
            return None
        value = None
        if role == Qt.DisplayRole:
            if index.column() == 2:
                value = format((float(self.list_data[index.row()][0]) - float(self.list_data[index.row()][1])),'.2f')
            elif index.column() == 3:
                tmp = abs(float(self.list_data[index.row()][0]) - float(self.list_data[index.row()][1])) * 100 / float(self.list_data[index.row()][0])
                value = ('%s' % format(tmp,'.2f')) + '%'
            else:
                value = str(self.list_data[index.row()][index.column()])
        return value


class PredictionModel(QAbstractTableModel):
    def __init__(self,parent, headers, list_data, *args):
        QAbstractTableModel.__init__(self,parent,*args)
        self.list_data = list_data
        self.headers = headers

    def headerData(self, p_int, Orientation, role=None):
        if Orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headers[p_int]
        return None

    def rowCount(self, parent=None, *args, **kwargs):
        return 1

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self.headers)

    def data(self, index, role=None):
        if not index.isValid():
            return None
        value = None
        if role == Qt.DisplayRole:
            value = str(self.list_data[index.column()])
            if index.column() == 0 and len(self.list_data[index.column()])>0:
                value = format(float(value),'.2f')
        return value

    def setData(self, index, value, role=None):
        if role == Qt.ItemIsEditable or role == Qt.DisplayRole:
            self.list_data[index.column()] = value if len(value)> 0 else 0
            self.dataChanged.emit(index,index)
            return True
        return False

    def flags(self, index):
        if index.column() == 0:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable
        else:
            return Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable

    def update_predicted_price(self,price):
        self.list_data[0] = str(price)
        self.dataChanged.emit(self.createIndex(0,0),self.createIndex(0,self.columnCount()))


