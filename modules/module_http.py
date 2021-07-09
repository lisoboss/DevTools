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
from requests import Session
from modules.base import BaseModule
from utils.cookies import cookiejar_from_list


LOG = getLogger(__name__)


class Module(BaseModule):
    name = 'http'

    def send(self, method, url, headers, cookies):
        if method not in ('GET', 'POST'):
            return 'method not in (\'GET\', \'POST\')'

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

        text = rp.text

        try:
            text = loads(text)
            return '%s\n\n%s' % (status, dumps(text, ensure_ascii=False, indent=4))
        except:
            return '%s\n\n%s' % (status, text)
    
    def layout(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel('url'), 1)
        url = QLineEdit()
        layout.addWidget(url, 1)
        layout.addWidget(QLabel('headers'), 1)
        headers = QTextEdit()
        layout.addWidget(headers, 5)
        layout.addWidget(QLabel('cookies'), 1)
        cookies = QTextEdit()
        layout.addWidget(cookies, 5)
        layout.addWidget(QLabel('method'), 1)
        method = QLineEdit()
        layout.addWidget(method, 1)
        send = QPushButton('send')
        layout.addWidget(send, 1)
        layout.addWidget(QLabel('text'), 1)
        text = QTextEdit()
        layout.addWidget(text, 30)

        # event

        def callback():
            self.flush(text.setPlainText, 'loadding...')
            try:
                self.flush(text.setPlainText, self.send(method.text(), url.text(), headers.toPlainText(), cookies.toPlainText()))
            except Exception as e:
                LOG.exception(e)
                self.flush(text.setPlainText, str(e))
    
        send.clicked.connect(callback)

        return layout
