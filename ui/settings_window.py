import PySide6
from PySide6.QtWidgets import QTreeWidgetItem
from core.logic import FileScanner
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl

import sys, os

from PySide6.QtWidgets import *
from ui.ui_add_series import *
from ui.ui_settings import *
from core.db import SettingsDB


class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_SettingsWindow()
        self.ui.setupUi(self)

        db = SettingsDB()
        self.ui.serviceTVDB_lineEdit.setText(db.get("tvdb_key", self.ui.serviceTVDB_lineEdit.text()))
        self.ui.serviceTMDB_lineEdit.setText(db.get("tmdb_key", self.ui.serviceTMDB_lineEdit.text()))
        self.ui.serviceAniList_lineEdit.setText(db.get("anilist_token", self.ui.serviceAniList_lineEdit.text()))
        self.ui.serviceMAL_lineEdit.setText(db.get("mal_token", self.ui.serviceMAL_lineEdit.text()))
        
        self.ui.settings_buttonBox.accepted.connect(self.accept)
        self.ui.settings_buttonBox.rejected.connect(self.reject)
        

    def save_key(self, service):
        if service == "tvdb" and service == "tmdb":
            key = self.ui.serviceTVDB_lineEdit.text()
            db = SettingsDB()
            db.set(service, key)