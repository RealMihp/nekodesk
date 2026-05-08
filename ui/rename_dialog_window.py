import PySide6
from PySide6.QtWidgets import *
from core.logic import FileScanner
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl

import sys, os

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

        self.title_data = title_data
        self.folder_path = folder_path

        self.insert_data()
        

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
        fansub_groups = local_data.get('groups')
        first_group = fansub_groups[0] if fansub_groups else ""
        max_ep = local_data.get('max_ep')
        title_romaji = data.get('title_romaji')
        title_native = data.get('title_native')
        title_english = data.get('title_english')

        title = title_romaji or title_native or title_english

        self.ui.translation_studio_lineEdit.setText(first_group)

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


    