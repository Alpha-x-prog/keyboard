import sys
from PyQt5 import QtWidgets, QtCore, QtGui, uic
from PyQt5.QtWidgets import QApplication
import sqlite3
import random
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import math

conn = sqlite3.connect('base_date/base.db')
cursor = conn.cursor()
key_board = ["а", "б", "в", "г", "д", "е", "ё", "ж", "з", "и", "й", "к", "л", "м", "н", "о",
             "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "ъ", "ы", "ь", "э", "ю", "я",
             "-", "=", "\"", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
first_side = ['Ё', 'Ё', 'Ц', 'У', 'К', 'Е', 'Ф', 'Ы', 'В', 'А', 'П', 'Я', 'Ч', 'С', 'М', 'И', '1', '2', '3', '4', '5']
additional_characters = {ord('"'): ['Left_Shift', 2], ord(':'): ['Right_Shift', 6], ord(","): ['Right_Shift', '.']}
lessons_letters = {1: ['ф', 'ы', 'в', 'а', 'о', 'л', 'д', 'ж'], 2: ['п', 'р']}


# conn.close()


class SwitchBetweenButtons(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.window = None
        self.user_test = None
        self.user_lessons = None

    def testing(self):
        self.user_test = Test()
        self.user_test.show()
        self.close()

    def lessons(self, lesson_number, part):
        self.user_lessons = UserLessons(lesson_number, part)
        self.user_lessons.show()
        self.close()


class ButtonsClick(SwitchBetweenButtons):
    def __init__(self):
        super().__init__()
        self.dop_button_color = None
        self.first_button = None
        self.first_press = 1
        self.result_typ = None
        self.first_color_button = None
        self.shift_button = None
        self.shift = None

    def eventFilter(self, obj, event):
        if obj is self.window.user_text and event.type() == QtCore.QEvent.KeyPress:
            if self.first_press == 1:
                self.timer.start(1000)
                self.first_press = 0
            if event.text() == self.text[self.count_pressed]:
                self.change_color_button_reverse_green()
                self.count_pressed += 1
                if self.count_pressed >= self.symbols:
                    self.result_typ = ResultTyping(self.count_time, self.mistakes, self.symbols)
                    self.result_typ.show()
                    self.timer.stop()
                    self.close()
                else:
                    self.change_color_button_green(ord(self.text[self.count_pressed].upper()))
                return False
            else:
                if event.text():
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


class FirstWindow(SwitchBetweenButtons):
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


class GeneralWindow(SwitchBetweenButtons):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        super(GeneralWindow, self).__init__()
        self.window = uic.loadUi('qt_designer/general information.ui', self)
        self.window.setWindowTitle('Общее')
        self.show()
        self.window.btn_testing.clicked.connect(self.testing)
        self.window.btn_user_lessons.clicked.connect(lambda: self.lessons(1, 1))


class Test(ButtonsClick):
    def __init__(self):
        super().__init__()
        self.window = None
        self.count_pressed = 0
        self.text = None
        self.symbols = None
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


class ResultTyping(QtWidgets.QMainWindow):
    def __init__(self, time, mistakes, symbols):
        super().__init__()
        self.window = None
        self.time_typing = time
        self.user_mistakes = mistakes
        self.symbols = symbols
        self.init_ui()

    def init_ui(self):
        super(ResultTyping, self).__init__()
        self.window = uic.loadUi('qt_designer/result_test.ui', self)
        minutes, second = self.russian_language(self.time_typing // 60, 'минут'), self.russian_language(
            self.time_typing % 60, 'секунд'),

        self.window.time.setText(f'{minutes} {second}')
        self.window.speed.setText(f'{math.ceil(self.symbols // self.time_typing * 60)} симв/мин')
        self.window.mistakes.setText(f'{self.user_mistakes}')
        print(self.user_mistakes, self.symbols)
        self.window.purity.setText(f'{format((self.symbols - self.user_mistakes) / self.symbols * 100, ".2f")}%')
        self.show()

    def russian_language(self, time, word):
        if time == 0 or time >= 5:
            time = str(str(time) + str(f" {word}"))
        elif time == 1:
            time = str(str(time) + str(f" {word}а"))
        else:
            time = str(str(time) + str(f" {word}ы"))
        return time


class UserLessons(SwitchBetweenButtons):
    def __init__(self, lesson_number, part):
        super().__init__()
        self.symbols = []
        self.init_ui(lesson_number, part)

    def init_ui(self, lesson_number, part):
        super(UserLessons, self).__init__()
        self.window = uic.loadUi('qt_designer/user_lessons.ui', self)
        for i in range(lesson_number):
            for j in range(len(lessons_letters.get(i + 1))):
                self.symbols.append(lessons_letters.get(i + 1)[j])
        if part == 1:
            print(random.choices((self.symbols), weights=[10, 20000, 10, 10, 10, 20, 10, 10]))
        elif part == 2:
            pass
        else:
            pass
        #  self.window.for_text.setPlainText("".join(self.symbols[::]))
        for i in range(3):
            self.window.findChild(QComboBox, str('lesson_' + str((i + 1)))).activated[str].connect(self.number_lesson)
        #  self.window.findChild(QComboBox, str('lesson_' + str((i + 1)))).currentIndexChanged[str].connect(self.number_lesson)

    def number_lesson(self):
        changed_text_box = str(self.sender().currentText())
        print(changed_text_box[changed_text_box.rfind(" ") - 2], changed_text_box[changed_text_box.rfind(" ") + 1:])
        part = changed_text_box[changed_text_box.rfind(" ") + 1:]
        if part == 'Буквы':
            part_lesson = 1
        elif part == 'Клавишы':
            part_lesson = 2
        else:
            part_lesson = 3
        self.lessons(int(changed_text_box[changed_text_box.rfind(" ") - 2]), part_lesson)


if __name__ == '__main__':
    result = cursor.execute('SELECT user_name '
                            'FROM user_informational').fetchone()
    app = QApplication(sys.argv)
    if not result:
        window = FirstWindow()
    else:
        window = GeneralWindow()
    sys.exit(app.exec_())
