import PySide6
from PySide6.QtWidgets import QTreeWidgetItem
from core.logic import FileScanner
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl

import sys, os

from PySide6.QtWidgets import *
from ui.theme import ThemeManager
from ui.ui_add_series import *
from ui.ui_settings import *
from core.db import SettingsDB


class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_SettingsWindow()
        self.ui.setupUi(self)

        db = SettingsDB()
        self.ui.serviceAniList_lineEdit.setText(db.get("anilist_token", self.ui.serviceAniList_lineEdit.text()))
        self.ui.serviceMAL_lineEdit.setText(db.get("mal_token", self.ui.serviceMAL_lineEdit.text()))
        self.ui.files_template_lineEdit.setText(db.get("files_template", self.ui.files_template_lineEdit.text()))
        self.ui.folder_template_lineEdit.setText(db.get("folder_template", self.ui.folder_template_lineEdit.text()))

        if db.get("offline_mode") and db.get("offline_mode") == 'True':
            self.ui.offline_mode_checkBox.setChecked(True)
        else:
            self.ui.offline_mode_checkBox.setChecked(False)

        

        self.ui.settings_buttonBox.accepted.connect(self.accept)
        self.ui.settings_buttonBox.rejected.connect(self.reject)

        
