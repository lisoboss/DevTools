#!/usr/bin/env python
# -*- coding: utf-8 -*-

from logging import getLogger
from PyQt5.QtWidgets import QAction, QWidget, QMainWindow, QVBoxLayout
from core.ui.tab import Tab
from core.base import BaseModule
from utils.obj import load_modules
import modules


LOG = getLogger(__name__)


class Main(QMainWindow):

    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('DevTools')
        # self.setWindowIconText('./DevTools.icon')
        # 将窗口的位置设置为屏幕坐标 (100, 100)，并将窗口的宽度和高度设置为 400 和 200。
        self.setGeometry(100, 100, 400, 200)

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
    def create_callback(func, Module):
        
        def callback():
            module: BaseModule = Module()
            module.draw()
            func(module.name, module.layout)

        return callback

    def set_bar(self):
        # 创建一个工具栏：
        bar_tool = self.addToolBar('工具栏')

        load_modules(modules)

        for Module in BaseModule.__subclasses__(): 
            LOG.info('add %s' % Module.__class__)

            # 为工具栏添加按钮：
            bar_tool.addAction(self.get_bar(Module.name, self.create_callback(self.tab.add, Module)))
            # 为添加分割线：
            bar_tool.addSeparator()

    