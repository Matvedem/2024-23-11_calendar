from PyQt6.QtWidgets import *
from PyQt6 import uic
from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import sqlite3
import sys
import datetime

global_date = ''


class Calendar(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(580, 540)
        self.setWindowTitle('Календарь')
        uic.loadUi('D:\\Project\\UI\\Calendar.ui', self)
        self.second_window_button = QPushButton('Заметки', self)
        self.second_window_button.clicked.connect(self.open_window)
        self.q_calendar = QCalendarWidget(self)
        self.q_calendar.move(0, 60)
        self.q_calendar.resize(581, 451)

    def open_window(self):
        global global_date
        global_date = self.q_calendar.selectedDate().toPyDate()
        self.window_second = Notes()
        self.window_second.show()


class Notes(QDialog):
    def __init__(self):
        super().__init__()
        self.selecteddate = global_date.strftime('%Y-%m-%d')
        self.setFixedSize(600, 400)
        uic.loadUi('D:\\Project\\UI\\Notes.ui', self)
        self.add_note_button = QPushButton('Добавить Заметку', self)
        self.delete_note_button = QPushButton('Убрать Заметку', self)
        self.add_note_button.clicked.connect(self.add_note_button_pressed)
        self.delete_note_button.clicked.connect(self.delete_note_button_pressed)
        self.task_list = QListWidget(self)
        self.text_line = QLineEdit(self)
        self.add_note_button.move(380, 190)
        self.add_note_button.resize(221, 51)
        self.task_list.move(0, 240)
        self.text_line.move(0, 190)
        self.text_line.resize(381, 51)
        self.task_list.resize(381, 181)
        self.delete_note_button.resize(221, 161)
        self.delete_note_button.move(380, 240)
        tl = self.reading_data_base()
        for t in tl:
            self.task_list.addItem(t)

    def add_note_button_pressed(self):
        linetext = self.text_line.text()
        if linetext:
            self.task_list.addItem(QListWidgetItem(linetext))
            self.saving_changes_in_qlist(linetext)
            self.text_line.setText('')
        else:
            messageBox = QMessageBox()
            messageBox.setText('Ошибка: пустая строка')
            messageBox.exec()

    def reading_data_base(self):
        date = self.selecteddate
        db = sqlite3.connect('D:\\Project\\DataBase\\mydata.db')
        cursor = db.cursor()

        query = 'SELECT task FROM tasks WHERE date = ?'
        row = (date,)
        results = cursor.execute(query, row).fetchall()
        tasklist = []
        for result in results:
            tasklist.append(result[0])
        return tasklist

    def saving_changes_in_qlist(self, add2list):
        db = sqlite3.connect('D:\\Project\\DataBase\\mydata.db')
        cursor = db.cursor()
        query = 'INSERT INTO tasks(task, date) VALUES (?,?)'
        row = (add2list, self.selecteddate)
        cursor.execute(query, row)
        db.commit()

    def delete_note_button_pressed(self):
        item = self.task_list.currentItem()
        if item is not None:

            date = self.selecteddate
            itemtext = item.text()
            db = sqlite3.connect('D:\\Project\\DataBase\\mydata.db')
            cursor = db.cursor()
            query = 'DELETE FROM tasks WHERE task = ? AND date = ?;'
            row = (itemtext, date)
            cursor.execute(query, row)
            db.commit()

            self.task_list.clear()

            date = self.selecteddate
            db = sqlite3.connect('D:\\Project\\DataBase\\mydata.db')
            cursor = db.cursor()
            query = 'SELECT task FROM tasks WHERE date = ?'
            row = (date,)
            results = cursor.execute(query, row).fetchall()
            for result in results:
                self.task_list.addItem(result[0])
        else:
            messageBox = QMessageBox()
            messageBox.setText('Ошибка: в списке не выбрана строка для удаления')
            messageBox.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Calendar()
    ex.show()
    sys.exit(app.exec())
