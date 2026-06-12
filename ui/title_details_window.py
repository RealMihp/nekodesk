import PySide6
from PySide6.QtWidgets import QTreeWidgetItem
from core.logic import FileScanner
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl

import sys, os

from PySide6.QtWidgets import *
from ui.ui_add_series import *
from ui.ui_title_details import *
from core.db import *
from core.utils import *



class Title_detailsWindow(QWidget):
    def __init__(self, parent=None, anilist_id: str = None):
        super().__init__(parent, Qt.WindowType.Window)
        self.ui = Ui_details_widget()
        self.ui.setupUi(self)
        self.anilist_id = anilist_id
        self.ldbClient = LibraryDB()
        self.imgmClient = ImageManager()
        self.prefManager = PreferencesManager()
        self.ui.buttonBox.accepted.connect(self.close)
        self.ui.buttonBox.rejected.connect(self.close)
        self.render_details()

    def render_details(self):
        if not self.anilist_id: return
        d = self.ldbClient.get_title(self.anilist_id)
        if not d: return
        title_romaji = d.get('title_romaji')
        title_native = d.get('title_native')
        title_english = d.get('title_english')

        title = self.prefManager.get_title_title(d.get('anilist_id')) or 'Unknown'
        syn_list = set([title_romaji, title_native, title_english, d.get('synonyms')])
        synonyms = ", ".join([s for s in syn_list if s != title and s]) or 'N/A'
        format = f"Type: {d.get('format', 'N/A')}"
        eps = f"Episodes: {d.get('episodes', 'N/A')}"
        status = f"Status: {d.get('status', 'N/A')}".replace('_', ' ')
        score = f"Avg. Score: {d.get('score', 'N/A')}%" if d.get('score') != 'None' else 'N/A'
        season = f"Season: {d.get('season') or ''} {d.get('season_year') or ''}".strip() or 'Season: N/A'
        genres = f"Genres: {d.get('genres', 'N/A')}"
        studio = f"Studio: {d.get('studio', 'N/A')}"
        desc = d.get('desc', 'No description :(')
        poster_link = d.get('poster_large_link')
        poster_color = d.get('poster_color')
        poster = self.imgmClient.get_poster(poster_link, return_pixmap=True) if poster_link else self.imgmClient.get_color_icon(poster_color)
        placeholder_poster = self.imgmClient.get_color_pixmap(poster_color, 460, 690)
        banner_link = d.get('banner_link')
        placeholder_banner = self.imgmClient.get_color_pixmap(poster_color, 1900, 400)
        banner = self.imgmClient.get_poster(banner_link, return_pixmap=True) if banner_link else placeholder_banner

        if not banner.isNull():
            banner = banner.scaledToWidth(800, Qt.TransformationMode.SmoothTransformation)
            self.ui.banner_label.setPixmap(banner)
            

        if not poster.isNull():
            poster = poster.scaledToWidth(210, Qt.TransformationMode.SmoothTransformation)
            self.ui.poster_label.setPixmap(poster)
            self.ui.poster_label.setFixedWidth(210)

        # poster = poster.scaled(
        #     200, 300, 
        #     Qt.AspectRatioMode.KeepAspectRatio, 
        #     Qt.TransformationMode.SmoothTransformation
        # )

                
                
                
        
        self.ui.title_label.setText(title)
        self.ui.synonyms_label.setText(synonyms)
        self.ui.type_label.setText(format)
        self.ui.episodes_label.setText(eps)
        self.ui.status_label.setText(status)
        self.ui.score_label.setText(score)
        self.ui.season_label.setText(season)
        self.ui.genres_label.setText(genres)
        self.ui.studio_label.setText(studio)
        self.ui.desc_label.setText(desc)
        self.ui.poster_label.setPixmap(poster)
        self.ui.banner_label.setPixmap(banner)

        self.ui.poster_label.setFixedSize(poster.size())
        





        
        
        