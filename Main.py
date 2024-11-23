from PyQt6.QtWidgets import *
from PyQt6 import uic
from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import sys

class Calendar(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(580, 540)
        uic.loadUi('Calendar.ui', self)
        self.btn = QPushButton("Кнопка", self)
        self.btn.clicked.connect(self.open_window)

 
    def open_window(self):
        self.wind = Notes()
        self.wind.show()

class Notes(QDialog):
    def __init__(self):
        super().__init__()
        self.setFixedSize(600, 400)
        uic.loadUi('Notes.ui', self)
        self.btn = QPushButton("Добавить Заметку", self)
        self.button = QPushButton("Убрать Заметку", self)
        self.btn.clicked.connect(self.ConnectedQList)
        self.QList = QListWidget(self)
        self.QLine = QLineEdit(self)
        self.btn.move(380,190)
        self.btn.resize(221,51)
        self.QList.move(0,240)
        self.QLine.move(0,190)
        self.QLine.resize(381,51)
        self.QList.resize(381,181)
        self.button.resize(221,161)
        self.button.move(380,240)
    def ConnectedQList(self):
        if self.QLine.text():
            self.QList.addItem(QListWidgetItem(self.QLine.text()))
        else:
            messageBox = QMessageBox()
            messageBox.setText("Ошибка: Пустая Строка")
            messageBox.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Calendar()
    ex.show()
    sys.exit(app.exec())