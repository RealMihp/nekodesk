import PySide6
from PySide6.QtWidgets import QTreeWidgetItem
from core.logic import FileScanner
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl

import sys, os

from PySide6.QtWidgets import *
from ui.ui_main import *
from ui.add_series_window import *
from ui.settings_window import *
from ui.ui_settings import *


PATH_ROLE = 32




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.history = []
        self.forward_stack = []

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.actionSelect_folder.triggered.connect(self.select_folder)
        self.ui.actionClose_folder.triggered.connect(self.close_folder)
        self.ui.files_treeWidget.itemDoubleClicked.connect(self.open_item)
        self.ui.back_pushButton.pressed.connect(self.back)
        self.ui.refresh_pushButton.pressed.connect(self.refresh)
        self.ui.forward_pushButton.pressed.connect(self.forward)
        self.ui.addSeries_pushButton.pressed.connect(self.show_addseries)
        self.ui.actionSettings.triggered.connect(self.show_settings)
        
    def show_addseries(self):
        dialog = AddSeriesWindow(self)
        
        if dialog.exec(): 
            print(f"Added series")
           
        else:
            print("Canceled adding series")

    def show_settings(self):
        dialog = SettingsWindow(self)

        if dialog.exec():
            db = SettingsDB()
            db.set("tvdb_key", dialog.ui.serviceTVDB_lineEdit.text())
            db.set("tmdb_key", dialog.ui.serviceTMDB_lineEdit.text())
            db.set("anilist_token", dialog.ui.serviceAniList_lineEdit.text())
            db.set("mal_token", dialog.ui.serviceMAL_lineEdit.text())
            
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


            