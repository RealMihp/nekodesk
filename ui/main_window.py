import threading

import PySide6
from PySide6.QtWidgets import QTreeWidgetItem, QMenu
from core.logic import FileScanner
from PySide6.QtGui import QDesktopServices, QAction
from PySide6.QtCore import QTimer, QUrl, QThreadPool

import sys, os
import keyring

from PySide6.QtWidgets import *
from ui.about_window import AboutWindow
from ui.title_details_window import Title_detailsWindow
from ui.rename_dialog_window import RenameWindow
from ui.ui_main import *
from ui.add_series_window import *
from ui.settings_window import *
from ui.ui_settings import *
from ui.widgets import FilesTree
from core.utils import PreferencesManager
from ui.loading_dialog import LoadingDialog

PATH_ROLE = 32




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.history = []
        self.forward_stack = []
        self.ldbclient = LibraryDB()
        self.al_client = AniListClient()
        self.prefManager = PreferencesManager(self.ldbclient)
        
        self.thread_pool = QThreadPool()
        self.thread_pool.setMaxThreadCount(3)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.anilist_widgets = {
            'CURRENT': self.ui.anilist_current_library_treeWidget,
            'REPEATING': self.ui.anilist_repeating_library_treeWidget,
            'PLANNING': self.ui.anilist_planning_library_treeWidget,
            'COMPLETED': self.ui.anilist_completed_library_treeWidget,
            'DROPPED': self.ui.anilist_dropped_library_treeWidget,
            'PAUSED': self.ui.anilist_paused_library_treeWidget
        }

        self.current_library_widget = self.ui.library_treeWidget # Default
        self.current_library_db = LibraryDB() # Default

        self.setup_treewidgets()
        self.setup_connections()

    def setup_connections(self):
        """Sets up all connections"""
        self.ui.actionSelect_folder.triggered.connect(self.select_folder)
        self.ui.actionClose_folder.triggered.connect(self.close_folder)
        self.ui.files_treeWidget.itemDoubleClicked.connect(self.open_item)
        self.ui.back_pushButton.pressed.connect(self.back)
        self.ui.refresh_pushButton.pressed.connect(self.refresh)
        self.ui.forward_pushButton.pressed.connect(self.forward)
        self.ui.addSeries_pushButton.pressed.connect(self.show_addseries)
        self.ui.actionSettings.triggered.connect(self.show_settings)
        self.ui.actionAbout.triggered.connect(self.show_about)
        self.ui.anilist_library_refresh_pushButton.pressed.connect(self.refresh_anilist)
        self.ui.right_tabWidget.currentChanged.connect(self.on_library_tab_changed)
        self.ui.anilist_library_tabWidget.currentChanged.connect(self.on_anilist_library_tab_changed)

    def setup_treewidgets(self):
        widgets = [
            self.ui.library_treeWidget,
            self.ui.anilist_current_library_treeWidget,
            self.ui.anilist_repeating_library_treeWidget,
            self.ui.anilist_planning_library_treeWidget,
            self.ui.anilist_completed_library_treeWidget,
            self.ui.anilist_dropped_library_treeWidget,
            self.ui.anilist_paused_library_treeWidget
        ]

        for widget in widgets:
            widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            widget.customContextMenuRequested.connect(self.show_library_context_menu)
            widget.header().setSectionResizeMode(0, QHeaderView.Stretch)
            widget.sortByColumn(0, Qt.AscendingOrder)

            widget.setDragDropOverwriteMode(False)
            widget.setDragEnabled(True)
            widget.setDragDropMode(QAbstractItemView.DragOnly)
            widget.setDropIndicatorShown(True)

        self.refresh_library(self.ui.library_treeWidget, self.ldbclient)
        self.refresh_anilist(update=False)

    def on_library_tab_changed(self, index):
        if index == 0:
            self.current_library_widget = self.ui.library_treeWidget
            self.current_library_db = LibraryDB()
        elif index == 1:
            current_anilist_index = self.ui.anilist_library_tabWidget.currentIndex()
            self.on_anilist_library_tab_changed(current_anilist_index)
        

    def on_anilist_library_tab_changed(self, index):
        tab_mapping = {
            0: self.ui.anilist_current_library_treeWidget,
            1: self.ui.anilist_repeating_library_treeWidget,
            2: self.ui.anilist_completed_library_treeWidget,
            3: self.ui.anilist_paused_library_treeWidget,
            4: self.ui.anilist_planning_library_treeWidget,
            5: self.ui.anilist_dropped_library_treeWidget
        }

        self.current_library_widget = tab_mapping.get(index, self.ui.anilist_current_library_treeWidget)
        for list, widget in self.anilist_widgets.items():
            if widget == self.current_library_widget:
                self.current_library_db = LibraryDB(f'data/anilist/{list.lower()}.db')

                

    def show_details(self, widget: QTreeWidget, anilist_id: str):
        self.details_window = Title_detailsWindow(self, widget, anilist_id)
        
        self.details_window.show()

    def show_about(self, anilist_id: str):
        self.about_window = AboutWindow(self)
        
        self.about_window.show()
        
    def show_library_context_menu(self, pos):
        widget = self.current_library_widget
        item = widget.itemAt(pos)
        if not item: return

        menu = QMenu(self)
        open_action = QAction('Details', self)
        remove_action = QAction('Remove from library', self)
        add_to_local_library_action = QAction('Add to local library', self)

        anilist_id = item.data(0, Qt.ItemDataRole.UserRole)
        open_action.triggered.connect(lambda: self.show_details(widget, anilist_id))
        remove_action.triggered.connect(lambda: self.remove_title(anilist_id))
        add_to_local_library_action.triggered.connect(lambda: self.add_to_local_library(anilist_id, widget))

        menu.addAction(open_action)
        if widget == self.ui.library_treeWidget:
            menu.addSeparator()
            menu.addAction(remove_action)
        if widget in self.anilist_widgets.values():
            menu.addSeparator()
            menu.addAction(add_to_local_library_action)

        menu.exec(widget.mapToGlobal(pos))

    def add_to_local_library(self, title_id: int | str, widget: QTreeWidget):
        if not title_id:
            return
        if not widget:
            widget = self.current_library_widget

        source_db = self.current_library_db
        target_db = self.ldbclient

        d = source_db.get_title(title_id)
        copy = target_db.copy_title(d)

        if copy:
            self.refresh_library(self.ui.library_treeWidget, target_db)




    def remove_title(self, anilist_id: str):
        self.ldbclient.remove_title_by_id(anilist_id)
        self.refresh_library()

    def show_addseries(self):
        dialog = AddSeriesWindow(self)
        
        if dialog.exec(): 
            print(f"Added series")
           
        else:
            print("Canceled adding series")
        self.refresh_library()

    def show_settings(self):
        dialog = SettingsWindow(self)

        if dialog.exec():
            self.refresh_library()
            print("Changed settings")
        else:
            print("Canceled changing settings")

    def populate_tree(self, folder_path = None):
        if not folder_path:
            folder_path = self.ui.path_lineEdit.text()
        items = FileScanner.get_items(folder_path)
        
        self.ui.files_treeWidget.clear()
        self.ui.path_lineEdit.setText(folder_path)
        current_dir = self.ui.path_lineEdit.text()
        for data in items:
            item = QTreeWidgetItem(self.ui.files_treeWidget)
            item.setText(0, data['name'])
            item.setData(0, PATH_ROLE, data['path'])
            
            # icons
            icon_type = QStyle.SP_DirIcon if data['is_dir'] else QStyle.SP_FileIcon
            item.setIcon(0, self.style().standardIcon(icon_type))

        self.ui.back_pushButton.setEnabled(len(self.history) > 0)
        self.ui.forward_pushButton.setEnabled(len(self.forward_stack) > 0)
        
        self.ui.refresh_pushButton.setEnabled(True if current_dir else False)
        


    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(
            self, 
            "Choose folder",
            "",
            QFileDialog.ShowDirsOnly
        )

        if folder_path:
            print(f"Path selected: {folder_path}")
            self.populate_tree(folder_path)
    
    def close_folder(self):
        self.ui.files_treeWidget.clear()
        self.ui.path_lineEdit.setText("")
        self.history.clear()
        self.forward_stack.clear()
        self.ui.back_pushButton.setEnabled(False)
        self.ui.forward_pushButton.setEnabled(False)
        self.ui.refresh_pushButton.setEnabled(False)

    def open_item(self, item, column):
        if item:
            path = item.data(0, PATH_ROLE)
            if path:
                if os.path.isdir(path):
                    current_dir = self.ui.path_lineEdit.text()
                    if current_dir:
                        self.history.append(current_dir)
                        self.forward_stack.clear()
                    self.populate_tree(path)
                else:
                    self.open_file(path)

    def open_file(self, path):
        file_url = QUrl.fromLocalFile(path)
        QDesktopServices.openUrl(file_url)

    def back(self):
        if self.history:
            current_dir = self.ui.path_lineEdit.text()
            last_folder = self.history.pop()
            self.forward_stack.append(current_dir)
            self.populate_tree(last_folder)
            
    
    def refresh(self):
        current_dir = self.ui.path_lineEdit.text()
        if current_dir:
            self.populate_tree(current_dir)
            self.ui.files_treeWidget.scrollToTop()

    def forward(self):
        if self.forward_stack:
            current_dir = self.ui.path_lineEdit.text()
            self.history.append(current_dir)
            
            next_folder = self.forward_stack.pop()
            self.populate_tree(next_folder)

    def refresh_library(self, widget: QTreeWidget = None, db: LibraryDB= None):
        if not widget:
            widget = self.current_library_widget
        if not db:
            db = self.current_library_db

        widget.clear()
        widget.setIconSize(QSize(64, 96))

        titles = db.get_all_titles()
        imgmClient = ImageManager()
        
        links_to_download = []

        for title in titles:
            prefManager = PreferencesManager(db)
            name = prefManager.get_title_title(title.get("anilist_id")) or 'Unknown'
            status = title.get('status', 'N/A')
            raw_year = title.get('season_year')
            year = str(raw_year) if raw_year else 'N/A'
            raw_episodes = title.get('episodes')
            episodes = str(raw_episodes).zfill(2) if raw_episodes else 'N/A'
            format = str(title.get('format', 'N/A'))
            if format == 'MOVIE' or format == 'SPECIAL':
                format = format.capitalize()
            elif format == 'TV_SHORT':
                format = 'TV Short'
            
            item = QTreeWidgetItem([name, year, format, episodes])

            path = title.get('poster_small_path')
            
            # If poster already in files
            if path and os.path.exists(path):
                item.setIcon(0, QIcon(path))
            # Else add to links_to_download
            else:
                poster_url = title.get('poster_small_link')
                
                if poster_url:
                    item.setData(0, Qt.ItemDataRole.UserRole + 1, poster_url)
                    links_to_download.append(poster_url)

                color = title.get('poster_color')
                item.setIcon(0, imgmClient.get_color_icon(color))

            item.setData(0, Qt.ItemDataRole.UserRole, title.get('anilist_id'))

            header = widget.header()
            header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

            widget.addTopLevelItem(item)
            
        imgmClient.clear_temp_folder()

        if links_to_download:
            self.start_posters_download(links_to_download)

    def start_posters_download(self, links: list):
        img_manager = ImageManager()
        worker = DownloadPostersWorker(links, img_manager.posters_path)
        worker.signals.finished.connect(self.on_posters_ready)
        
        self.thread_pool.start(worker)

    def on_posters_ready(self, posters_data: dict):
        widgets = [
            self.ui.library_treeWidget,
            self.ui.anilist_current_library_treeWidget,
            self.ui.anilist_repeating_library_treeWidget,
            self.ui.anilist_planning_library_treeWidget,
            self.ui.anilist_completed_library_treeWidget,
            self.ui.anilist_dropped_library_treeWidget,
            self.ui.anilist_paused_library_treeWidget
        ]

        for widget in widgets:
            iterator = QTreeWidgetItemIterator(widget)
            while iterator.value():
                item = iterator.value()
                
                item_url = item.data(0, Qt.ItemDataRole.UserRole + 1)
                
                if item_url and item_url in posters_data:
                    file_path = posters_data[item_url]
                    if file_path and os.path.exists(file_path):
                        item.setIcon(0, QIcon(file_path))
                        
                iterator += 1

    def open_rename_dialog(self, title_id: str, folder_path: str):
        title_data = self.current_library_db.get_title(title_id) # dict
        print(f"{title_data.get('title_romaji')} -> {folder_path}")

        dialog = RenameWindow(self, title_data=title_data, folder_path=folder_path, db=self.current_library_db)
        if dialog.exec(): 
            time.sleep(0.2)
            self.populate_tree()
            print("Title renamed, tree refreshed")
        else:
            print("Rename dialog Cancel")

    def update_anilist_db(self):
        self.al_db = SettingsDB('data/anilist/anilist.db')
        user_id = self.al_db.get('id')
        if user_id:
            data = self.al_client.get_user_media_list(user_id)
        else:
            return
        lists = data.get('data', {}).get('MediaListCollection', {}).get('lists', [])
        if not lists:
            return

        anime_lists = {
            'CURRENT': [],
            'REPEATING': [],
            'PLANNING': [],
            'COMPLETED': [],
            'DROPPED': [],
            'PAUSED': []
        }

        for anime_list in lists:
            status = anime_list.get('status', '').upper()
            if status in anime_lists:
                anime_lists[status] = anime_list.get('entries', [])

        for list, entries in anime_lists.items():
            db = LibraryDB(f'data/anilist/{list.lower()}.db')
            for title in entries:
                title_id = title.get('media', {}).get('id')
                if title_id:
                    db.add_title(title, title_id)
        
    def refresh_anilist(self, update: bool = True):
        if update:
            self.update_anilist_db()

        for list, widget in self.anilist_widgets.items():
            db = LibraryDB(f'data/anilist/{list.lower()}.db')
            self.refresh_library(widget, db)
            widget.sortByColumn(0, Qt.AscendingOrder)
            widget.header().setSectionResizeMode(0, QHeaderView.Stretch)
            
            
            

