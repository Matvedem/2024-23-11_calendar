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
        uic.loadUi('D:\\Project\\UI\\Calendar.ui', self)
        self.SecondWindowButton = QPushButton("Кнопка", self)
        self.SecondWindowButton.clicked.connect(self.open_window)
        self.QCalendar = QCalendarWidget(self)
        self.QCalendar.move(0, 60)
        self.QCalendar.resize(581, 451)

    def open_window(self):
        global global_date
        global_date = self.QCalendar.selectedDate().toPyDate()
        self.window_second = Notes()
        self.window_second.show()
        messageBox = QMessageBox()
        messageBox.setText(f"date selected {global_date}")
        print(global_date)
        messageBox.exec()


class Notes(QDialog):
    def __init__(self):
        super().__init__()
        self.selecteddate = global_date.strftime("%Y-%m-%d")
        self.setFixedSize(600, 400)
        uic.loadUi('D:\\Project\\UI\\Notes.ui', self)
        self.AddTaskButton = QPushButton("Добавить Заметку", self)
        self.DeleteTaskButton = QPushButton("Убрать Заметку", self)
        self.AddTaskButton.clicked.connect(self.Connecting_QList_AddTaskButton)
        self.DeleteTaskButton.clicked.connect(self.DeletingInQlist)
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
        tl = self.ReadingDataBase()
        for t in tl:
            self.QTaskList.addItem(t)

    def Connecting_QList_AddTaskButton(self):
        LineText = self.QTextLine.text()
        if LineText:
            self.QTaskList.addItem(QListWidgetItem(LineText))
            self.SavingChanges_In_Qlist(LineText)
        else:
            messageBox = QMessageBox()
            messageBox.setText("Ошибка: Пустая Строка")
            messageBox.exec()

    def ReadingDataBase(self):
        date = self.selecteddate
        db = sqlite3.connect("D:\\Project\\DataBase\\mydata.db")
        cursor = db.cursor()

        query = "SELECT task FROM tasks WHERE date = ?"
        row = (date,)
        results = cursor.execute(query, row).fetchall()
        tasklist = []
        for result in results:
            print(result[0])
            tasklist.append(result[0])
        return tasklist

    def SavingChanges_In_Qlist(self, add2list):
        db = sqlite3.connect("D:\\Project\\DataBase\\mydata.db")
        cursor = db.cursor()
        query = "INSERT INTO tasks(task, date) VALUES (?,?)"
        row = (add2list, self.selecteddate)
        cursor.execute(query, row)
        db.commit()

    def DeletingInQlist(self):
        item = self.QTaskList.currentItem()
        date = self.selecteddate
        ItemText = item.text()
        db = sqlite3.connect("D:\\Project\\DataBase\\mydata.db")
        cursor = db.cursor()
        query = "DELETE FROM tasks WHERE task = ? AND date = ?;"
        row = (ItemText, date)
        cursor.execute(query, row)
        db.commit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Calendar()
    ex.show()
    sys.exit(app.exec())
