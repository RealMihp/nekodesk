import time

import PySide6
from PySide6.QtWidgets import QTreeWidgetItem
from core.logic import FileScanner
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl, QThread, Signal
from rapidfuzz import fuzz
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
        self.ldbClient = LibraryDB()
        self.sdb = SettingsDB()
        self.search_data_cache = []
        self.scan_data_cache = []
        self.ALclient = AniListClient()
        self.session = self.ALclient.session
        self.ImageManager = ImageManager()
        self.prefManager = PreferencesManager()
        self.title_lang_priority = self.sdb.get("title_lang_priority", "Romaji,English,Native").split(",")
        

        self.ui.scan_results_treeWidget.sortByColumn(0, Qt.AscendingOrder)
        self.ui.scan_results_treeWidget.header().setSectionsClickable(True)
        self.ui.search_treeWidget.sortByColumn(1, Qt.AscendingOrder)
        self.ui.search_treeWidget.header().setSectionsClickable(True)
        self.ui.scan_results_treeWidget.header().setSectionResizeMode(0, QHeaderView.Stretch)
        self.ui.search_treeWidget.header().setSectionResizeMode(0, QHeaderView.Stretch)

        #self.ui.AniList_radioButton.setChecked(True)
        self.ui.search_pushButton.pressed.connect(self.populate_search_tree)
        self.ui.search_pushButton.setEnabled(True)

        self.ui.scan_folder_browse_pushButton.pressed.connect(self.select_folder)
        self.ui.scan_start_pushButton.pressed.connect(self.start_scan_library)

        self.ui.search_treeWidget.itemSelectionChanged.connect(lambda: self.ui.search_add_pushButton.setEnabled(True))
        self.ui.scan_results_treeWidget.itemSelectionChanged.connect(lambda: self.ui.scan_add_pushButton.setEnabled(True))

        self.ui.search_add_pushButton.pressed.connect(lambda: self.handle_add_series('self.ui.search_treeWidget'))
        self.ui.scan_add_pushButton.pressed.connect(lambda: self.handle_add_series('self.ui.scan_results_treeWidget'))
        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)

    

    def populate_search_tree(self):
        query = self.ui.search_lineEdit.text()
        if not query:
            return
        imgm = self.ImageManager

        self.ui.search_treeWidget.clear()
        self.search_data_cache = []
        self.ui.search_treeWidget.setIconSize(QSize(64, 96))

        #if self.ui.AniList_radioButton.isChecked():
        self.ui.statusbar_label.setText("Searching...")
        client = self.ALclient
        results = client.search_title(query)
        
        if not results:
            self.ui.statusbar_label.setText(r"Nothing found (っ- ‸ - ς)")
            return
        
        self.search_data_cache = results

        links = [r.get('coverImage', {}).get('medium') for r in results if r.get('coverImage')]
        
        posters_map = imgm.get_posters(links, session=self.session, is_temp=True)

        for result in results:
            title = None
            title_langs = {
                "romaji": result.get('title', {}).get('romaji'),
                "english": result.get('title', {}).get('english'),
                "native": result.get('title', {}).get('native')
            }

            for lang in self.title_lang_priority:
                lang_key = lang.lower()
                title_value = title_langs.get(lang_key)

                if title_value:
                    title = title_value
                    break

            if not title:
                title = "Unknown Title"
            
            year = str(result.get('seasonYear') or "N/A")
            status = result.get('status') or "Unknown"
            status = status.capitalize()
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
        
        header = self.ui.search_treeWidget.header()
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

        self.ui.statusbar_label.setText(f"Found titles: {len(results)}")
            
    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(
            self, 
            "Choose folder",
            "",
            QFileDialog.ShowDirsOnly
        )
        
        if folder_path:
            print(f"Path selected: {folder_path}")
            self.ui.scan_folder_lineEdit.setText(folder_path)
            self.ui.scan_start_pushButton.setEnabled(True)

    def populate_scan_tree(self, titles):
        if not titles:
            self.ui.statusbar_label.setText(r"Nothing new to add ¯\_(ツ)_/¯")
            return
        self.scan_data_cache = titles
        imgm = self.ImageManager

        links = [r.get('coverImage', {}).get('medium') for r in titles if r.get('coverImage')]
        posters_map = imgm.get_posters(links, session=self.session, is_temp=True)
        added_ids = set()
        
        self.ui.scan_results_treeWidget.setIconSize(QSize(64, 96))

        for result in titles:
                title = None
                title_langs = {
                    "romaji": result.get('title', {}).get('romaji'),
                    "english": result.get('title', {}).get('english'),
                    "native": result.get('title', {}).get('native')
                }

                for lang in self.title_lang_priority:
                    lang_key = lang.lower()
                    title_value = title_langs.get(lang_key)

                    if title_value:
                        title = title_value
                        break
                    
                if not title:
                    title = "Unknown Title"

                year = str(result.get('seasonYear') or "N/A")
                status = result.get('status') or "Unknown"
                status = status.capitalize()
                anime_id = str(result.get('id', ''))

                if anime_id in added_ids:
                    continue
                added_ids.add(anime_id)
                
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
                self.ui.scan_results_treeWidget.addTopLevelItem(item)

        header = self.ui.scan_results_treeWidget.header()
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

        self.ui.statusbar_label.setText(f"Found titles: {len(added_ids)}")

    def handle_add_series(self, widget):
        if widget == 'self.ui.scan_results_treeWidget':
            widget = self.ui.scan_results_treeWidget
            cache = self.scan_data_cache
        elif widget == 'self.ui.search_treeWidget':
            widget = self.ui.search_treeWidget
            cache = self.search_data_cache
        else:
            return
        
        selected_items = widget.selectedItems()
        if not selected_items:
                return

        for item in selected_items:
            title_id = item.data(0, ID_ROLE)

            self.ldbClient.add_title(cache, title_id)

    def start_scan_library(self):
        folder = self.ui.scan_folder_lineEdit.text()
        if not folder:
            return

        self.ui.scan_start_pushButton.setEnabled(False)
        self.ui.statusbar_label.setText("Scanning folder...")

        self.scan_worker = LibraryScanWorker(folder)
        
        self.scan_worker.progress.connect(
            lambda title: self.ui.statusbar_label.setText(f"Searching: {title}...")
        )
        self.scan_worker.finished.connect(self.on_scan_finished)
        
        self.scan_worker.start()

    def on_scan_finished(self, found_titles: list):
        self.ui.statusbar_label.setText(f"Found titles: {len(found_titles)}")
        self.ui.scan_start_pushButton.setEnabled(True)
        self.ui.scan_results_treeWidget.clear()

        titles = []
        for sublist in found_titles:
            if isinstance(sublist, list) and sublist and isinstance(sublist[0], dict):
                first_match = sublist[0]
                titles.append(first_match)

        self.populate_scan_tree(titles)


