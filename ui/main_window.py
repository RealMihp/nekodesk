import threading

import PySide6
from PySide6.QtWidgets import QTreeWidgetItem, QMenu
from core.logic import FileScanner, qbit
from PySide6.QtGui import QDesktopServices, QAction
from PySide6.QtCore import QTimer, QUrl, QThreadPool

import sys, os
import keyring

from PySide6.QtWidgets import *
from ui.about_window import AboutWindow
from ui.title_details_window import Title_detailsWindow
from ui.rename_dialog_window import RenameWindow
from core.renamer import RenamerService
from core.worker import RenameWorker
from core.models import RenameConfig
from ui.ui_main import *
from ui.add_series_window import *
from ui.settings_window import *
from ui.ui_settings import *
from ui.widgets import FilesTree
from core.utils import PreferencesManager
from ui.loading_dialog import LoadingDialog
from core.api.shikimori_api import *

PATH_ROLE = 32




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.history = []
        self.forward_stack = []
        self.ldbclient = LibraryDB()
        self.al_client = AniListClient()
        self.sh_client = ShikimoriClient()
        self.prefManager = PreferencesManager(self.ldbclient)
        self.loading_window = None
        
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
        self.shikimori_widgets = {
            'CURRENT': self.ui.shikimori_watching_library_treeWidget,
            'REPEATING': self.ui.shikimori_rewatching_library_treeWidget,
            'PLANNING': self.ui.shikimori_planned_library_treeWidget,
            'COMPLETED': self.ui.shikimori_completed_library_treeWidget,
            'DROPPED': self.ui.shikimori_dropped_library_treeWidget,
            'PAUSED': self.ui.shikimori_on_hold_library_treeWidget
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
        self.ui.shikimori_library_tabWidget.currentChanged.connect(self.on_shikimori_library_tab_changed)
        self.ui.shikimori_library_refresh_pushButton.pressed.connect(self.refresh_shikimori)

    def setup_treewidgets(self):
        widgets = [
            self.ui.library_treeWidget,
            self.ui.anilist_current_library_treeWidget,
            self.ui.anilist_repeating_library_treeWidget,
            self.ui.anilist_planning_library_treeWidget,
            self.ui.anilist_completed_library_treeWidget,
            self.ui.anilist_dropped_library_treeWidget,
            self.ui.anilist_paused_library_treeWidget,
            self.ui.shikimori_watching_library_treeWidget,
            self.ui.shikimori_rewatching_library_treeWidget,
            self.ui.shikimori_planned_library_treeWidget,
            self.ui.shikimori_completed_library_treeWidget,
            self.ui.shikimori_dropped_library_treeWidget,
            self.ui.shikimori_on_hold_library_treeWidget
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

        self.ui.files_treeWidget.customContextMenuRequested.connect(self.show_files_context_menu)
        self.refresh_library(self.ui.library_treeWidget, self.ldbclient)
        self.refresh_anilist(update=False)
        self.refresh_shikimori(update=False)

    def on_library_tab_changed(self, index):
        if index == 0:
            self.current_library_widget = self.ui.library_treeWidget
            self.current_library_db = LibraryDB()
        elif index == 1:
            current_anilist_index = self.ui.anilist_library_tabWidget.currentIndex()
            self.on_anilist_library_tab_changed(current_anilist_index)
        elif index == 2:
            current_shikimori_index = self.ui.shikimori_library_tabWidget.currentIndex()
            self.on_shikimori_library_tab_changed(current_shikimori_index)
        

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

    def on_shikimori_library_tab_changed(self, index):
        tab_mapping = {
            0: self.ui.shikimori_watching_library_treeWidget,
            1: self.ui.shikimori_rewatching_library_treeWidget,
            2: self.ui.shikimori_completed_library_treeWidget,
            3: self.ui.shikimori_on_hold_library_treeWidget,
            4: self.ui.shikimori_planned_library_treeWidget,
            5: self.ui.shikimori_dropped_library_treeWidget
        }

        self.current_library_widget = tab_mapping.get(index, self.ui.shikimori_watching_library_treeWidget)
        for list, widget in self.shikimori_widgets.items():
            if widget == self.current_library_widget:
                self.current_library_db = LibraryDB(f'data/shikimori/{list.lower()}.db')

                

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
        if widget in self.shikimori_widgets.values():
            menu.addSeparator()
            menu.addAction(add_to_local_library_action)
        

        menu.exec(widget.mapToGlobal(pos))

    def show_files_context_menu(self, pos):
        widget = self.ui.files_treeWidget
        item = widget.itemAt(pos)
        if not item: return

        path = item.data(0, PATH_ROLE)
        if not path: return

        # Папка, для которой нужно проверить наличие резервного снимка:
        # если кликнули по файлу — берём его родительскую папку, если по
        # папке — саму папку.
        folder_path = path if os.path.isdir(path) else os.path.dirname(path)

        menu = QMenu(self)

        # Пункт "Restore" показываем только если для этой папки есть
        # скрытый файл-снимок и в нём реально есть что откатывать (файлы
        # и/или сама папка, переименованные программой, всё ещё под новыми
        # именами).
        if RenamerService.has_restorable_changes(folder_path):
            restore_action = QAction('Restore', self)
            restore_action.triggered.connect(lambda: self.restore_original_names(folder_path))
            menu.addAction(restore_action)

        if menu.isEmpty():
            return

        menu.exec(widget.mapToGlobal(pos))

    def restore_original_names(self, folder_path: str):
        """Откатывает переименование файлов и (если применимо) самой папки
        в folder_path, используя скрытый файл-снимок
        (nekodesk.json), созданный RenamerService при
        переименовании. Файлы, добавленные в папку позже (постеры/баннеры
        и т.п.), не затрагиваются — их не было в исходном списке.

        Здесь нет доступа к qBittorrent-клиенту (в отличие от
        RenameWindow), поэтому откат папки делается обычным os.rename —
        для торрентов, переименованных через qBittorrent, лучше открыть
        "Rename" ещё раз и откатить оттуда."""
        restore_queue = RenamerService.build_restore_queue(folder_path)
        folder_restore = RenamerService.get_folder_restore(folder_path)

        if not restore_queue and not folder_restore:
            QMessageBox.information(
                self,
                "Nothing to restore",
                "No backup snapshot found for this folder, or files are already at their original names."
            )
            return

        total_changes = len(restore_queue) + (1 if folder_restore else 0)
        reply = QMessageBox.question(
            self,
            "Restore original names?",
            f"This will restore {total_changes} item(s) to their original names in:\n\n{folder_path}\n\nContinue?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return

        config = RenameConfig(folder_path=folder_path, template="")

        # Пытаемся найти торрент в qBittorrent и откатить через его API —
        # если этого не делать, файлы переименуются только на диске, а
        # qBittorrent продолжит считать их под старыми (переименованными)
        # именами. Из-за этого расхождения следующая операция с этим же
        # релизом (rename/restore) не находит нужные файлы и падает.
        qbit_client = None
        torrent_obj = None
        sdb = SettingsDB()
        if sdb.get('qbit', 'False') == 'True':
            try:
                qbit_client = qbit(
                    host=sdb.get('qbit_ip'),
                    port=int(sdb.get('qbit_port')),
                    username=sdb.get('qbit_username'),
                    password=keyring.get_password(
                        "nekodesk", sdb.get("qbit_username", "admin")
                    )
                )
                if qbit_client.login():
                    torrent_obj = qbit_client.find_torrent_by_content_path(folder_path)
                if not torrent_obj:
                    qbit_client = None
            except Exception as e:
                print(f"Failed to init qBittorrent client for restore: {e}")
                qbit_client = None
                torrent_obj = None

        config.use_qbit = bool(qbit_client and torrent_obj)

        self.restore_worker = RenameWorker(
            rename_queue=restore_queue,
            config=config,
            qbit_client=qbit_client,
            torrent_obj=torrent_obj,
            folder_rename=folder_restore,
            new_torrent_name=None,
            parent=self
        )
        self.restore_worker.error_occurred.connect(lambda msg: QMessageBox.critical(self, "Restore error", msg))
        self.restore_worker.completed.connect(lambda msg: self._on_restore_completed(folder_path))
        self.restore_worker.start()

    def _on_restore_completed(self, folder_path: str):
        QMessageBox.information(self, "Restore complete", "Original file names have been restored.")
        # Обновляем дерево файлов, если сейчас открыта та же (или родительская) папка
        current_dir = self.ui.path_lineEdit.text()
        if current_dir:
            self.populate_tree(current_dir)

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
        sdb = SettingsDB()
        initial_dir = sdb.get('last_folder_path', None)

        if not initial_dir or not os.path.exists(initial_dir):
            initial_dir = ''

        folder_path = QFileDialog.getExistingDirectory(
            self, 
            "Choose folder",
            initial_dir,
            QFileDialog.ShowDirsOnly
        )

        if folder_path:
            sdb.set('last_folder_path', folder_path)
            print(f'Path selected: {folder_path}')
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
            self.ui.anilist_paused_library_treeWidget,
            self.ui.shikimori_watching_library_treeWidget,
            self.ui.shikimori_rewatching_library_treeWidget,
            self.ui.shikimori_planned_library_treeWidget,
            self.ui.shikimori_completed_library_treeWidget,
            self.ui.shikimori_dropped_library_treeWidget,
            self.ui.shikimori_on_hold_library_treeWidget
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
            # Небольшая задержка на случай, если ФС ещё не "устаканилась"
            # после переименования файлов — но без блокировки GUI-потока.
            QTimer.singleShot(200, self.populate_tree)
            print("Title renamed, tree refreshed")
        else:
            print("Rename dialog Cancel")

    def update_anilist_db(self):
        self.al_db = SettingsDB('data/anilist/anilist.db')
        user_id = self.al_db.get('id')
        if not user_id:
            return

        data = self.al_client.get_user_media_list(user_id)
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

        for list_name, entries in anime_lists.items():
            db_path = f'data/anilist/{list_name.lower()}.db'
            db = LibraryDB(db_path)
            
            try:
                for title in entries:
                    title_id = title.get('media', {}).get('id')
                    if title_id:
                        db.add_title(title, title_id)
            finally:
                if hasattr(db, 'close'):
                    db.close()
                elif hasattr(db, 'conn'):
                    db.conn.close()

    def refresh_anilist(self, update: bool = True):
                self.refresh_service('AniList', update)
        
    def refresh_service(self, service: str = '', update: bool = True):
        if service:
            if update:
                self.loading_window = LoadingDialog(f'Refreshing {service} library...', 'Refreshing...', self)
                self.loading_window.show()

                self.worker = UpdateWorker(service, self)
                self.worker.finished_service.connect(self._on_service_db_updated)
                self.worker.finished_service.connect(self.worker.deleteLater)
                
                self.worker.start()
            else:
                self._populate_service_widgets(service)

    def _populate_service_widgets(self, service: str = ''):
        if service.lower() == 'anilist':
            for list_name, widget in self.anilist_widgets.items():
                db = LibraryDB(f'data/anilist/{list_name.lower()}.db')
                self.refresh_library(widget, db)
                widget.sortByColumn(0, Qt.AscendingOrder)
                widget.header().setSectionResizeMode(0, QHeaderView.Stretch)
        elif service.lower() == 'shikimori':
            for list, widget in self.shikimori_widgets.items():
                db = LibraryDB(f'data/shikimori/{list.lower()}.db')
                self.refresh_library(widget, db)
                widget.sortByColumn(0, Qt.AscendingOrder)
                widget.header().setSectionResizeMode(0, QHeaderView.Stretch)

    def _on_service_db_updated(self, service: str = ''):
        self._populate_service_widgets(service)
        
        if self.loading_window:
            self.loading_window.close()
            self.loading_window = None

    def update_shikimori_db(self):
        self.sh_db = SettingsDB('data/shikimori/shikimori.db')
        user_id = self.sh_db.get('id')
        if not user_id:
            return

        raw_data = self.sh_client.get_user_media_list(user_id)
        data = self._anilistize_shikimori(raw_data)

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

        for status_key, entries in anime_lists.items():
            db = LibraryDB(f'data/shikimori/{status_key.lower()}.db')
            for title in entries:
                title_id = title.get('media', {}).get('id')
                if title_id:
                    db.add_title(title, title_id)
                    

    def _anilistize_shikimori(self, user_media: dict) -> dict:
        STATUS_CONFIG = {
            'watching': {'name': 'Watching', 'status': 'CURRENT'},
            'rewatching': {'name': 'Rewatching', 'status': 'REPEATING'},
            'planned': {'name': 'Planning', 'status': 'PLANNING'},
            'completed': {'name': 'Completed', 'status': 'COMPLETED'},
            'on_hold': {'name': 'Paused', 'status': 'PAUSED'},
            'dropped': {'name': 'Dropped', 'status': 'DROPPED'}
        }

        FORMAT_MAP = {
            'tv': 'TV',
            'tv_special': 'TV_SHORT',
            'special': 'SPECIAL',
            'ova': 'OVA',
            'ona': 'ONA',
            'movie': 'MOVIE',
            'music': 'MUSIC'
        }

        STATUS_ANIME_MAP = {
            'released': 'FINISHED',
            'ongoing': 'RELEASING',
            'anons': 'NOT_YET_RELEASED'
        }

        grouped_rates = {key: [] for key in STATUS_CONFIG.keys()}

        for rate in user_media.get('data', {}).get('userRates', []):
            st = rate.get('status')
            if st not in grouped_rates:
                continue

            anime = rate.get('anime') or {}

            season_raw = anime.get('season')
            season_val = None
            season_year_val = None
            if season_raw:
                parts = season_raw.split('_')
                season_val = parts[0].upper()
                if len(parts) > 1 and parts[1].isdigit():
                    season_year_val = int(parts[1])

            media_obj = {
                "id": int(anime['id']) if anime.get('id') else None,
                "idMal": int(anime['malId']) if anime.get('malId') else None,
                "title": {
                    "romaji": anime.get('name'),
                    "english": anime.get('english'),
                    "native": anime.get('japanese')
                },
                "description": anime.get('descriptionHtml'),
                "type": "ANIME",
                "format": FORMAT_MAP.get(anime.get('kind'), (anime.get('kind') or '').upper()),
                "status": STATUS_ANIME_MAP.get(anime.get('status'), "UNKNOWN"),
                "countryOfOrigin": "JP",
                "season": season_val,
                "seasonYear": season_year_val,
                "episodes": anime.get('episodes'),
                "duration": anime.get('duration'),
                "genres": [g.get('name') for g in anime.get('genres', []) if g.get('kind') != 'theme'],
                "synonyms": anime.get('synonyms', []),
                "averageScore": int(float(anime['score']) * 10) if anime.get('score') else None,
                "isAdult": anime.get('rating') == 'rx',
                "bannerImage": None,
                "coverImage": {
                    "color": None,
                    "medium": anime.get('poster', {}).get('mainUrl') if anime.get('poster') else None,
                    "extraLarge": anime.get('poster', {}).get('originalUrl') if anime.get('poster') else None
                },
                "studios": {
                    "nodes": [{"name": s.get('name')} for s in anime.get('studios', []) if s.get('name')]
                },
                "externalLinks": [
                    {
                        "site": link.get('kind'),
                        "url": link.get('url')
                    } for link in anime.get('externalLinks', [])
                ],
                "relations": {
                    "edges": [
                        {
                            "relationType": "OTHER",
                            "node": {
                                "id": int(rel['anime']['id']) if rel['anime'].get('id') else None,
                                "idMal": int(rel['anime']['malId']) if rel['anime'].get('malId') else None,
                                "title": {
                                    "romaji": rel['anime'].get('name'),
                                    "native": rel['anime'].get('japanese'),
                                    "english": rel['anime'].get('english')
                                },
                                "type": "ANIME",
                                "format": FORMAT_MAP.get(rel['anime'].get('kind'), rel['anime'].get('kind', '').upper())
                            }
                        }
                        for rel in anime.get('related', [])
                        if rel and rel.get('anime')
                    ]
                }
            }

            entry = {
                "id": int(rate.get('id')) if rate.get('id') else None,
                "progress": rate.get('episodes', anime.get('episodes', 0)),
                "score": rate.get('score', 0),
                "media": media_obj
            }
            grouped_rates[st].append(entry)

        lists_result = []
        for status_key, config in STATUS_CONFIG.items():
            entries = grouped_rates[status_key]
            if entries:
                lists_result.append({
                    "name": config['name'],
                    "status": config['status'],
                    "entries": entries
                })

        return {
            "data": {
                "MediaListCollection": {
                    "lists": lists_result
                }
            }
        }
    
    def refresh_shikimori(self, update: bool = True):
            self.refresh_service('Shikimori', update)

class UpdateWorker(QThread):
    finished_service = Signal(str)

    def __init__(self, service = '', parent = None):
        super().__init__()
        self.parent = parent
        self.service = service

    def run(self):
        try:
            if self.service.lower() == 'anilist':
                self.parent.update_anilist_db()
            elif self.service.lower() == 'shikimori':
                self.parent.update_shikimori_db()
            else:
                return
        except Exception as e:
            print(f"Worker Error: {e}")
        finally:
            self.finished_service.emit(self.service)