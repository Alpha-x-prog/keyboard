import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5 import uic


class FirstWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.window = None
        self.general_window = None

    def initUI(self):
        super(FirstWindow, self).__init__()
        self.window = uic.loadUi('C:/my_key_board/qt_designer/first_window.ui', self)
        self.window.setWindowTitle('Введите имя')
        self.show()
        self.window.btnfinished.clicked.connect(self.btnClicked)

    def btnClicked(self):
        self.general_window = GeneralWindow()
        self.general_window.show()
        self.close()


class GeneralWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.window = None

    def initUI(self):
        super(GeneralWindow, self).__init__()
        self.window = uic.loadUi('C:/my_key_board/qt_designer/general information.ui', self)
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
        self.initUI()
        self.window = None

    def initUI(self):
        super(Test, self).__init__()
        self.window = uic.loadUi('C:/my_key_board/qt_designer/test.ui', self)
        self.window.setWindowTitle('Проверка скорости')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FirstWindow()
    sys.exit(app.exec_())
