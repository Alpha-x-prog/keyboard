import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication
from PyQt5 import uic
import sqlite3
import random
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget

conn = sqlite3.connect('base_date/base.db')
cursor = conn.cursor()
first_side = ['Ё', 'Ё', 'Ц', 'У', 'К', 'Е', 'Ф', 'Ы', 'В', 'А', 'П', 'Я', 'Ч', 'С', 'М', 'И', '1', '2', '3', '4', '5']


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
        self.init_ui()

    def init_ui(self):
        super(Test, self).__init__()
        self.window = uic.loadUi('qt_designer/test.ui', self)
        self.window.setWindowTitle('Проверка скорости')
        count_str = cursor.execute('SELECT COUNT(1) '
                                   'FROM texts').fetchone()[0]
        id_text = random.randint(1, count_str)
        self.text, symbols = cursor.execute('SELECT text, symbols '
                                            'FROM texts '
                                            'WHERE id = ?', (id_text,)).fetchone()
        self.window.for_text.setPlainText(self.text)
        self.show()
        self.change_color_button_green(ord(self.text[self.count_pressed]))
        self.window.user_text.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj is self.window.user_text and event.type() == QtCore.QEvent.KeyPress:
            if event.text() == self.text[self.count_pressed]:
                self.change_color_button_reverse()
                self.change_color_button_green(ord(self.text[self.count_pressed + 1].upper()))
                self.count_pressed += 1
                return False
            else:
                return True
        return False

    def change_color_button_green(self, number_button):
        self.first_button = 'pushButton_' + str(number_button)
        self.first_color_button = self.window.findChild(QPushButton,
                                                        self.first_button).palette().button().color().name()
        self.window.findChild(QPushButton, self.first_button).setStyleSheet("background-color: #00ff00")
        name_button = self.text[self.count_pressed]
        if name_button.isupper():
            if name_button in first_side:
                self.dop_button_color = self.window.Left_Shift.palette().button().color().name()
                self.window.Left_Shift.setStyleSheet("background-color: #00ff00")
                self.shift_button = 1
            else:
                self.dop_button_color = self.window.Right_Shift.palette().button().color().name()
                self.window.Right_Shift.setStyleSheet("background-color: #00ff00")
                self.shift_button = 2

    def change_color_button_reverse(self):
        self.window.findChild(QPushButton, self.first_button).setStyleSheet(
            f"background-color: {self.first_color_button}")
        if self.shift_button == 1:
            self.window.Left_Shift.setStyleSheet(f"background-color: {self.dop_button_color}")
        elif self.shift_button == 2:
            self.window.Right_Shift.setStyleSheet(f"background-color: {self.dop_button_color}")
        self.shift = 0


if __name__ == '__main__':
    result = cursor.execute('SELECT user_name '
                            'FROM user_informational').fetchone()
    app = QApplication(sys.argv)
    if not result:
        window = FirstWindow()
    else:
        window = GeneralWindow()
    sys.exit(app.exec_())
