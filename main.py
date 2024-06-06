#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication
from core.ui.main import Main
from utils.log import init_root_logger

    
if __name__ == "__main__":
    init_root_logger()
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
