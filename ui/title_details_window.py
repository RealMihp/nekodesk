import webbrowser

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
    def __init__(self, parent=None, widget: QTreeWidget = None, anilist_id: str = None):
        super().__init__(parent, Qt.WindowType.Window)
        self.ui = Ui_details_widget()
        self.ui.setupUi(self)
        self.parent = parent
        if not widget:
            return
        self.anilist_id = anilist_id
        self.ldbClient = self.select_db(widget)
        self.imgmClient = ImageManager()
        self.prefManager = PreferencesManager(self.ldbClient)
        self.ui.buttonBox.accepted.connect(self.close)
        self.ui.buttonBox.rejected.connect(self.close)
        self.ui.poster_label.mousePressEvent = lambda event: self.open_link()
        self.render_details()

    def select_db(self, widget = None):
        if widget == self.parent.ui.library_treeWidget:
            db = LibraryDB('data/local_library.db')
            return db
        
        anilist_widgets = {
            'CURRENT': self.parent.ui.anilist_current_library_treeWidget,
            'REPEATING': self.parent.ui.anilist_repeating_library_treeWidget,
            'PLANNING': self.parent.ui.anilist_planning_library_treeWidget,
            'COMPLETED': self.parent.ui.anilist_completed_library_treeWidget,
            'DROPPED': self.parent.ui.anilist_dropped_library_treeWidget,
            'PAUSED': self.parent.ui.anilist_paused_library_treeWidget
        }
        shikimori_widgets = {
            'CURRENT': self.parent.ui.shikimori_watching_library_treeWidget,
            'REPEATING': self.parent.ui.shikimori_rewatching_library_treeWidget,
            'PLANNING': self.parent.ui.shikimori_planned_library_treeWidget,
            'COMPLETED': self.parent.ui.shikimori_completed_library_treeWidget,
            'DROPPED': self.parent.ui.shikimori_dropped_library_treeWidget,
            'PAUSED': self.parent.ui.shikimori_on_hold_library_treeWidget
        }
        for list, al_widget in anilist_widgets.items():
            if widget == al_widget:
                db = LibraryDB(f'data/anilist/{list.lower()}.db')
                return db
        for list, sh_widget in shikimori_widgets.items():
            if widget == sh_widget:
                db = LibraryDB(f'data/shikimori/{list.lower()}.db')
                return db
        

    def render_details(self):
        if not self.anilist_id: return
        d = self.ldbClient.get_title(self.anilist_id)
        if not d: return
        
        title_romaji = d.get('title_romaji')
        title_native = d.get('title_native')
        title_english = d.get('title_english')
        s_val = d.get('season') or ''
        y_val = d.get('season_year') or ''
        genres_list = d.get('genres')

        title = self.prefManager.get_title_title(d.get('anilist_id')) or 'Unknown'
        syn_list = set([title_romaji, title_native, title_english, d.get('synonyms')])
        synonyms = ", ".join([s for s in syn_list if s != title and s]) or 'N/A'
        
        format = d.get('format', 'N/A')
        if format == 'MOVIE':
            format = 'Movie'
        elif format == 'TV_SHORT':
            format = 'TV Short'
        elif format == 'SPECIAL':
            format = 'Special'
        format = f'Type: {format}'
        
        eps = f"Episodes: {d.get('episodes')}" if d.get('episodes') else 'Episodes: N/A'
        status = f"Status: {d.get('status', 'N/A')}".replace('_', ' ')
        score = f"Avg. Score: {d.get('score', 'N/A')}%" if d.get('score') is not None else 'Avg. Score: N/A'
        season = f"Season: {s_val} {y_val}".strip() if (s_val or y_val) else 'Season: N/A'
        genres = f"Genres: {genres_list}" if genres_list else "Genres: N/A"
        studio = f"Studio: {d.get('studio', 'N/A')}"
        desc = d.get('desc', 'No description :(')
        
        self.poster_link = d.get('poster_large_link')
        self.poster_small_link = d.get('poster_small_link')
        self.banner_link = d.get('banner_link')
        poster_color = d.get('poster_color')
        
        self.placeholder_poster = self.imgmClient.get_color_pixmap(poster_color, 460, 690)
        self.placeholder_banner = self.imgmClient.get_color_pixmap(poster_color, 1900, 400)
        
        self.poster = self.placeholder_poster.scaledToWidth(210, Qt.TransformationMode.SmoothTransformation)
        self.banner = self.placeholder_banner.scaledToWidth(800, Qt.TransformationMode.SmoothTransformation)
        
        self.ui.poster_label.setPixmap(self.poster)
        self.ui.poster_label.setFixedSize(self.poster.size())
        self.ui.banner_label.setPixmap(self.banner)

        self.ui.title_label.setText(title)
        self.ui.synonyms_label.setText(f"\u200E{synonyms}")
        self.ui.type_label.setText(format)
        self.ui.episodes_label.setText(eps)
        self.ui.status_label.setText(status)
        self.ui.score_label.setText(score)
        self.ui.season_label.setText(season)
        self.ui.genres_label.setText(genres)
        self.ui.studio_label.setText(studio)
        self.ui.desc_label.setText(desc)

        links = [self.poster_link, self.poster_small_link, self.banner_link]
        img_manager = ImageManager()
        worker = DownloadPostersWorker(links, img_manager.posters_path)
        worker.signals.finished.connect(self.on_posters_ready)

        self.parent.thread_pool.start(worker)

    def on_posters_ready(self, posters_data: dict):
        poster_path = posters_data.get(self.poster_link) or posters_data.get(self.poster_small_link) if self.poster_link else None
        banner_path = posters_data.get(self.banner_link) if self.banner_link else None
        
        if poster_path and os.path.exists(poster_path):
            real_poster = QPixmap(poster_path)
        else:
            real_poster = self.placeholder_poster
            
        if banner_path and os.path.exists(banner_path):
            real_banner = QPixmap(banner_path)
        else:
            real_banner = self.placeholder_banner

        if not real_banner.isNull():
            self.banner = real_banner.scaledToWidth(800, Qt.TransformationMode.SmoothTransformation)
            self.ui.banner_label.setPixmap(self.banner)

        if not real_poster.isNull():
            self.poster = real_poster.scaledToWidth(210, Qt.TransformationMode.SmoothTransformation)
            self.ui.poster_label.setPixmap(self.poster)
            self.ui.poster_label.setFixedSize(self.poster.size())

    def open_link(self):
        if not self.anilist_id: return
        d = self.ldbClient.get_title(self.anilist_id)
        if not d: return
        title_id = self.anilist_id

        if 'anilist' in self.ldbClient.db_path:
            link = f'https://anilist.co/anime/{title_id}'
        elif 'shikimori' in self.ldbClient.db_path:
            link = f'https://shikimori.io/animes/{title_id}'
        else:
            return

        QDesktopServices.openUrl(QUrl(link))