class LibraryScanWorker(QThread):
    finished = Signal(list)
    progress = Signal(str)

    def __init__(self, folder_path):
        super().__init__()
        self.folder_path = folder_path
        self.ldbClient = LibraryDB()

    def run(self):
        titles = FileScanner.scan_folder(self.folder_path)

        library = self.ldbClient.get_all_titles()
        romaji_titles = {title.get('title_romaji', '').lower() for title in library if title.get('title_romaji')}
        existing_ids = {str(title.get('anilist_id')) for title in library if title.get('anilist_id')}
        
        found_titles = []
        if titles:
            unique_titles = FileScanner.clean_and_deduplicate_titles(titles)
            for title in unique_titles:
                self.progress.emit(title)
                title_lower = title.lower()
                if any(fuzz.ratio(title_lower, r_title) >= 85 for r_title in romaji_titles):
                    print(f"Skipping (already in Library): {title}")
                    continue 

                time.sleep(1)
                print(f"Searching: {title}")
                try:
                    result = self.client.search_title(title)
                    
                    if result:
                        title_data = result[0] if isinstance(result, list) else result
                        if title_data and str(title_data.get('id')) not in existing_ids:
                            found_titles.append(result)
                        else:
                            print(f"Not showing (already in Library): {title}")
                        
                except Exception as e:
                    print(f"Critical error for {title}: {e}")
                    
        self.finished.emit(found_titles)
        