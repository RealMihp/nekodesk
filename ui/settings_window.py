import PySide6
from PySide6.QtWidgets import QTreeWidgetItem
from core.logic import FileScanner
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl

import sys, os

from PySide6.QtWidgets import *
from ui.ui_add_series import *
from ui.ui_settings import *



class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_SettingsWindow()
        self.ui.setupUi(self)
        
        self.ui.settings_buttonBox.accepted.connect(self.accept)
        self.ui.settings_buttonBox.rejected.connect(self.reject)