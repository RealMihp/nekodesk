import PySide6
from PySide6.QtWidgets import QTreeWidgetItem
from core.logic import FileScanner
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl

import sys, os

from PySide6.QtWidgets import *
from ui.ui_about import *
from core.db import *
from core.utils import *



class AboutWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowType.Window)
        self.ui = Ui_about_widget()
        self.ui.setupUi(self)
        
        self.ui.about_text_label.setText('Icon')
        self.ui.app_name_label.setText('Series Library Manager')
        self.ui.about_text_label.setText('')