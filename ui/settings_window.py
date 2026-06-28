import os
import keyring
from datetime import datetime

from PySide6.QtWidgets import *
from ui.ui_add_series import *
from ui.ui_settings import *
from core.db import SettingsDB
from core.api.anilist_api import *
from ui.pin_dialog_window import *
from core.utils import *


class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_SettingsWindow()
        self.ui.setupUi(self)

        # DB
        self.db = SettingsDB()
        self.al_db = SettingsDB('data/anilist/anilist.db')
        self.al_imgManager = ImageManager('data/anilist')
        self.logged_in = False

        self.setup_connections()
        self.load_settings()
        self.update_anilist_ui()

    def setup_connections(self):
        """Sets up all connections"""
        self.ui.qbit_checkBox.checkStateChanged.connect(self.handle_checkboxes)
        self.ui.anilist_auth_pushButton.pressed.connect(self.anilist_auth)

    def load_settings(self):
        """Loads and inserts data at launch"""
        # Templates
        templates = ["files_template", "folder_template", "poster_template", "banner_template", "torrent_template"]
        for t in templates:
            line_edit = getattr(self.ui, f"{t}_lineEdit")
            line_edit.setText(self.db.get(t, line_edit.text()))

        # Language priority
        lang_priority = self.db.get("title_lang_priority", "Romaji,English,Native").split(",")
        if len(lang_priority) == 3:
            self.ui.lang_priority_1_comboBox.setCurrentText(lang_priority[0])
            self.ui.lang_priority_2_comboBox.setCurrentText(lang_priority[1])
            self.ui.lang_priority_3_comboBox.setCurrentText(lang_priority[2])

        # qBit
        qbit_enabled = self.db.get("qbit") == "True"
        self.ui.qbit_checkBox.setChecked(qbit_enabled)
        self.handle_checkboxes()

        self.ui.offline_mode_checkBox.setChecked(self.db.get("offline_mode") == "True")

        self.ui.ip_lineEdit.setText(self.db.get("qbit_ip", "localhost"))
        self.ui.port_doubleSpinBox.setValue(float(self.db.get("qbit_port", 8080)))
        
        username = self.db.get("qbit_username", "admin")
        self.ui.username_lineEdit.setText(username)
        
        password = keyring.get_password("nekodesk", username)
        if password:
            self.ui.password_lineEdit.setText(password)

    def handle_checkboxes(self):
        state = self.ui.qbit_checkBox.isChecked()
        for widget in [self.ui.ip_lineEdit, self.ui.port_doubleSpinBox, self.ui.username_lineEdit, self.ui.password_lineEdit]:
            widget.setEnabled(state)
        self.ui.torrent_template_widget.setVisible(state)

    def update_anilist_ui(self):
        """Loads and inserts AniList data"""
        username = self.al_db.get('username', '')
        self.logged_in = bool(username)

        if self.logged_in:
            self.ui.logged_in_as_label.setText(f'Logged in as {username}')
            self.ui.anilist_auth_pushButton.setText('Log out')
            self.ui.al_username_label.setText(f'Username : {username}')
            
            # Date
            created_at = self.al_db.get('created_at')
            if created_at:
                readable_date = datetime.fromtimestamp(int(created_at)).strftime("%d %B %Y")
                self.ui.al_createdAt_label.setText(f'Account created : {readable_date}')
            
            self.ui.al_anime_count_label.setText(f"Anime count : {self.al_db.get('anime_count', '0')}")
            
            # Banner
            banner_path = self.al_db.get('banner_path', '')
            self.ui.al_widget.setStyleSheet(f"QWidget#al_widget {{ background-image: url({banner_path}); background-position: center; }}")
            
            # Avatar
            avatar_path = self.al_db.get('avatar_path')
            if avatar_path and os.path.exists(avatar_path):
                pixmap = QPixmap(avatar_path).scaledToWidth(150, Qt.TransformationMode.SmoothTransformation)
                self.ui.avatar_label.setPixmap(pixmap)
                self.ui.avatar_label.setFixedWidth(150)
                
            self.ui.al_widget.show()
        else:
            # Default
            self.ui.logged_in_as_label.setText('Not logged in')
            self.ui.anilist_auth_pushButton.setText('Log in')
            self.ui.al_widget.hide()
            self.ui.avatar_label.setPixmap(QPixmap())
            self.ui.al_username_label.setText('Username : ')
            self.ui.al_createdAt_label.setText('Account created : ')
            self.ui.al_anime_count_label.setText('Anime count : ')
            self.ui.al_widget.setStyleSheet('')

        # Theme
        self.apply_theme_styles()

    def apply_theme_styles(self):
        bg_color = "rgba(30, 30, 30, 160)" if otherUtils.is_dark_theme() else "rgba(255, 255, 255, 160)"
        self.ui.al_widget_2.setStyleSheet(f"QWidget#al_widget_2 {{ background-color: {bg_color} }}")

    def anilist_auth(self):
        os.makedirs("data/anilist", exist_ok=True)
        
        if self.logged_in:
            # Logout
            keys_to_clear = ['id', 'username', 'avatar_link', 'banner_link', 'avatar_path', 'banner_path', 'created_at', 'anime_count']
            for key in keys_to_clear:
                self.al_db.set(key, '')
            keyring.set_password('AniList_Token', str(self.al_db.get('id', '')), '')
            
            self.update_anilist_ui()
            return

        # Login
        client = AniListClient()
        client.open_auth_url()
        dialog = PINWindow()

        dialog.setWindowFlags(dialog.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        
        if dialog.exec():
            token = dialog.ui.AniList_Auth_lineEdit.text()
            res_json = client.save_token(token)
            
            if not res_json or 'data' not in res_json or not res_json['data'].get('Viewer'):
                print("[Login] AniList auth error: Invalid token!")
                return
                
            user_data = res_json['data']['Viewer']
                
            # Data
            user_id = str(user_data.get('id'))
            username = user_data.get('name', 'N/A')
            avatar_link = user_data.get('avatar', {}).get('large')
            banner_link = user_data.get('bannerImage')
            created_at = user_data.get('createdAt')
            anime_count = user_data.get('statistics', {}).get('anime', {}).get('count', 0)

            # Assets
            avatar_path = self.al_imgManager.get_poster(avatar_link, f"avatar.{avatar_link.split('.')[-1]}", return_pixmap=False)
            banner_path = self.al_imgManager.get_poster(banner_link, f"banner.{banner_link.split('.')[-1]}", return_pixmap=False)

            # Save
            self.al_db.set('id', user_id)
            self.al_db.set('username', username)
            self.al_db.set('avatar_link', avatar_link)
            self.al_db.set('banner_link', banner_link)
            self.al_db.set('avatar_path', avatar_path)
            self.al_db.set('banner_path', banner_path)
            self.al_db.set('created_at', str(created_at))
            self.al_db.set('anime_count', str(anime_count))

            self.update_anilist_ui()

    def accept(self):
        """Save settings"""
        # Template
        templates = ["files_template", "folder_template", "poster_template", "banner_template", "torrent_template"]
        for t in templates:
            line_edit = getattr(self.ui, f"{t}_lineEdit")
            self.db.set(t, line_edit.text())

        # Checkboxes
        self.db.set("offline_mode", str(self.ui.offline_mode_checkBox.isChecked()))
        self.db.set("qbit", str(self.ui.qbit_checkBox.isChecked()))
        
        # Comboboxes
        lang_priority = f'{self.ui.lang_priority_1_comboBox.currentText()},{self.ui.lang_priority_2_comboBox.currentText()},{self.ui.lang_priority_3_comboBox.currentText()}'
        self.db.set("title_lang_priority", lang_priority)
        
        # qBit
        self.db.set("qbit_ip", self.ui.ip_lineEdit.text())
        self.db.set("qbit_port", str(int(self.ui.port_doubleSpinBox.value())))
        
        username = self.ui.username_lineEdit.text()
        self.db.set("qbit_username", username)
        
        password = self.ui.password_lineEdit.text()
        if password:
            keyring.set_password("nekodesk", username, password)

        super().accept()