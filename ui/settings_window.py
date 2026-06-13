import PySide6
from PySide6.QtWidgets import QTreeWidgetItem
from core.logic import FileScanner
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl

import sys, os
import keyring

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
        self.ui.serviceAniList_lineEdit.setText(db.get("anilist_token", self.ui.serviceAniList_lineEdit.text()))
        self.ui.serviceMAL_lineEdit.setText(db.get("mal_token", self.ui.serviceMAL_lineEdit.text()))
        self.ui.files_template_lineEdit.setText(db.get("files_template", self.ui.files_template_lineEdit.text()))
        self.ui.folder_template_lineEdit.setText(db.get("folder_template", self.ui.folder_template_lineEdit.text()))

        title_lang_priority = db.get("title_lang_priority", "Romaji,English,Native").split(",")
        self.ui.lang_priority_1_comboBox.setCurrentText(title_lang_priority[0])
        self.ui.lang_priority_2_comboBox.setCurrentText(title_lang_priority[1])
        self.ui.lang_priority_3_comboBox.setCurrentText(title_lang_priority[2])


        if db.get("qbit") and db.get("qbit") == "True":
            self.ui.qbit_checkBox.setChecked(True)
        else:
            self.ui.qbit_checkBox.setChecked(False)
        self.handle_checkboxes('qbit_checkBox')
        self.ui.qbit_checkBox.checkStateChanged.connect(lambda: self.handle_checkboxes('qbit_checkBox'))

        self.ui.ip_lineEdit.setText(db.get("qbit_ip", "localhost"))
        self.ui.port_doubleSpinBox.setValue(float(db.get("qbit_port", 8080))) 
        username = db.get("qbit_username", "admin")
        self.ui.username_lineEdit.setText(username)
        password = keyring.get_password("series-library-manager", username)
        self.ui.password_lineEdit.setText(password)


        if db.get("offline_mode") and db.get("offline_mode") == "True":
            self.ui.offline_mode_checkBox.setChecked(True)
        else:
            self.ui.offline_mode_checkBox.setChecked(False)


        self.ui.settings_buttonBox.accepted.connect(self.accept)
        self.ui.settings_buttonBox.rejected.connect(self.reject)

    def handle_checkboxes(self, checkbox: str):
        if checkbox == 'qbit_checkBox':
            state = self.ui.qbit_checkBox.isChecked()
            self.ui.ip_lineEdit.setEnabled(state)
            self.ui.port_doubleSpinBox.setEnabled(state)
            self.ui.username_lineEdit.setEnabled(state)
            self.ui.password_lineEdit.setEnabled(state)

        
