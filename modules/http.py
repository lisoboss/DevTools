#!/usr/bin/env python
# -*- coding: utf-8 -*-

from json import loads, dumps
from logging import getLogger
from PyQt5.QtWidgets import QLabel, QLineEdit, QTextEdit, QPushButton, QComboBox
from requests import Session
from core.base import BaseModule
from utils.cookies import cookiejar_from_list


LOG = getLogger(__name__)


class HttpModule(BaseModule):
    name = 'http'

    def send(self, method, url, headers, cookies, encode):
        if not url:
            return 'url is null'

        if headers:
            try:
                headers = loads(headers)
            except Exception as e:
                LOG.exception(e)
                return 'headers is not json -> %s' % e
        else:
            headers = None

        if cookies:
            try:
                cookies = loads(cookies)
            except Exception as e:
                LOG.exception(e)
                return 'cookies is not json -> %s' % e

        se = Session()
        if cookies:
            se.cookies = cookiejar_from_list(cookies)

        rp = se.request(method, url, headers=headers)

        status = '%s' % rp

        rp.encoding = encode
        text = rp.text

        try:
            text = loads(text)
            return '%s\n\n%s' % (status, dumps(text, ensure_ascii=False, indent=4))
        except:
            return '%s\n\n%s' % (status, text)
    
    def draw(self):
        self.layout.addWidget(QLabel('url'), 1)
        url = QLineEdit()
        self.layout.addWidget(url, 1)
        self.layout.addWidget(QLabel('headers'), 1)
        headers = QTextEdit()
        self.layout.addWidget(headers, 5)
        self.layout.addWidget(QLabel('cookies'), 1)
        cookies = QTextEdit()
        self.layout.addWidget(cookies, 5)
        self.layout.addWidget(QLabel('method'), 1)
        method = QComboBox()
        method.addItem('GET')
        method.addItem('POST')
        method.addItem('PUT')
        method.addItem('HEAD')
        method.addItem('DELETE')
        method.addItem('OPTIONS')
        method.addItem('TRACE')
        method.addItem('CONNECT')
        self.layout.addWidget(method, 1)
        send = QPushButton('send')
        self.layout.addWidget(send, 1)

        self.layout.addWidget(QLabel('encode'), 1)
        encode = QLineEdit('UTF-8')
        self.layout.addWidget(encode, 5)

        self.layout.addWidget(QLabel('text'), 1)
        text = QTextEdit()
        self.layout.addWidget(text, 30)

        # event

        def callback():
            self.flush_text(text.setPlainText, 'loadding...')
            try:
                self.flush_text(text.setPlainText, self.send(method.currentText(), url.text(), headers.toPlainText(), cookies.toPlainText(), encode.text()))
            except Exception as e:
                LOG.exception(e)
                self.flush_text(text.setPlainText, str(e))
    
        send.clicked.connect(callback)
