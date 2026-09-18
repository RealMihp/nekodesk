import os
import sys
import time

import PySide6
from PySide6.QtCore import QSize, Qt, QThread, QThreadPool, QUrl, Signal
from PySide6.QtGui import QDesktopServices, QIcon, QPixmap
from PySide6.QtWidgets import *
from rapidfuzz import fuzz

from core.api.anilist_api import *
from core.db import *
from core.logic import FileScanner
from core.utils import *
from ui.ui_add_series import *
from ui.ui_settings import *

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
        self.prefManager = PreferencesManager(parent.current_library_db)
        self.title_lang_priority = self.sdb.get("title_lang_priority", "Romaji,English,Native").split(",")

        self.ui.scan_results_treeWidget.sortByColumn(0, Qt.DescendingOrder)
        self.ui.scan_results_treeWidget.header().setSectionsClickable(True)
        self.ui.search_treeWidget.sortByColumn(1, Qt.DescendingOrder)
        self.ui.search_treeWidget.header().setSectionsClickable(True)
        self.ui.scan_results_treeWidget.header().setSectionResizeMode(0, QHeaderView.Stretch)
        self.ui.search_treeWidget.header().setSectionResizeMode(0, QHeaderView.Stretch)

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
        query = self.ui.search_lineEdit.text().strip()
        if not query:
            return

        imgm = self.ImageManager
        self.ui.search_treeWidget.clear()
        self.search_data_cache = []
        self.ui.search_treeWidget.setIconSize(QSize(64, 96))

        self.ui.statusbar_label.setText("Searching...")
        results = self.ALclient.search_title(query)
        
        if not results:
            self.ui.statusbar_label.setText(r"Nothing found (っ- ‸ - ς)")
            return
        
        self.search_data_cache = results

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
            status = (result.get('status') or "Unknown").replace('_',' ').capitalize()
            anime_id = str(result.get('id'))
            
            link = result.get('coverImage', {}).get('medium')
            color = result.get('coverImage', {}).get('color')
            
            item = QTreeWidgetItem([title, year, status])

            placeholder_pixmap = imgm.get_color_icon(color)
            item.setIcon(0, QIcon(placeholder_pixmap))
            
            item.setData(0, Qt.UserRole + 1, link)
            item.setData(0, ID_ROLE, anime_id)
            
            self.ui.search_treeWidget.addTopLevelItem(item)

        header = self.ui.search_treeWidget.header()
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

        self.ui.statusbar_label.setText(f"Found titles: {len(results)}. Loading covers...")

        links = [r.get('coverImage', {}).get('medium') for r in results if r.get('coverImage')]
        if links:
            worker = DownloadPostersWorker(links, imgm.posters_path)
            worker.signals.finished.connect(self.on_posters_ready)
            self.parent().thread_pool.start(worker)


    def on_posters_ready(self, posters_map: dict):
        root = self.ui.search_treeWidget.invisibleRootItem()
        
        for i in range(root.childCount()):
            item = root.child(i)
            link = item.data(0, Qt.UserRole + 1)
            
            if link in posters_map:
                data = posters_map[link]
                
                if isinstance(data, (tuple, list)):
                    data = data[0]

                if isinstance(data, str):
                    pixmap = QPixmap(data)
                else:
                    pixmap = data
                    
                if pixmap and isinstance(pixmap, QPixmap) and not pixmap.isNull():
                    item.setIcon(0, QIcon(pixmap))
                    
        self.ui.statusbar_label.setText(f"Found titles: {len(self.search_data_cache)}")


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


    def populate_scan_tree(self, titles: list[dict]):
        if not titles:
            self.ui.statusbar_label.setText(r"Nothing new to add ¯\_(ツ)_/¯")
            return

        self.scan_data_cache = titles
        imgm = self.ImageManager

        self.ui.scan_results_treeWidget.clear()
        self.ui.scan_results_treeWidget.setIconSize(QSize(64, 96))

        added_ids = set()

        for result in titles:
            anime_id = str(result.get('id', ''))
            if not anime_id or anime_id in added_ids:
                continue
            added_ids.add(anime_id)

            title = None
            title_langs = result.get('title', {})
            for lang in self.title_lang_priority:
                title_value = title_langs.get(lang.lower())
                if title_value:
                    title = title_value
                    break

            if not title:
                title = "Unknown Title"

            year = str(result.get('seasonYear') or "N/A")
            status = str(result.get('status') or "Unknown").capitalize()

            link = result.get('coverImage', {}).get('medium')
            color = result.get('coverImage', {}).get('color')

            item = QTreeWidgetItem([title, year, status])

            placeholder = imgm.get_color_icon(color)
            item.setIcon(0, QIcon(placeholder))
            item.setData(0, Qt.UserRole + 1, link)
            item.setData(0, ID_ROLE, anime_id)

            self.ui.scan_results_treeWidget.addTopLevelItem(item)

        header = self.ui.scan_results_treeWidget.header()
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

        self.ui.statusbar_label.setText(f"Found titles: {len(added_ids)}. Loading covers...")

        links = [r.get('coverImage', {}).get('medium') for r in titles if r.get('coverImage')]
        if links:
            worker = DownloadPostersWorker(links, imgm.posters_path)
            worker.signals.finished.connect(self.on_scan_posters_ready)
            QThreadPool.globalInstance().start(worker)


    def on_scan_posters_ready(self, posters_map: dict):
        root = self.ui.scan_results_treeWidget.invisibleRootItem()

        for i in range(root.childCount()):
            item = root.child(i)
            link = item.data(0, Qt.UserRole + 1)

            if link in posters_map:
                data = posters_map[link]
                if isinstance(data, (tuple, list)):
                    data = data[0]

                pixmap = QPixmap(data) if isinstance(data, str) else data

                if pixmap and isinstance(pixmap, QPixmap) and not pixmap.isNull():
                    item.setIcon(0, QIcon(pixmap))

        self.ui.statusbar_label.setText(f"Found titles: {len(self.scan_data_cache)}")


    def handle_add_series(self, widget):
        if widget == self.ui.scan_results_treeWidget or widget == 'self.ui.scan_results_treeWidget':
            tree = self.ui.scan_results_treeWidget
            cache = self.scan_data_cache
        elif widget == self.ui.search_treeWidget or widget == 'self.ui.search_treeWidget':
            tree = self.ui.search_treeWidget
            cache = self.search_data_cache
        else:
            return

        selected_items = tree.selectedItems()
        if not selected_items:
            return

        for item in selected_items:
            selected_id = str(item.data(0, ID_ROLE))

            target_title = None
            for title_data in cache:
                data = title_data[0] if isinstance(title_data, list) and title_data else title_data
                
                if isinstance(data, dict) and str(data.get('id', '')) == selected_id:
                    target_title = data
                    break

            if target_title:
                self.ldbClient.add_title(target_title, selected_id)


    def start_scan_library(self):
        folder = self.ui.scan_folder_lineEdit.text().strip()
        if not folder:
            return

        self.ui.scan_start_pushButton.setEnabled(False)
        self.ui.statusbar_label.setText("Scanning folder...")

        self.scan_worker = LibraryScanWorker(folder, client=self.ALclient, parent=self)
        self.scan_worker.progress.connect(
            lambda title: self.ui.statusbar_label.setText(f"Searching: {title}...")
        )
        self.scan_worker.finished.connect(self.on_scan_finished)
        self.scan_worker.finished.connect(self.scan_worker.deleteLater)
        self.scan_worker.start()


    def on_scan_finished(self, found_titles: list):
        self.ui.scan_start_pushButton.setEnabled(True)
        self.populate_scan_tree(found_titles)


