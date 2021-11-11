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
first_side = ['ё','й','ц','у','к','е','ф','ы','в','а','п','я','ч','с','м','и','1','2','3','4','5','','','','','','','','','','','','','']

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
        name_button = 'pushButton_' + str(ord(self.text[0]))
        self.first_color = self.window.findChild(QPushButton, name_button).palette().button().color().name()
        self.window.findChild(QPushButton, name_button).setStyleSheet("background-color: #00ff00")
        self.window.user_text.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj is self.window.user_text and event.type() == QtCore.QEvent.KeyPress:
            if event.text() == self.text[self.count_pressed]:
                self.count_pressed += 1
                return False
            else:
                return True
        return False


if __name__ == '__main__':
    result = cursor.execute('SELECT user_name '
                            'FROM user_informational').fetchone()
    app = QApplication(sys.argv)
    if not result:
        window = FirstWindow()
    else:
        window = GeneralWindow()
    sys.exit(app.exec_())
