#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from glob import glob 
from os.path import abspath
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QTabWidget,
    QWidget,
    QMainWindow,
    QVBoxLayout
)
from utils.obj import load_class
from utils.log import init_logger


LOG = init_logger('dev-tools')


class Tab(QTabWidget):

    def __init__(self, parent=None):
        super(Tab, self).__init__(parent)
        self._titles = {}

        # 设置样式 
        # self.setTabShape(QTabWidget.Triangular)
        # self.setDocumentMode(True)
        self.setMovable(True)
        self.setTabsClosable(True)

        self.tabCloseRequested.connect(self.remove)

    def add(self, title, layout):
        tab = QWidget()
        tab.setLayout(layout)
        
        title_number = self._titles.get(title) or 1
        self._titles[title] = title_number + 1
        title = '%s_%s' % (title, title_number)

        index = self.addTab(tab, title)
        self.setCurrentIndex(index)
        return title

    def remove(self, index):
        self.removeTab(index)


class Main(QMainWindow):

    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('DevTools')
        # self.setWindowIconText('./DevTools.icon')

        self.modules = {}
        self.tab = Tab(self)

        layout = QVBoxLayout()
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        
        self.set_bar()
        layout.addWidget(self.tab)

    def get_bar(self, text, func):
        action = QAction(text, self)
        # 为动作添加图标：
        # action_file.setIcon(QIcon('open.png'))
        # 将点击动作的信号连接到 action_open 方法：
        action.triggered.connect(func)
        return action

    @staticmethod
    def create_callback(func, name, layout):
        
        def callback():
            func(name, layout())

        return callback

    def set_bar(self):
        # 创建一个工具栏：
        bar_tool = self.addToolBar('工具栏')
       
        abs_path = abspath('.') + '/'
        module_paths = glob(abs_path + 'modules/module_*.py')
        module_paths.sort()
        for module_path in module_paths: 
            module_class = module_path.replace(abs_path, '').replace('/', '.').replace('.py', '.Module')
            LOG.info('loadding %s' % module_class)
            self.modules[module_class] = load_class(module_class)()

            # 为工具栏添加按钮：
            bar_tool.addAction(self.get_bar(self.modules[module_class].name, self.create_callback(self.tab.add, self.modules[module_class].name, self.modules[module_class].layout)))
            # 为添加分割线：
            bar_tool.addSeparator()

    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
    

