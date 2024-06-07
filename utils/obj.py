#!/usr/bin/env python
# -*- coding: utf-8 -*-

from logging import getLogger
from importlib import import_module


LOG = getLogger(__name__)


def load_class(obj_str):
    LOG.debug('loading class %s' , obj_str)
    s = obj_str.split('.')
    module_ = import_module(".".join(s[:-1]))
    return getattr(module_, s[-1])


def load_module(module_str):
    LOG.debug('loading module %s' , module_str)
    module_ = import_module(module_str)
    return module_
