import PySide6
from PySide6.QtWidgets import QTreeWidgetItem, QMenu
from core.logic import FileScanner
from PySide6.QtGui import QDesktopServices, QAction
from PySide6.QtCore import QUrl

import sys, os

from PySide6.QtWidgets import *
from ui.title_details_window import Title_detailsWindow
from ui.rename_dialog_window import RenameWindow
from ui.ui_main import *
from ui.add_series_window import *
from ui.settings_window import *
from ui.ui_settings import *
from ui.widgets import FilesTree


PATH_ROLE = 32




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.history = []
        self.forward_stack = []
        self.ldbclient = LibraryDB()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.library_treeWidget.header().setSectionResizeMode(0, QHeaderView.Stretch)
        self.ui.library_treeWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.library_treeWidget.sortByColumn(0, Qt.AscendingOrder)

        self.ui.library_treeWidget.customContextMenuRequested.connect(self.show_library_context_menu)
        self.ui.actionSelect_folder.triggered.connect(self.select_folder)
        self.ui.actionClose_folder.triggered.connect(self.close_folder)
        self.ui.files_treeWidget.itemDoubleClicked.connect(self.open_item)
        self.ui.back_pushButton.pressed.connect(self.back)
        self.ui.refresh_pushButton.pressed.connect(self.refresh)
        self.ui.forward_pushButton.pressed.connect(self.forward)
        self.ui.addSeries_pushButton.pressed.connect(self.show_addseries)
        self.ui.actionSettings.triggered.connect(self.show_settings)

        self.ui.files_treeWidget.setDragDropOverwriteMode(False)
        self.ui.library_treeWidget.setDragEnabled(True)
        self.ui.library_treeWidget.setDragDropMode(QAbstractItemView.DragOnly)
        self.ui.files_treeWidget.setDropIndicatorShown(True)

        self.refresh_library()

    def show_details(self, anilist_id: str):
        self.details_window = Title_detailsWindow(self, anilist_id)
        
        self.details_window.show()
        
    def show_library_context_menu(self, pos):
        item = self.ui.library_treeWidget.itemAt(pos)
        if not item: return

        menu = QMenu(self)
        open_action = QAction('Details', self)
        remove_action = QAction('Remove from library', self)

        anilist_id = item.data(0, Qt.ItemDataRole.UserRole)
        open_action.triggered.connect(lambda: self.show_details(anilist_id))
        remove_action.triggered.connect(lambda: self.remove_title(anilist_id))

        menu.addAction(open_action)
        menu.addSeparator()
        menu.addAction(remove_action)

        menu.exec(self.ui.library_treeWidget.mapToGlobal(pos))

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
            db = SettingsDB()
            db.set("anilist_token", dialog.ui.serviceAniList_lineEdit.text())
            db.set("mal_token", dialog.ui.serviceMAL_lineEdit.text())
            db.set("files_template", dialog.ui.files_template_lineEdit.text())
            db.set("folder_template", dialog.ui.folder_template_lineEdit.text())
            if dialog.ui.offline_mode_checkBox.isChecked():
                db.set("offline_mode", "True")
            else:
                db.set("offline_mode", "False")
            
            print("Changed settings")
        else:
            print("Canceled changing settings")

    def populate_tree(self, folder_path):
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

    def refresh_library(self):
        widget = self.ui.library_treeWidget
        widget.clear()
        widget.setIconSize(QSize(64, 96))

        titles = self.ldbclient.get_all_titles()

        for title in titles:
            name = title.get('title_romaji') or "Unknown"
            status = title.get('status') or "N/A"
            year = str(title.get('season_year')) or "N/A"
            episodes = str(title.get('episodes')).zfill(2) or "?"
            
            item = QTreeWidgetItem([name, year, episodes])

            path = title.get('poster_small_path')
            if path and os.path.exists(path):
                item.setIcon(0, QIcon(path))
            else:
                color = title.get('poster_color')
                if color:
                    pix = QPixmap(40, 60)
                    pix.fill(QColor(color))
                    item.setIcon(0, QIcon(pix))

            item.setData(0, Qt.ItemDataRole.UserRole, title.get('anilist_id'))

            header = widget.header()
            header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

            widget.addTopLevelItem(item)
        imgmClient = ImageManager()
        imgmClient.clear_temp_folder()

    def open_rename_dialog(self, title_id: str, folder_path: str):
        title_data = self.ldbclient.get_title(title_id) # dict

        print(f"{title_data['title_romaji']} -> {folder_path}")

        dialog = RenameWindow(self, title_data=title_data, folder_path=folder_path)
        
        if dialog.exec(): 
            print(f"Rename dialog OK")
            dialog.rename()
        else:
            print("Rename dialog Cancel")



