import sys  # sys нужен для передачи argv в QApplication
# import os
from PyQt5 import QtWidgets
import requests
import re

import getcontact
import get_error
import get_null

import qdarktheme


class Null_info(QtWidgets.QDialog, get_null.Ui_Dialog):
    def __init__(self):
        super(Null_info, self).__init__()
        self.setupUi(self)  # Загрузка дизайна из файла
        self.setFixedSize(400, 124)

        self.setModal(True)


class Error(QtWidgets.QDialog, get_error.Ui_Dialog):
    def __init__(self):
        super(Error, self).__init__()
        self.setupUi(self)  # Загрузка дизайна из файла
        self.setFixedSize(358, 131)

        self.setModal(True)


class App(QtWidgets.QMainWindow, getcontact.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.lineEdit.clear()

        self.tableWidget.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)

        self.tableWidget_2.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)

        self.tableWidget.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch)
        self.tableWidget_2.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch)

        self.pushButton.clicked.connect(self.search)

    def is_phone_number(self, phone_number):
        pattern = r'^(7|8|\+7)\d{10}$'
        return bool(re.match(pattern, phone_number))

    def search(self):
        number = self.lineEdit.text()
        status = self.is_phone_number(number)
        if status:
            data = {'number': number}
            html = requests.post(
                'http://127.0.0.1:6666/api', data=data)
            row = html.json()
            if row != {}:
                numbuster = row[0][0].split(',\n')
                getcontact = row[0][1].split(',\n')
                self.tableWidget.setRowCount(len(getcontact))
                self.tableWidget_2.setRowCount(len(numbuster))

                for i, x in enumerate(numbuster):
                    self.tableWidget_2.setItem(
                        0, i, QtWidgets.QTableWidgetItem(x))

                for i, x in enumerate(getcontact):
                    self.tableWidget.setItem(
                        0, i, QtWidgets.QTableWidgetItem(x))
            else:
                self.error = Null_info()
                self.error.show()

        else:
            self.error = Error()
            self.error.show()

        # self.lineEdit.clear()


def main():
    # Enable HiDPI.
    qdarktheme.enable_hi_dpi()

    app = QtWidgets.QApplication(sys.argv)

    # Apply dark theme.
    qdarktheme.setup_theme(custom_colors={"primary": "#00ff00"})

    window = App()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
