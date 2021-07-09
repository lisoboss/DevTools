#coding=utf-8
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication

class Example1(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        pass

    def initUI(self):
        self.statusBar().showMessage('Reday')
        self.setGeometry(300, 300, 450, 450)
        self.setWindowTitle('QMainWindow的状态栏demo')
        self.show()
        pass

def main1():
    app = QApplication(sys.argv)
    example = Example1()
    example.show()
    sys.exit(app.exec_())
    pass

if __name__ == '__main__':
    main1()

