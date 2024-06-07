#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Zimo
# @Time    : 2024/6/7 09:25
# @File    : csdn.py
# @Software: PyCharm
# @contact : 2319899766@qq.com
# @Site    : https://blog.csdn.net/qq_39799322


from json import loads, dumps
from logging import getLogger

from PyQt5.QtWidgets import QTextEdit, QPushButton, QLineEdit, QLabel, QWidget, QHBoxLayout
from core.base import BaseModule
from plugins.csdn.csdn_download import spider_csdn

LOG = getLogger(__name__)


class CSDNModule(BaseModule):
    name = 'download-csdn'

    def draw(self):

        w1_825408 = QWidget()
        l1_829920 = QHBoxLayout()
        w1_825408.setLayout(l1_829920)
        self.layout.addWidget(w1_825408, 1)

        # url:
        l1_829920.addWidget(QLabel("url:"), 1)

        # QLineEdit
        url = QLineEdit()
        l1_829920.addWidget(url, 30)

        w1_841696 = QWidget()
        l1_842112 = QHBoxLayout()
        w1_841696.setLayout(l1_842112)
        self.layout.addWidget(w1_841696, 1)

        # path
        l1_842112.addWidget(QLabel("path"), 1)

        # QLineEdit
        path = QLineEdit("./tmp")
        l1_842112.addWidget(path, 30)

        # QPushButton
        button_download = QPushButton("download")
        self.layout.addWidget(button_download, 1)

        # QTextEdit
        text_log = QTextEdit()
        self.layout.addWidget(text_log, 30)

        def callback():
            self.flush_text(text_log.setPlainText, 'loadding...')
            try:
                spider_csdn(url.text(), path.text())
                self.flush_text(text_log.setPlainText, 'ok')
            except Exception as e:
                LOG.exception(e)
                self.flush_text(text_log.setPlainText, str(e))

        button_download.clicked.connect(callback)