class LibraryScanWorker(QThread):
    finished = Signal(list)
    progress = Signal(str)

    def __init__(self, folder_path, client, parent=None):
        super().__init__(parent)
        self.folder_path = folder_path
        self.client = client

    def run(self):
        ldb_client = LibraryDB()
        found_titles = []

        titles = FileScanner.scan_folder(self.folder_path)

        library = ldb_client.get_all_titles()
        romaji_titles = {title.get('title_romaji', '').lower() for title in library if title.get('title_romaji')}
        existing_ids = {str(title.get('anilist_id')) for title in library if title.get('anilist_id')}
        
        if titles:
            unique_titles = FileScanner.clean_and_deduplicate_titles(titles)
            for title in unique_titles:
                self.progress.emit(title)
                title_lower = title.lower()

                if any(fuzz.ratio(title_lower, r_title) >= 85 for r_title in romaji_titles):
                    print(f"Skipping (already in Library): {title}")
                    continue 

                time.sleep(1) # Задержка для апи
                print(f"Searching: {title}")
                try:
                    results = self.client.search_title(title)
                    
                    if results:
                        top_match = results[0] if isinstance(results, list) else results
                        
                        if top_match and str(top_match.get('id')) not in existing_ids:
                            found_titles.append(top_match)
                            existing_ids.add(str(top_match.get('id')))
                        else:
                            print(f"Not showing (already in Library): {title}")
                        
                except Exception as e:
                    print(f"Critical error for {title}: {e}")

        self.finished.emit(found_titles)