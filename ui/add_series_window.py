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
            client = AniListClient()
            results = client.search_title(query)
            
            if not results:
                return


            links = [r.get('coverImage', {}).get('extraLarge') for r in results if r.get('coverImage')]
            
            imgm = ImageManager()
            posters_map = imgm.get_posters(links, session=client.session)

            for result in results:
                title = result.get('title', {}).get('romaji') or "Unknown Title"
                year = str(result.get('seasonYear') or "N/A")
                status = result.get('status') or "Unknown"
                anime_id = str(result.get('id'))
                
                link = result.get('coverImage', {}).get('extraLarge')
                color = result.get('coverImage', {}).get('color')
                pixmap = posters_map.get(link)
                
                item = QTreeWidgetItem([title, year, status])
                
                if pixmap and not pixmap.isNull():
                    item.setIcon(0, QIcon(pixmap))
                else:
                    pixmap = imgm.get_color_icon(color)
                    item.setIcon(0, QIcon(pixmap))
                
                item.setData(0, ID_ROLE, anime_id)
                self.ui.search_treeWidget.addTopLevelItem(item)