#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from rich.logging import RichHandler

from logging import NOTSET
from logging import DEBUG
from logging import INFO
from logging import ERROR
from logging import getLogger
from logging import Formatter
from logging import getLevelName
from logging import StreamHandler
from datetime import datetime


# LOG_LEVEL = 'INFO'
LOG_LEVEL = 'DEBUG'
root_logger = None


class MyFileHandler(StreamHandler):

    def __init__(self, filename, rollover_filename, mode='a', encoding=None, delay=10):

        filename = os.fspath(filename)
        rollover_filename = os.fspath(rollover_filename)
        cache_dir = 'cache'
        os.makedirs(cache_dir, exist_ok=True)
        cache_filename = cache_dir + '/log_time'
        cache_filename = os.fspath(cache_filename)
        self.baseFilename = os.path.abspath(filename)
        self.rollover_filename = os.path.abspath(rollover_filename)
        self.cache_filename = os.path.abspath(cache_filename)
        self.mode = mode
        self.encoding = encoding
        self.delay = delay  # 秒
        self.time_difference = 28800  # 2021-04-09 08:00:00 -> 2021-04-09 00:00:00
        self.now_time = self.format_now_time(local_ok=True)
        StreamHandler.__init__(self, self._open())

    def format_now_time(self, local_ok=False, set_local_ok=False):
        timestamp = int(
            (datetime.now().timestamp() + self.time_difference) / self.delay
        ) * self.delay - self.time_difference
        if local_ok:
            try:
                with open(self.cache_filename, 'r', encoding='utf-8') as f:
                    cache = f.read()
            except Exception as e:
                e = e
                with open(self.cache_filename, 'w', encoding='utf-8') as f:
                    f.write(str(timestamp))
                cache = timestamp
            if cache:
                timestamp = int(cache)
            else:
                with open(self.cache_filename, 'w', encoding='utf-8') as f:
                    f.write(str(timestamp))
        if set_local_ok:
            with open(self.cache_filename, 'w', encoding='utf-8') as f:
                f.write(str(timestamp))
        return datetime.fromtimestamp(timestamp)

    def close(self):
        self.acquire()
        try:
            try:
                if self.stream:
                    try:
                        self.flush()
                    finally:
                        stream = self.stream
                        self.stream = None
                        if hasattr(stream, "close"):
                            stream.close()
            finally:
                # Issue #19523: call unconditionally to
                # prevent a handler leak when delay is set
                StreamHandler.close(self)
        finally:
            self.release()

    def _open(self):
        return open(self.baseFilename, self.mode, encoding=self.encoding)

    def __repr__(self):
        level = getLevelName(self.level)
        return '<%s %s (%s)>' % (self.__class__.__name__, self.baseFilename, level)

    def emit(self, record):

        if self.stream is None:
            self.stream = self._open()
        try:
            self.do_rollover()
            StreamHandler.emit(self, record)
        except Exception as e:
            print(e)
            self.handleError(record)

    def do_rollover(self):
        now_time = self.format_now_time()
        if (now_time - self.now_time).total_seconds() >= self.delay:
            if self.stream:
                self.stream.close()
                self.stream = None
            self.rotator(self.now_time.strftime(self.rollover_filename))
            self.stream = self._open()
            self.now_time = self.format_now_time(set_local_ok=True)

    def rotator(self, target):
        os.rename(self.baseFilename, target)


def init_root_logger(file_name='root'):
    global root_logger
    if root_logger is None:
        root_dir = 'logs'
        os.makedirs(root_dir, exist_ok=True)
        info_dir = f'{root_dir}/info'
        os.makedirs(info_dir, exist_ok=True)
        debug_dir = f'{root_dir}/debug'
        os.makedirs(debug_dir, exist_ok=True)
        error_dir = f'{root_dir}/error'
        os.makedirs(error_dir, exist_ok=True)

        delay = 60 * 60 * 24  # 一天
        file_name_formatter = '%Y-%m-%d.log'
        # file_name_formatter = '%Y-%m-%d_%H-%M-%S.log'

        _logger = getLogger()
        _logger.setLevel(NOTSET)

        for h in _logger.handlers:
            _logger.removeHandler(h)

        #  %(pathname)s
        formatter = Formatter(
            '%(asctime)s [%(levelname)s] [%(name)s] [%(filename)s:%(lineno)d] >>> %(message)s')

        # 屏幕
        #console_handle = StreamHandler()
        console_handle = RichHandler(markup=True)
        if LOG_LEVEL == 'INFO':
            console_handle.setLevel(INFO)
        else:
            console_handle.setLevel(NOTSET)

        # INFO 文件
        # info_file_handle = FileHandler(f'{info_dir}/info.log')
        info_file_handle = MyFileHandler(filename=f'{info_dir}/{file_name}.info.log',
                                         rollover_filename=f'{info_dir}/{file_name}.info.{file_name_formatter}',
                                         mode='a',
                                         encoding='utf-8',
                                         delay=delay)
        info_file_handle.setLevel(INFO)

        # DEBUG 文件
        # debug_file_handle = FileHandler(f'{debug_dir}/debug.log')
        debug_file_handle = MyFileHandler(filename=f'{debug_dir}/{file_name}.debug.log',
                                          rollover_filename=f'{debug_dir}/{file_name}.debug.{file_name_formatter}',
                                          mode='a',
                                          encoding='utf-8',
                                          delay=delay)
        debug_file_handle.setLevel(DEBUG)

        # ERROR 文件
        # error_file_handle = FileHandler(f'{error_dir}/error.log')
        error_file_handle = MyFileHandler(filename=f'{error_dir}/{file_name}.error.log',
                                          rollover_filename=f'{error_dir}/{file_name}.error.{file_name_formatter}',
                                          mode='a',
                                          encoding='utf-8',
                                          delay=delay)
        error_file_handle.setLevel(ERROR)

        # 添加日志格式
        console_handle.setFormatter(formatter)
        info_file_handle.setFormatter(formatter)
        debug_file_handle.setFormatter(formatter)
        error_file_handle.setFormatter(formatter)

        # 添加handles
        _logger.addHandler(console_handle)
        _logger.addHandler(info_file_handle)
        _logger.addHandler(debug_file_handle)
        _logger.addHandler(error_file_handle)

        root_logger = _logger
