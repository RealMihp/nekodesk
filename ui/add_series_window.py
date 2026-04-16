import PySide6
from PySide6.QtWidgets import QTreeWidgetItem
from core.logic import FileScanner
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl

import sys, os

from PySide6.QtWidgets import *
from ui.ui_add_series import *
from ui.ui_settings import *
from core.db import *
from core.utils import *
from core.api.anilist_api import *

ID_ROLE = 32

class AddSeriesWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_AddSeriesWindow()
        self.ui.setupUi(self)

        self.ui.AniList_radioButton.setChecked(True)
        self.ui.search_pushButton.pressed.connect(self.populate_search_tree)
        self.ui.search_pushButton.setEnabled(True)

        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)


    def populate_search_tree(self):
        query = self.ui.search_lineEdit.text()
        if not query:
            return
        imgm = ImageManager()

        self.ui.search_treeWidget.clear()
        self.ui.search_treeWidget.setIconSize(QSize(64, 96))

        if self.ui.AniList_radioButton.isChecked():
            Client = AniListClient()
            results = Client.search_title(query)

            for result in results:
                title = result.get('title', {}).get('romaji') or "Unknown Title"
                year = str(result.get('seasonYear') or "N/A")
                status = result.get('status') or "Unknown"
                anime_id = str(result.get('id'))
                poster = imgm.get_poster(result.get('coverImage', {}).get('extraLarge'))
                item = QTreeWidgetItem([title, year, status])
                item.setIcon(0, poster)
                item.setData(0, ID_ROLE, anime_id)

                self.ui.search_treeWidget.addTopLevelItem(item)