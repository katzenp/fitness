"""
weighin_ui.py

Description:
    Weigh logging user interfaces
"""
# stdlib
import datetime
import sys

# external
from PyQt5 import QtCore, QtGui, QtWidgets


class WeighInModel(QtCore.QAbstractItemModel):
    def __init__(self, parent=None):
        super(WeighInModel, self).__init__(parent)
        self._internal_data = (
            ["monday",    0.0],
            ["tuesday",   0.0],
            ["wednesday", 0.0],
            ["thursday",  0.0],
            ["friday",    0.0],
            ["saturday",  0.0],
            ["sunday",    0.0],
            ["average",   0.0],
        )

    def rowCount(self, parent=QtCore.QModelIndex()):
        """
        Returns the number of number of rows this model contains

        :param parent: The QModelIndex you wish to query
        :param parent: instance of <class 'QtCore.QModelIndex'>
        :return: n/a
        :rtype: int
        """
        return len(self._internal_data)

    def columnCount(self, parent=QtCore.QModelIndex()):
        """
        Returns the number of columns number of columns this model contains

        :param parent: The QModelIndex you wish to query
        :param parent: instance of <class 'QtCore.QModelIndex'>
        :return: number of columns this model contains
        :rtype: int
        """
        return len(self._internal_data[0])

    def flags(self, index):
        """
        Sets the various properties of QModelIndex objects associated with this model

        :param index: The QModelIndex to operate on
        :param index: instance of <class 'QtCore.QModelIndex'>
        :return: item data flags
        :rtype: QtCore.Qt.ItemData flag
        """
        row = index.row()
        column = index.column()

        flags = QtCore.Qt.ItemIsEnabled

        if column == 1 and row != 7:
            flags = (
                QtCore.Qt.ItemIsEnabled |
                QtCore.Qt.ItemIsSelectable |
                QtCore.Qt.ItemIsEditable
            )
        return flags

    def parent(self, index):
        """
        Returns the parent of the specified QModelIndex

        :param index: the QModelIndex to operate on
        :type index: instance of <class 'QModelIndex'>
        :return: the parent of the specified QModelIndex
        :rtype: instance of <class 'QModelIndex'>
        """
        return QtCore.QModelIndex()

    def index(self, row, column, parent):
        """
        Returns a QModelIndex for the given row and column, with the specified parent

        :param row: the child index's row number relative to the specified parent index
        :type row: int
        :param column: the child index's column number relative to the specified parent index
        :type column: int
        :param parent: QModelIndex whose child index you wish to fetch
        :type parent: instance of <class 'QModelIndex'>
        :return: child index
        :rtype: instance of <class 'QModelIndex'>
        """
        return self.createIndex(row, column, QtCore.QModelIndex())

    def data(self, index, role):
        """
        Returns a value that this model's view expects for the specified role

        :param index: The QModelIndex to operate on
        :param index: instance of <class 'QtCore.QModelIndex'>
        :param role: the item data role whose value you wish to fetch
        :type role: QtCore.Qt.ItemDataRole value
        :return: a piece of data from the internal data block
        :rtype: any
        """
        row = index.row()
        column = index.column()

        if role == QtCore.Qt.DisplayRole:
            value = self._internal_data[row][column]
            if not isinstance(value, basestring):
                value = repr(value)
            return value

        if role == QtCore.Qt.ForegroundRole:
            if column == 1:
                return QtGui.QColor(20, 120, 120)
            return QtGui.QColor(20, 20, 20)
        
        if role == QtCore.Qt.TextAlignmentRole:
            if column == 1:
                return QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter
            return QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter

    def setData(self, index, value, role):
        row = index.row()
        column = index.column()
        if column == 1 and row != 7:
            self._internal_data[row][column] = value
            self.dataChanged.emit(index, index)
            return True
        return False



class WeighInDelegate(QtWidgets.QItemDelegate):
    def __init__(self, parent=None):
        super(WeighInDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        if index.row() != 7 and index.column() == 1: 
            editor = QtWidgets.QSpinBox(parent)
            editor.setButtonSymbols(QtWidgets.QSpinBox.NoButtons)
            editor.setRange(0.0, 1000.0)
        else:
            editor = super(WeighInDelegate, self).createEditor(
                parent, option, index
            )
        return editor
        

class WeighInDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(WeighInDialog, self).__init__(parent=parent)
        self.setStyleSheet("""
            QWidget * {border: 1px solid blue;}
            QDoubleSpinBox {color: black;}
        """)

        self._entries = (
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
            "average",
        )
        self._labels = []
        self._spinboxes = []

        self._build_ui()
        self._connect_signals()
        self._data_changed()

    def _build_ui(self):
        self._main_layout = QtWidgets.QGridLayout()
        self._main_layout.setHorizontalSpacing(0)
        self._main_layout.setContentsMargins(4, 4, 4, 4)
        self.setLayout(self._main_layout)

        date = datetime.datetime.today().strftime("%x")
        self._date_field = QtWidgets.QLabel(date)
        self._date_field.setAlignment(QtCore.Qt.AlignCenter)
        self._main_layout.addWidget(self._date_field, 0, 0, 1, 2)

        row = 1
        for each in self._entries:
            label = QtWidgets.QLabel(each)
            label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
            self._main_layout.addWidget(label, row, 0, 1, 1)
            self._labels.append(label)

            spinbox = QtWidgets.QDoubleSpinBox()
            spinbox.setRange(0.0, 1000.0)
            spinbox.setSingleStep(1.0)
            spinbox.setButtonSymbols(QtWidgets.QSpinBox.NoButtons)
            if each is self._entries[-1]:
                spinbox.setEnabled(False)
            self._main_layout.addWidget(spinbox, row, 1, 1, 1)
            self._spinboxes.append(spinbox)

            row += 1

    def _data_changed(self):
        values = []
        for each in self._spinboxes[:-1]:
            v = each.value()
            if v:
                values.append(v)
        total = 0.0
        if values:
            total = sum(values) / len(values)
        self._spinboxes[-1].setValue(total)

    def _connect_signals(self):
        for each in self._spinboxes[:-1]:
            each.valueChanged.connect(self._data_changed)
        