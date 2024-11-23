from PyQt6.QtWidgets import *
from PyQt6 import uic
from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import sqlite3
import sys
import datetime
global_date = ""

class Calendar(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(580, 540)
        uic.loadUi('Calendar.ui', self)
        self.SecondWindowButton = QPushButton("Кнопка", self)
        self.SecondWindowButton.clicked.connect(self.open_window)
        self.QCalendar = QCalendarWidget(self)
        self.QCalendar.move(0, 60)
        self.QCalendar.resize(581, 451)

    def open_window(self):
        global global_date
        global_date = self.QCalendar.selectedDate().toPyDate()
        self.wind = Notes()
        self.wind.show()
        messageBox = QMessageBox()
        messageBox.setText(f"date selected {global_date}")
        print(global_date)
        messageBox.exec()



class Notes(QDialog):
    def __init__(self):
        super().__init__()
        self.myselecteddate = global_date.strftime("%Y-%m-%d")
        self.setFixedSize(600, 400)
        uic.loadUi('Notes.ui', self)
        self.AddTaskButton = QPushButton("Добавить Заметку", self)
        self.DeleteTaskButton = QPushButton("Убрать Заметку", self)
        self.AddTaskButton.clicked.connect(self.ConnectedQList)
        self.QTaskList = QListWidget(self)
        self.QTextLine = QLineEdit(self)
        self.AddTaskButton.move(380, 190)
        self.AddTaskButton.resize(221, 51)
        self.QTaskList.move(0, 240)
        self.QTextLine.move(0, 190)
        self.QTextLine.resize(381, 51)
        self.QTaskList.resize(381, 181)
        self.DeleteTaskButton.resize(221, 161)

        self.DeleteTaskButton.move(380, 240)

    def ConnectedQList(self):
        if self.QTextLine.text():
            self.QTaskList.addItem(QListWidgetItem(self.QTextLine.text()))
            # self.saveChanges(add2list=QTextLine.text(), , )
        else:
            messageBox = QMessageBox()
            messageBox.setText("Ошибка: Пустая Строка")
            messageBox.exec()

    def readdb(date):
        db = sqlite3.connect("D:\\Project\\mydata.db")
        cursor = db.cursor()

        query = "SELECT task FROM tasks WHERE date = ?"
        row = (date)
        results = cursor.execute(query, row).fetchall()
        tasklist = []
        for result in results:
            print(result)
            tasklist.append(result)
        return tasklist

    def saveChanges(add2list, tasklist, date):
        db = sqlite3.connect("D:\\Project\\mydata.db")
        cursor = db.cursor()
        tasklist.append(add2list)
        query = "INSERT INTO tasks(task, date) VALUES (?,?)"
        row = (add2list, date)
        cursor.execute(query, row)
        db.commit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Calendar()
    ex.show()
    sys.exit(app.exec())
