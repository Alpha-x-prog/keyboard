import sys
from PyQt5 import QtWidgets, QtCore, QtGui, uic
from PyQt5.QtWidgets import QApplication
import sqlite3
import random
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import math
import tkinter as tk

conn = sqlite3.connect('base_date/base.db')
cursor = conn.cursor()
key_board = ["а", "б", "в", "г", "д", "е", "ё", "ж", "з", "и", "й", "к", "л", "м", "н", "о",
             "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "ъ", "ы", "ь", "э", "ю", "я",
             "-", "=", "\"", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
first_side = ['Ё', 'Ё', 'Ц', 'У', 'К', 'Е', 'Ф', 'Ы', 'В', 'А', 'П', 'Я', 'Ч', 'С', 'М', 'И', '1', '2', '3', '4', '5']
additional_characters = {ord('"'): ['Left_Shift', 2], ord(':'): ['Right_Shift', 6], ord(","): ['Right_Shift', '.']}
lessons_letters = {1: ['ф', 'ы', 'в', 'а', 'о', 'л', 'д', 'ж'], 2: ['п', 'р'], 3: ['к', 'г', 'е', 'н'],
                   4: ['м', 'ь', 'и', 'т'], 5: ['у', 'ш', 'с', 'б'], 6: ['ц', 'ч', 'щ', 'ю'],
                   7: ['й', 'я', 'з', 'х', 'ъ', 'э'], 8: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']}
special_symb = [16777217, 16777219, 16777220]


# conn.close()


class SwitchBetweenButtons(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.window = None
        self.user_test = None
        self.user_lessons = None
        root = tk.Tk()
        self.height = root.winfo_screenwidth()
        self.width = root.winfo_screenheight()
        self.setFixedSize(self.height, self.width - 70)
        self.move(0, 0)

    def testing(self):
        self.user_test = Test()
        self.user_test.show()
        self.close()

    def lessons(self, lesson_number, part):
        self.user_lessons = UserLessons(lesson_number, part)
        self.user_lessons.show()
        self.close()

    def info(self):
        self.general_window = GeneralWindow()
        self.general_window.show()
        self.close()

    def prof(self):
        self.profile = Profile()
        self.profile.show()
        self.close()


class ButtonsClick(SwitchBetweenButtons):
    def __init__(self):
        super().__init__()
        self.text = None
        self.dop_button_color = None
        self.first_button = None
        self.result_typ = None
        self.first_color_button = None
        self.shift_button = None
        self.first_press = 1
        self.shift = None
        self.count_pressed = 0
        self.count_user_number_lesson = 1
        self.timer = QTimer(self)
        self.symbols_for_text = []
        self.first_red_button_name = None
        self.first_red_button_color = None
        self.flag = 0
        self.shift_flag = 0
        self.shift_name = None
        self.shift_color = None
        self.mistakes = 0
        self.symbols = None

    def eventFilter(self, obj, event):
        if obj is self.window.user_text and event.type() == QtCore.QEvent.KeyPress:
            if self.first_press == 1:
                self.timer.start(1000)
                self.first_press = 0
            if event.text() == self.text[self.count_pressed]:
                self.window.english.setVisible(False)
                self.change_color_button_reverse_green()
                self.change_color_button_reverse_red()
                self.change_shift_reverse_red()
                self.count_pressed += 1
                if self.count_pressed >= self.symbols:
                    if self.us_lessons == 1:
                        return self.lesson_repeat(1)
                    elif self.us_lessons == 2:
                        return self.lesson_repeat(2)
                    elif self.us_lessons == 3:
                        return self.lesson_repeat(3)
                    else:

                        self.result_typ = ResultTyping(self.count_time, self.mistakes, self.symbols)
                        self.result_typ.show()
                        self.timer.stop()
                        self.close()
                else:
                    self.change_color_button_green(ord(self.text[self.count_pressed].upper()))
                return False
            else:
                self.window.english.setVisible(False)
                if event.text():
                    self.change_color_button_reverse_red()
                    self.change_shift_reverse_red()
                    self.change_color_button_reverse_red()
                    if event.key() in special_symb:
                        self.flag = 1
                        self.change_color_button_red(event.key())
                    else:
                        self.mistakes += 1
                        if event.text().lower() not in key_board and event.text().isalpha():
                            self.window.english.setVisible(True)
                        else:
                            if self.text[self.count_pressed] in additional_characters:
                                pass
                            elif self.text[self.count_pressed] == " " or self.text[self.count_pressed].isdigit():
                                if event.text().isupper():
                                    self.shift_flag = 1
                                    self.change_shift_red(event.text().upper())
                                    self.flag = 1
                                    self.change_color_button_red(event.text().upper())
                                else:
                                    self.flag = 1
                                    self.change_color_button_red(event.text().upper())
                            elif self.text[self.count_pressed].isupper():
                                if event.text().islower():
                                    if event.text() != self.text[self.count_pressed].lower():
                                        self.flag = 1
                                        self.change_color_button_red(event.text().upper())
                                else:
                                    self.flag = 1
                                    self.change_color_button_red(event.text().upper())
                            elif self.text[self.count_pressed].islower():
                                if event.text().isupper():
                                    self.shift_flag = 1
                                    self.change_shift_red(event.text().upper())
                                    if event.text().lower() != self.text[self.count_pressed]:
                                        self.flag = 1
                                        self.change_color_button_red(event.text().upper())
                                else:
                                    self.flag = 1
                                    self.change_color_button_red(event.text().upper())
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
        #    x = self.window.findChild(QPushButton, self.first_button).QStyle()

        #   self.window.findChild(QPushButton, self.first_button).setStyleSheet(" border-width: 1px; border-style: solid;        border-color: black;        border-style: outset;        border-radius: 10px;                                                                            background-color: '#00ff00'")
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

    def change_color_button_red(self, button):
        if button in special_symb:
            self.first_red_button_name = 'pushButton_' + str(button)
        else:
            self.first_red_button_name = 'pushButton_' + str(ord(button))
        self.first_red_button_color = self.window.findChild(QPushButton,
                                                            self.first_red_button_name).palette().button().color().name()
        self.window.findChild(QPushButton, self.first_red_button_name).setStyleSheet(f"background-color: red")

    def change_color_button_reverse_red(self):
        if self.flag == 0:
            pass
        else:
            self.window.findChild(QPushButton, self.first_red_button_name).setStyleSheet(
                f"background-color: {self.first_red_button_color}")
            self.flag = 0

    def change_shift_red(self, button):
        if button not in first_side:
            self.shift_name = 'Left_Shift'
        else:
            self.shift_name = 'Right_Shift'
        self.shift_color = self.window.findChild(QPushButton,
                                                 self.shift_name).palette().button().color().name()
        self.window.findChild(QPushButton, self.shift_name).setStyleSheet(f"background-color: red")

    def change_shift_reverse_red(self):
        if self.shift_flag == 0:
            pass
        else:
            self.window.findChild(QPushButton, self.shift_name).setStyleSheet(
                f"background-color: {self.shift_color}")
            self.shift_flag = 0

    def showTime(self):
        self.count_time += 1
        self.window.time.setText(str(self.count_time // 60) + "." + str(self.count_time % 60).zfill(2))

    def random_letters_part_1(self, a):
        text = ""
        for j in range(26):
            text += str(random.choices(self.symbols_user, weights=a)[0]) + " "
        self.text = text
        self.symbols = len(text) - 1
        self.window.for_text.setPlainText(text)
        self.window.user_text.setPlainText("")

    def random_letters_part_2(self, a):
        text = ""
        while len(text) < 40:
            for i in range(random.randint(3, 6)):
                text += str(random.choices(self.symbols_user, weights=a)[0])
            text += ' '
        self.text = text
        self.symbols = len(self.text) - 1
        self.window.for_text.setPlainText(text)
        self.window.user_text.setPlainText("")

    def random_letters_part_3(self):
        f = open(f'words/lesson{self.lesson_number}.txt')
        lines = f.readlines()
        words = []
        len_lesson_word = len(lines) - 1
        while len(' '.join(words)) <= 20:
            words.append(lines[random.randint(0, len_lesson_word)].strip())
        self.text = ' '.join(words)
        self.symbols = len(self.text)
        self.window.for_text.setPlainText(self.text)
        self.window.user_text.setPlainText("")
        f.close()

    def random_letters_part_4(self):
        numbers = lessons_letters[8]
        text = ""
        for j in range(29):
            text += str(random.choices(numbers)[0]) + " "
        self.text = text
        self.symbols = len(text) - 1
        self.window.for_text.setPlainText(text)
        self.window.user_text.setPlainText("")

    def random_letters_part_5(self):
        numbers = lessons_letters[8]
        text = ""
        while len(text) < 40:
            for i in range(random.randint(3, 6)):
                text += str(random.choices(numbers)[0])
            text += ' '
        self.text = text
        self.symbols = len(self.text) - 1
        self.window.for_text.setPlainText(text)
        self.window.user_text.setPlainText("")


    def table_result(self, view, time, mistakes, symbols, percent):
        max_id = cursor.execute('SELECT MAX(id) '
                                'FROM history').fetchone()[0]
        if max_id is None:
            max_id = 1
        else:
            max_id += 1
        cursor.execute('INSERT INTO history '
                       '(id, view, time, mistakes, symbols, clean_text) '
                       f'VALUES ({max_id}, "{view}", {time}, {mistakes}, {symbols}, {percent})')
        conn.commit()

    def count_result(self, time, mistakes, symbols, view):
        if view == "lesson":
            symbols *= 3
        minutes, second = self.russian_language(time // 60, 'минут'), self.russian_language(
            time % 60, 'секунд')
        self.window.times_result.setText(f'{minutes} {second}')
        self.window.speed_result.setText(f'{int(symbols / time * 60)} симв/мин')
        self.window.count_mistakes_result.setText(f'{mistakes}')
        percent = ((symbols - mistakes) / symbols) * 100
        if percent <= 0:
            self.window.percent_text_result.setText('0%')
            percent = 0
        else:
            self.window.percent_text_result.setText(
                f'{format(((symbols - mistakes) / symbols) * 100, ".2f")}%')
            percent = f'{format(percent, ".2f")}'
        self.table_result(view, time, mistakes, symbols, percent)

    def russian_language(self, time, word):
        if time == 0 or time >= 5:
            time = str(str(time) + str(f" {word}"))
        elif time == 1:
            time = str(str(time) + str(f" {word}а"))
        else:
            time = str(str(time) + str(f" {word}ы"))
        return time

    def lesson_repeat(self, number):
        if self.count_user_number_lesson == 3:
            self.window.my_result.setVisible(True)
            a = ['times', 'speed', 'percent_text', 'count_mistakes']
            for i in range(4):
                self.window.findChild(QLabel, a[i]).setVisible(True)
                self.window.findChild(QLabel, str(a[i]) + '_result').setVisible(True)
            self.window.user_text.deleteLater()
            self.window.for_text.setVisible(False)
            self.timer.stop()
            self.count_result(self.count_time, self.mistakes, self.symbols, 'lesson')
            self.count_user_number_lesson = 1
            return False
        else:
            self.count_pressed = 0
            if number == 1:
                self.random_letters_part_1(self.symbols_for_text)
            elif number == 2:
                self.random_letters_part_2(self.symbols_for_text)
            elif number == 3:
                self.random_letters_part_3()
            self.count_user_number_lesson += 1
            return True


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
        self.window.btn_testing.clicked.connect(self.testing)
        self.window.btn_user_lessons.clicked.connect(lambda: self.lessons(1, 1))
        self.window.btn_informational.clicked.connect(self.info)
        self.window.btn_profile.clicked.connect(self.prof)
        self.show()


class Test(ButtonsClick):
    def __init__(self):
        super().__init__()
        self.window = None
        self.count_pressed = 0
        self.text = None
        self.symbols = None
        self.count_time = 0
        self.timer = None
        self.first_press = 1
        self.us_lessons = 0
        self.init_ui()

    def init_ui(self):
        super(Test, self).__init__()
        self.window = uic.loadUi('qt_designer/test.ui', self)
        self.window.setWindowTitle('Проверка скорости')

        self.timer.timeout.connect(self.showTime)

        count_str = cursor.execute('SELECT COUNT(1) '
                                   'FROM texts').fetchone()[0]
        id_text = random.randint(1, count_str)
        self.text, self.symbols = cursor.execute('SELECT text, symbols '
                                                 'FROM texts '
                                                 'WHERE id = ?', (5,)).fetchone()  # текст
        self.window.for_text.setPlainText(self.text)
        self.window.english.setVisible(False)
        self.window.btn_testing.clicked.connect(self.testing)
        self.window.btn_user_lessons.clicked.connect(lambda: self.lessons(1, 1))
        self.window.btn_informational.clicked.connect(self.info)
        self.window.btn_profile.clicked.connect(self.prof)
        self.show()
        self.change_color_button_green(ord(self.text[self.count_pressed]))
        self.window.user_text.installEventFilter(self)


class ResultTyping(ButtonsClick):
    def __init__(self, time, mistakes, symbols):
        super().__init__()
        self.window = None
        self.time_typing = time
        self.user_mistakes = mistakes
        self.symbols_text = symbols
        self.init_ui()

    def init_ui(self):
        super(ResultTyping, self).__init__()
        self.window = uic.loadUi('qt_designer/result_test.ui', self)
        print(self.time_typing, self.user_mistakes, self.symbols_text, "text")
        self.count_result(self.time_typing, self.user_mistakes, self.symbols_text, "text")

        self.window.btn_testing.clicked.connect(self.testing)
        self.window.btn_user_lessons.clicked.connect(lambda: self.lessons(1, 1))
        self.window.btn_informational.clicked.connect(self.info)
        self.window.btn_profile.clicked.connect(self.prof)
        self.show()


class UserLessons(ButtonsClick):
    def __init__(self, lesson_number, part):
        super().__init__()
        self.symbols_user = []
        self.text = None
        self.window = None
        self.text = None
        self.symbols = None
        self.count_time = 0
        self.mistakes = 0
        self.timer = None
        self.first_press = 1
        self.us_lessons = None
        self.lesson_number = lesson_number
        self.init_UI(part)

    def init_UI(self, part):
        super(UserLessons, self).__init__()
        self.window = uic.loadUi('qt_designer/user_lessons.ui', self)
        main_letters = lessons_letters.get(self.lesson_number)
        self.timer.timeout.connect(self.showTime)
        self.window.btn_testing.clicked.connect(self.testing)
        self.window.btn_user_lessons.clicked.connect(lambda: self.lessons(1, 1))
        self.window.btn_informational.clicked.connect(self.info)
        self.window.btn_profile.clicked.connect(self.prof)
        self.window.english.setVisible(False)
        self.window.my_result.setVisible(False)
        self.window.name_lesson.setText(f'Урок {self.lesson_number} часть {part}')
        a = ['times', 'speed', 'percent_text', 'count_mistakes']
        for i in range(4):
            self.window.findChild(QLabel, a[i]).setVisible(False)
            self.window.findChild(QLabel, str(a[i]) + '_result').setVisible(False)
        self.show()
        if part in [1, 2]:
            for i in range(self.lesson_number):
                for j in range(len(lessons_letters.get(i + 1))):
                    self.symbols_user.append(lessons_letters.get(i + 1)[j])
            for i in range(len(self.symbols_user)):
                if self.symbols_user[i] in main_letters:
                    self.symbols_for_text.append(30)
                else:
                    self.symbols_for_text.append(10)
        if part == 1:
            self.us_lessons = 1
            self.random_letters_part_1(self.symbols_for_text)
            self.change_color_button_green(ord(self.text[self.count_pressed].upper()))
            self.window.user_text.installEventFilter(self)
        elif part == 2:
            self.us_lessons = 2
            self.random_letters_part_2(self.symbols_for_text)
            self.change_color_button_green(ord(self.text[self.count_pressed].upper()))
            self.window.user_text.installEventFilter(self)
        elif part == 3:
            self.us_lessons = 3
            self.random_letters_part_3()
            self.change_color_button_green(ord(self.text[self.count_pressed].upper()))
            self.window.user_text.installEventFilter(self)
        elif part == 4:
            self.us_lessons = 4
            self.random_letters_part_4()
            self.change_color_button_green(ord(self.text[self.count_pressed].upper()))
            self.window.user_text.installEventFilter(self)
        elif part == 5:
            self.us_lessons = 5
            self.random_letters_part_5()
            self.change_color_button_green(ord(self.text[self.count_pressed].upper()))
            self.window.user_text.installEventFilter(self)
        for i in range(8):
            self.window.findChild(QComboBox, str('lesson_' + str((i + 1)))).activated[str].connect(self.number_lesson)

    def number_lesson(self):
        changed_text_box = str(self.sender().currentText())
        #  print(changed_text_box[changed_text_box.rfind(" ") - 2], changed_text_box[changed_text_box.rfind(" ") + 1:])
        part = changed_text_box[changed_text_box.rfind(" ") + 1:]
        if part == 'Цифры-1':
            part_lesson = 4
        elif part == 'Цифры-2':
            part_lesson = 5
        elif part == 'Буквы':
            part_lesson = 1
        elif part == 'Клавишы':
            part_lesson = 2
        else:
            part_lesson = 3
        self.lessons(int(changed_text_box[changed_text_box.rfind(" ") - 2]), part_lesson)


class Profile(ButtonsClick):
    def __init__(self):
        super().__init__()
        self.window = None
        self.init_ui()

    def init_ui(self):
        super(Profile, self).__init__()
        self.window = uic.loadUi('qt_designer/profile.ui', self)
        self.window.setWindowTitle('Профиль')
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
