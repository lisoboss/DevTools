#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
from PyQt5.QtWidgets import (
    QApplication,
    QVBoxLayout
)


class BaseModule:
    name = 'base'

    @staticmethod
    def flush(set_func, obj):
        r = set_func(obj)
        QApplication.processEvents()
        sleep(0.1)
        return r

    def layout(self):
        return QVBoxLayout()

