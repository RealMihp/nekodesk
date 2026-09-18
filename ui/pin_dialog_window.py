import PySide6
from PySide6.QtWidgets import QDialog, QMessageBox
from ui.ui_pin_dialog import Ui_PIN_Dialog

class PINWindow(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.ui = Ui_PIN_Dialog()
        self.ui.setupUi(self)
        self.parent = parent

        self.ui.AniList_Auth_buttonBox.accepted.connect(self.accept)

    def accept(self):
        token = self.ui.AniList_Auth_lineEdit.text()
        if not token:
                QMessageBox.warning(self, "Error", "Invalid token!")
                return
        
        super().accept()
