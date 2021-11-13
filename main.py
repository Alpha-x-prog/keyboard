import sys
from PyQt5 import QtWidgets, QtCore, QtGui, uic
from PyQt5.QtWidgets import QApplication
import sqlite3
import random
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

conn = sqlite3.connect('base_date/base.db')
cursor = conn.cursor()
key_board = ["а", "б", "в", "г", "д", "е", "ё", "ж", "з", "и", "й", "к", "л", "м", "н", "о",
             "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "ъ", "ы", "ь", "э", "ю", "я",
             "-", "=", "\"", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
first_side = ['Ё', 'Ё', 'Ц', 'У', 'К', 'Е', 'Ф', 'Ы', 'В', 'А', 'П', 'Я', 'Ч', 'С', 'М', 'И', '1', '2', '3', '4', '5']
additional_characters = {ord('"'): ['Left_Shift', 2], ord(':'): ['Right_Shift', 6], ord(","): ['Right_Shift', '.']}


# conn.close()


class FirstWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.window = None
        self.general_window = None
        self.user_name = None
        self.init_ui()

    def init_ui(self):
        super(FirstWindow, self).__init__()
        self.window = uic.loadUi('qt_designer/first_window.ui', self)
        self.window.setWindowTitle('Введите имя')
        self.show()
        self.window.btnfinished.clicked.connect(self.btn_clicked)

    def btn_clicked(self):
        result_name = self.window.user_name_label.text()
        if result_name:
            cursor.execute('INSERT INTO user_informational '
                           'VAlUES (?)', (result_name,))
            conn.commit()
            self.general_window = GeneralWindow()
            self.general_window.show()
            self.close()
        else:
            self.window.warning.setText("нельзя войти с пустым именем")


class GeneralWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.window = None

    def initUI(self):
        super(GeneralWindow, self).__init__()
        self.window = uic.loadUi('qt_designer/general information.ui', self)
        self.window.setWindowTitle('Общее')
        self.show()
        self.window.btntest.clicked.connect(self.testing)

    def testing(self):
        self.print_test = Test()
        self.print_test.show()
        self.close()


class Test(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.window = None
        self.count_pressed = 0
        self.text = None
        self.first_color_button = None
        self.dop_button_color = None
        self.first_button = None
        self.shift_button = 0
        self.symbols = None
        self.red_button = None
        self.red_button_color = None
        self.result_typ = None
        self.count_time = 0
        self.mistakes = 0
        self.timer = None
        self.init_ui()

    def init_ui(self):
        super(Test, self).__init__()
        self.window = uic.loadUi('qt_designer/test.ui', self)
        self.window.setWindowTitle('Проверка скорости')

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1000)

        count_str = cursor.execute('SELECT COUNT(1) '
                                   'FROM texts').fetchone()[0]
        id_text = random.randint(1, count_str)
        self.text, self.symbols = cursor.execute('SELECT text, symbols '
                                                 'FROM texts '
                                                 'WHERE id = ?', (5,)).fetchone()  # id_text
        self.window.for_text.setPlainText(self.text)
        self.show()
        self.change_color_button_green(ord(self.text[self.count_pressed]))
        self.window.user_text.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj is self.window.user_text and event.type() == QtCore.QEvent.KeyPress:
            if event.text() == self.text[self.count_pressed]:
                self.change_color_button_reverse_green()
                self.count_pressed += 1
                if self.count_pressed >= self.symbols:
                    self.result_typ = ResultTyping(self.count_time, self.mistakes)
                    self.result_typ.show()
                    self.timer.stop()
                    self.close()
                else:
                    self.change_color_button_green(ord(self.text[self.count_pressed].upper()))
                return False
            else:
                self.mistakes += 1
                return True
        return False

    def change_color_button_green(self, number_button):
        shift = 0
        if number_button in additional_characters:
            self.first_button = 'pushButton_' + str(ord(str(additional_characters.get(34)[1])))
            shift = 1
        else:
            self.first_button = 'pushButton_' + str(number_button)
        self.first_color_button = self.window.findChild(QPushButton,
                                                        self.first_button).palette().button().color().name()
        self.window.findChild(QPushButton, self.first_button).setStyleSheet("background-color: '#00ff00'")
        name_button = self.text[self.count_pressed]
        if name_button.isupper() or shift == 1:
            if name_button not in first_side:
                self.dop_button_color = self.window.Left_Shift.palette().button().color().name()
                self.window.Left_Shift.setStyleSheet("background-color: #00ff00")
                self.shift_button = 1
            else:
                self.dop_button_color = self.window.Right_Shift.palette().button().color().name()
                self.window.Right_Shift.setStyleSheet("background-color: #00ff00")
                self.shift_button = 2

    def change_color_button_reverse_green(self):
        self.window.findChild(QPushButton, self.first_button).setStyleSheet(
            f"background-color: {self.first_color_button}")
        if self.shift_button == 1:
            self.window.Left_Shift.setStyleSheet(f"background-color: {self.dop_button_color}")
        elif self.shift_button == 2:
            self.window.Right_Shift.setStyleSheet(f"background-color: {self.dop_button_color}")
        self.shift = 0

    def showTime(self):
        self.count_time += 1
        self.window.time.setText(str(self.count_time // 60) + "." + str(self.count_time % 60).zfill(2))


class ResultTyping(QtWidgets.QMainWindow):
    def __init__(self, time, mistakes):
        super().__init__()
        self.window = None
        self.time = time
        self.mistakes = mistakes
        self.init_ui()

    def init_ui(self):
        print(self.mistakes, self.time)
        super(ResultTyping, self).__init__()
        self.window = uic.loadUi('qt_designer/result_test.ui', self)
        self.show()


if __name__ == '__main__':
    result = cursor.execute('SELECT user_name '
                            'FROM user_informational').fetchone()
    app = QApplication(sys.argv)
    if not result:
        window = FirstWindow()
    else:
        window = GeneralWindow()
    sys.exit(app.exec_())
