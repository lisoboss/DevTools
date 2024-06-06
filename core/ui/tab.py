#!/usr/bin/env python
# -*- coding: utf-8 -*-


from logging import getLogger
from PyQt5.QtWidgets import QTabWidget, QWidget


LOG = getLogger(__name__)


class Tab(QTabWidget):

    def __init__(self, parent=None):
        super(Tab, self).__init__(parent)
        self._titles = {}

        # 设置样式 
        self.setTabShape(QTabWidget.Triangular)
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

