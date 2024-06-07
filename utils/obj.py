#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from logging import getLogger
from pkgutil import iter_modules
from importlib import import_module
from importlib.util import module_from_spec


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


def load_modules(parent):
    for importer, module_name, is_package in iter_modules(parent.__path__):
        module_name = f'{parent.__name__}.{module_name}'
        spec = importer.find_spec(module_name)
        module = module_from_spec(spec)
        sys.modules[module_name] = module
        if is_package:
            load_modules(module)
        else:
            spec.loader.exec_module(module)
