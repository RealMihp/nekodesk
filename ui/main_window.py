from PySide6.QtWidgets import QTreeWidgetItem
from core.logic import FileScanner
import sys, os
import PySide6
from PySide6.QtWidgets import *
from ui.ui_main import *
from ui.ui_settings import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.actionSelect_folder.triggered.connect(self.select_folder)
        
    def populate_tree(self, folder_path, parent_item=None):
        items = FileScanner.get_directory_structure(folder_path)
        
        for name in items:
            full_path = os.path.join(folder_path, name)
            
            item = QTreeWidgetItem(parent_item or self.ui.files_treeWidget)
            item.setText(0, name)
            
            if os.path.isdir(full_path):
                icon = self.style().standardIcon(QStyle.SP_DirIcon)
                item.setIcon(0, icon)
                
                
                item.setData(0, Qt.UserRole, full_path)
            else:
                file_icon = self.style().standardIcon(QStyle.SP_FileIcon)
                item.setIcon(0, file_icon)

    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(
            self, 
            "Choose folder",
            "",
            QFileDialog.ShowDirsOnly
        )

        if folder_path:
            print(f"Path selected: {folder_path}")
            self.ui.path_lineEdit.setText(folder_path)
            self.ui.files_treeWidget.clear()
            self.populate_tree(folder_path)

    