import PySide6
from PySide6.QtWidgets import QTreeWidgetItem
from core.logic import FileScanner
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl

import sys, os

from PySide6.QtWidgets import *
from ui.ui_add_series import *
from ui.ui_settings import *
from core.api.tvdb_api import TVDBClient
from core.db import *
from core.utils import *


class AddSeriesWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_AddSeriesWindow()
        self.ui.setupUi(self)
        
        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)

    def tvdb_search(self):
        # Get key from db
        db = SettingsDB()
        saved_key = db.get("tvdb_key")
        query = self.ui.search_lineEdit.text()
        if query:
            # Create client and search
            client = TVDBClient(saved_key)
            if client.authenticate():
                results = client.search(query)
                if results:
                    self.populate_search_tree(results)

    def populate_search_tree(self, results):
        if results.get("data"):
                for result in results["data"]:
                    name = result.get("translations", {}).get("eng", result.get("name", ""))
                    tvdb_id = result.get("id", "").strip("series-")
                    url = result.get("image_url")
                    
                    imgm = ImageManager()
                    pixmap = imgm.load_poster(imgm, url)
                    
                    status = result.get("status", "Unknown")
                    year = result.get("year", "N/A")
                    info = f"{year}\n{status}\nTVDB id: {tvdb_id}"