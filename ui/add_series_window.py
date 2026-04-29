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
        self.ldbclient = LibraryDB()
        self.search_data_cache = []

        self.ui.AniList_radioButton.setChecked(True)
        self.ui.search_pushButton.pressed.connect(self.populate_search_tree)
        self.ui.search_pushButton.setEnabled(True)

        self.ui.search_treeWidget.itemSelectionChanged.connect(lambda: self.ui.search_add_pushButton.setEnabled(True))

        self.ui.search_add_pushButton.pressed.connect(self.handle_add_series)
        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)


    def populate_search_tree(self):
        query = self.ui.search_lineEdit.text()
        if not query:
            return
        imgm = ImageManager()

        self.ui.search_treeWidget.clear()
        self.search_data_cache = []
        self.ui.search_treeWidget.setIconSize(QSize(64, 96))

        if self.ui.AniList_radioButton.isChecked():
            client = AniListClient()
            results = client.search_title(query)
            
            if not results:
                return
            
            self.search_data_cache = results

            links = [r.get('coverImage', {}).get('medium') for r in results if r.get('coverImage')]
            
            imgm = ImageManager()
            posters_map = imgm.get_posters(links, session=client.session, is_temp=True)

            for result in results:
                title = result.get('title', {}).get('romaji') or "Unknown Title"
                year = str(result.get('seasonYear') or "N/A")
                status = result.get('status') or "Unknown"
                anime_id = str(result.get('id'))
                
                link = result.get('coverImage', {}).get('medium')
                color = result.get('coverImage', {}).get('color')
                pixmap = posters_map.get(link, (None, None))[0]
                
                item = QTreeWidgetItem([title, year, status])
                
                if pixmap and not pixmap.isNull():
                    item.setIcon(0, QIcon(pixmap))
                else:
                    pixmap = imgm.get_color_icon(color)
                    item.setIcon(0, QIcon(pixmap))
                
                item.setData(0, ID_ROLE, anime_id)
                self.ui.search_treeWidget.addTopLevelItem(item)

    def handle_add_series(self):
        selected_items = self.ui.search_treeWidget.selectedItems()
        if not selected_items:
            return

        item = selected_items[0]
        
        index = self.ui.search_treeWidget.indexOfTopLevelItem(item)
        
        if 0 <= index < len(self.search_data_cache):
            self.ldbclient.add_title(self.search_data_cache[index])