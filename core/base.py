#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
from abc import ABCMeta, abstractmethod
from PyQt5.QtWidgets import (
    QApplication,
    QVBoxLayout
)


class BaseModule(metaclass=ABCMeta):
    layout_ = None

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    def draw(self):
        ...

    @staticmethod
    def flush_text(func, text):
        r = func(text)
        QApplication.processEvents()
        sleep(0.1)
        return r

    @property
    def layout(self) -> QVBoxLayout:
        if self.layout_ is None:
            self.layout_ = QVBoxLayout()
        return self.layout_

