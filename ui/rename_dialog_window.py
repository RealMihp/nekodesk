import PySide6
from PySide6.QtWidgets import *
from core.logic import FileScanner
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl

import sys, os, shutil

from ui.ui_rename_dialog import *
from core.db import *
from core.utils import *
from core.api.anilist_api import *
from core.logic import FileScanner


class RenameWindow(QDialog):
    def __init__(self, parent=None, title_data: dict = {}, folder_path: str = ""):
        super().__init__(parent)
        self.ui = Ui_RenameDialog()
        self.ui.setupUi(self)
        self.imgmClient = ImageManager()

        self.title_data = title_data
        self.folder_path = folder_path

        self.save_poster_file_name = 'poster'   # get from settings
        self.save_banner_file_name = 'banner'   # get from settings

        self.insert_data()
        
        self.ui.save_poster_checkBox.toggled.connect(lambda: self.handle_checkboxes('save_poster_checkBox'))
        self.ui.save_banner_checkBox.toggled.connect(lambda: self.handle_checkboxes('save_banner_checkBox'))
        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)

    def render_preview_tree(self):
        """Render the preview treeWidget"""
        ...

    def insert_data(self):
        """Insert data to lineEdits using self.title_data and names of video files in the folder"""
        ...
        data = self.title_data
        folder_path = self.folder_path

        local_data = FileScanner.get_title_local_data(folder_path)
        fansub_groups = local_data.get('groups', '')
        first_group = fansub_groups[0] if fansub_groups else ""
        max_ep = local_data.get('max_ep', '')
        resolution = local_data.get('resolution')
        source = local_data.get('source', '')
        title_romaji = data.get('title_romaji')
        title_native = data.get('title_native')
        title_english = data.get('title_english')

        title = title_romaji or title_native or title_english

        self.ui.fansub_lineEdit.setText(first_group)

        eps_in_folder_str = '(' + str(max_ep) + ' in folder)' if max_ep > 0 else ''
        self.ui.episodes_in_folder_label.setText(eps_in_folder_str)
        
        self.ui.title_lineEdit.setText(title)
        self.ui.season_num_lineEdit.setText('1')
        self.ui.season_lineEdit.setText(data.get('season', ''))
        self.ui.season_year_lineEdit.setText(str(data.get('season_year', '')))
        self.ui.type_lineEdit.setText(data.get('format', '').capitalize() if data.get('format', '') == 'MOVIE' else data.get('format', ''))
        self.ui.studio_lineEdit.setText(data.get('studio', ''))
        self.ui.duration_lineEdit.setText(str(data.get('duration', '')))
        self.ui.episodes_lineEdit.setText(str(data.get('episodes', '')))
        self.ui.start_from_lineEdit.setText('1')
        self.ui.score_lineEdit.setText(str(data.get('score', '')))
        self.ui.status_lineEdit.setText(data.get('status', ''))
        self.ui.resolution_lineEdit.setText(resolution)
        self.ui.source_lineEdit.setText(source)


        poster_link = data.get('poster_large_link')
        poster_color = data.get('poster_color')
        poster = self.imgmClient.get_poster(poster_link, return_pixmap=True) if poster_link else self.imgmClient.get_color_icon(poster_color)
        placeholder_poster = self.imgmClient.get_color_pixmap(poster_color, 460, 690)
        banner_link = data.get('banner_link')
        placeholder_banner = self.imgmClient.get_color_pixmap(poster_color, 1900, 400)
        banner = self.imgmClient.get_poster(banner_link, return_pixmap=True) if banner_link else placeholder_banner

        if not banner.isNull():
            banner = banner.scaledToWidth(998, Qt.TransformationMode.SmoothTransformation)
            self.ui.banner_label.setPixmap(banner)
            

        if not poster.isNull():
            poster = poster.scaledToWidth(191, Qt.TransformationMode.SmoothTransformation)
            self.ui.poster_label.setPixmap(poster)
            self.ui.poster_label.setFixedSize(poster.size())

        self.ui.banner_label.setPixmap(banner)
        self.ui.poster_label.setPixmap(poster)
        
    def handle_checkboxes(self, checkbox):
        if checkbox == 'save_poster_checkBox':
            self.ui.save_poster_lineEdit.setEnabled(self.ui.save_poster_checkBox.isChecked())
        elif checkbox == 'save_banner_checkBox':
            self.ui.save_banner_lineEdit.setEnabled(self.ui.save_banner_checkBox.isChecked())
    
    def save_pictures(self):
        poster_link = self.title_data.get('poster_large_link')
        banner_link = self.title_data.get('banner_link')
        
        imgmClient = ImageManager(posters_path=self.folder_path)

        if poster_link:
            poster_src = imgmClient.get_poster(poster_link, return_pixmap=False, is_temp=False)
            if poster_src:
                poster_dst = os.path.join(self.folder_path, os.path.basename(poster_src)).replace('\\', '/')

                if os.path.abspath(poster_src) != os.path.abspath(poster_dst):
                    shutil.copy2(poster_src, poster_dst)

        if banner_link:
            banner_src = imgmClient.get_poster(banner_link, return_pixmap=False, is_temp=False)
            if banner_src:
                banner_dst = os.path.join(self.folder_path, os.path.basename(banner_src)).replace('\\', '/')
                if os.path.abspath(banner_src) != os.path.abspath(banner_dst):
                    shutil.copy2(banner_src, banner_dst)


        