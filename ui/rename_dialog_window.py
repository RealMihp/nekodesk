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
        title_data = self.title_data
        folder_path = self.folder_path

        local_data = FileScanner.get_title_local_data(folder_path)
        fansub_groups = local_data.get('groups')
        max_ep = local_data.get('max_ep')

        self.ui.translation_studio_lineEdit.setText((',').join(fansub_groups))

        eps_in_folder_str = '(' + str(max_ep) + ' in folder)' if max_ep > 0 else ''
        self.ui.episodes_in_folder_label.setText(eps_in_folder_str)
        


    