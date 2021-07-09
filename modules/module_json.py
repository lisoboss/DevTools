#!/usr/bin/env python
# -*- coding: utf-8 -*-

from json import loads, dumps
from logging import getLogger
from PyQt5.QtWidgets import (
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
    QPushButton,
)
from modules.base import BaseModule


LOG = getLogger(__name__)


class Module(BaseModule):
    name = 'json'

    def format(self, text):
        if not text:
            return 'text is null'

        text = loads(text)
        text = dumps(text, ensure_ascii=False, indent=4)

        return text

    def unformat(self, text):
        if not text:
            return 'text is null'

        text = loads(text)
        text = dumps(text)

        return text

    
    def layout(self):
        layout = QVBoxLayout()

        f = QPushButton('Format')
        layout.addWidget(f, 1)
        uf = QPushButton('UnFormat')
        layout.addWidget(uf, 1)
        body = QTextEdit()
        layout.addWidget(body, 30)

        # event

        def f_callback():
            text = body.toPlainText()
            self.flush(body.setPlainText, 'loadding...')
            try:
                self.flush(body.setPlainText, self.format(text))
            except Exception as e:
                LOG.exception(e)
                self.flush(body.setPlainText, 'not json %s' % str(e))

        def uf_callback():
            text = body.toPlainText()
            self.flush(body.setPlainText, 'loadding...')
            try:
                self.flush(body.setPlainText, self.unformat(text))
            except Exception as e:
                LOG.exception(e)
                self.flush(body.setPlainText, str(e))
    
        f.clicked.connect(f_callback)
        uf.clicked.connect(uf_callback)

        return layout
    
        send.clicked.connect(callback)

        return layout
