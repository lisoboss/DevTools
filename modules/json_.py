#!/usr/bin/env python
# -*- coding: utf-8 -*-

from json import loads, dumps
from logging import getLogger

from PyQt5.QtWidgets import QTextEdit, QPushButton
from core.base import BaseModule


LOG = getLogger(__name__)


class JsonModule(BaseModule):
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

    
    def draw(self):
        f = QPushButton('Format')
        self.layout.addWidget(f, 1)
        uf = QPushButton('UnFormat')
        self.layout.addWidget(uf, 1)
        body = QTextEdit()
        self.layout.addWidget(body, 30)

        # event

        def f_callback():
            text = body.toPlainText()
            self.flush_text(body.setPlainText, 'loadding...')
            try:
                self.flush_text(body.setPlainText, self.format(text))
            except Exception as e:
                LOG.exception(e)
                self.flush_text(body.setPlainText, 'not json %s' % str(e))

        def uf_callback():
            text = body.toPlainText()
            self.flush_text(body.setPlainText, 'loadding...')
            try:
                self.flush_text(body.setPlainText, self.unformat(text))
            except Exception as e:
                LOG.exception(e)
                self.flush_text(body.setPlainText, str(e))
    
        f.clicked.connect(f_callback)
        uf.clicked.connect(uf_callback)
