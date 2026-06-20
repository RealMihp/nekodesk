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

        self.db = SettingsDB()
        self.ui.serviceAniList_lineEdit.setText(self.db.get("anilist_token", self.ui.serviceAniList_lineEdit.text()))
        self.ui.serviceMAL_lineEdit.setText(self.db.get("mal_token", self.ui.serviceMAL_lineEdit.text()))
        self.ui.files_template_lineEdit.setText(self.db.get("files_template", self.ui.files_template_lineEdit.text()))
        self.ui.folder_template_lineEdit.setText(self.db.get("folder_template", self.ui.folder_template_lineEdit.text()))
        self.ui.poster_template_lineEdit.setText(self.db.get("poster_template", self.ui.poster_template_lineEdit.text()))
        self.ui.banner_template_lineEdit.setText(self.db.get("banner_template", self.ui.banner_template_lineEdit.text()))
        self.ui.torrent_template_lineEdit.setText(self.db.get("torrent_template", self.ui.torrent_template_lineEdit.text()))


        title_lang_priority = self.db.get("title_lang_priority", "Romaji,English,Native").split(",")
        self.ui.lang_priority_1_comboBox.setCurrentText(title_lang_priority[0])
        self.ui.lang_priority_2_comboBox.setCurrentText(title_lang_priority[1])
        self.ui.lang_priority_3_comboBox.setCurrentText(title_lang_priority[2])


        if self.db.get("qbit") and self.db.get("qbit") == "True":
            self.ui.qbit_checkBox.setChecked(True)
        else:
            self.ui.qbit_checkBox.setChecked(False)
            self.ui.torrent_template_widget.hide()
        self.handle_checkboxes('qbit_checkBox')
        self.ui.qbit_checkBox.checkStateChanged.connect(lambda: self.handle_checkboxes('qbit_checkBox'))

        self.ui.ip_lineEdit.setText(self.db.get("qbit_ip", "localhost"))
        self.ui.port_doubleSpinBox.setValue(float(self.db.get("qbit_port", 8080))) 
        username = self.db.get("qbit_username", "admin")
        self.ui.username_lineEdit.setText(username)
        password = keyring.get_password("series-library-manager", username)
        self.ui.password_lineEdit.setText(password)


        if self.db.get("offline_mode") and self.db.get("offline_mode") == "True":
            self.ui.offline_mode_checkBox.setChecked(True)
        else:
            self.ui.offline_mode_checkBox.setChecked(False)

    def handle_checkboxes(self, checkbox: str):
        if checkbox == 'qbit_checkBox':
            state = self.ui.qbit_checkBox.isChecked()
            self.ui.ip_lineEdit.setEnabled(state)
            self.ui.port_doubleSpinBox.setEnabled(state)
            self.ui.username_lineEdit.setEnabled(state)
            self.ui.password_lineEdit.setEnabled(state)
            if state == True:
                self.ui.torrent_template_widget.show()
            else:
                self.ui.torrent_template_widget.hide()

        
    def accept(self):
        self.db.set("anilist_token", self.ui.serviceAniList_lineEdit.text())
        self.db.set("mal_token", self.ui.serviceMAL_lineEdit.text())
        self.db.set("files_template", self.ui.files_template_lineEdit.text())
        self.db.set("folder_template", self.ui.folder_template_lineEdit.text())
        self.db.set("poster_template", self.ui.poster_template_lineEdit.text())
        self.db.set("banner_template", self.ui.banner_template_lineEdit.text())
        self.db.set("torrent_template", self.ui.torrent_template_lineEdit.text())

        if self.ui.offline_mode_checkBox.isChecked():
            self.db.set("offline_mode", "True")
        else:
            self.db.set("offline_mode", "False")
        title_lang_priority = f'{self.ui.lang_priority_1_comboBox.currentText()},{self.ui.lang_priority_2_comboBox.currentText()},{self.ui.lang_priority_3_comboBox.currentText()}'
        self.db.set("title_lang_priority", title_lang_priority)
        if self.ui.qbit_checkBox.isChecked():
            self.db.set("qbit", "True")
        else:
            self.db.set("qbit", "False")
        self.db.set("qbit_ip", self.ui.ip_lineEdit.text())
        try:
            port_value = str(int(self.ui.port_doubleSpinBox.value()))
            self.db.set("qbit_port", port_value)
        except TypeError:
            pass
        self.db.set("qbit_port", port_value)
        self.db.set("qbit_username", self.ui.username_lineEdit.text())
        password = self.ui.password_lineEdit.text()
        if password:
            keyring.set_password("series-library-manager", self.ui.username_lineEdit.text(), password)

        super().accept()
        