from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem
from PySide6.QtCore import Qt

from PySide6.QtWidgets import *


PATH_ROLE = 32

class FilesTree(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setDragDropMode(QAbstractItemView.DragDrop) 
        self.setDropIndicatorShown(True)
        self.setDefaultDropAction(Qt.CopyAction)
        

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-qabstractitemmodeldatalist"):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("application/x-qabstractitemmodeldatalist"):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        print('dropEvent')
        target_item = self.itemAt(event.pos())
        if not target_item:
            event.ignore()
            return

        target_path = target_item.data(0, PATH_ROLE)

        source_item = event.source().currentItem()
        if not source_item:
            return
            
        title_id = source_item.data(0, Qt.UserRole)

        self.window().open_rename_dialog(title_id, target_path)
        

        event.accept()