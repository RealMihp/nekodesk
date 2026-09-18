import os
import keyring
from datetime import datetime

from PySide6.QtWidgets import QDialog
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

from ui.ui_settings import Ui_SettingsWindow
from core.db import SettingsDB
from core.api.anilist_api import AniListClient
from core.api.shikimori_api import ShikimoriClient
from ui.pin_dialog_window import PINWindow
from core.utils import ImageManager, DownloadPostersWorker, otherUtils


class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_SettingsWindow()
        self.ui.setupUi(self)
        self.parent = parent

        self.db = SettingsDB()
        self.al_db = SettingsDB('data/anilist/anilist.db')
        self.sh_db = SettingsDB('data/shikimori/shikimori.db')
        self.al_imgManager = ImageManager('data/anilist')
        self.sh_imgManager = ImageManager('data/shikimori')
        self.al_logged_in = False
        self.sh_logged_in = False

        self.avatar_link = None
        self.profile_banner_link = None
        self.sh_avatar_link = None

        self.setup_connections()
        self.load_settings()
        self.update_anilist_ui()
        self.update_shikimori_ui()

    def setup_connections(self):
        self.ui.qbit_checkBox.checkStateChanged.connect(self.handle_checkboxes)
        self.ui.anilist_auth_pushButton.pressed.connect(self.anilist_auth)
        self.ui.shikimori_link_pushButton.pressed.connect(self.shikimori_link)

    def load_settings(self):
        templates = ["files_template", "folder_template", "poster_template", "banner_template", "torrent_template"]
        for t in templates:
            line_edit = getattr(self.ui, f"{t}_lineEdit")
            line_edit.setText(self.db.get(t, line_edit.text()))

        lang_priority = self.db.get("title_lang_priority", "Romaji,English,Native").split(",")
        if len(lang_priority) == 3:
            self.ui.lang_priority_1_comboBox.setCurrentText(lang_priority[0])
            self.ui.lang_priority_2_comboBox.setCurrentText(lang_priority[1])
            self.ui.lang_priority_3_comboBox.setCurrentText(lang_priority[2])

        qbit_enabled = self.db.get("qbit") == "True"
        self.ui.qbit_checkBox.setChecked(qbit_enabled)
        self.handle_checkboxes()


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
        username = self.al_db.get('username', '')
        self.al_logged_in = bool(username)

        if self.al_logged_in:
            self.ui.anilist_logged_in_as_label.setText(f'Logged in as {username}')
            self.ui.anilist_auth_pushButton.setText('Log out')
            
            
            created_at = self.al_db.get('created_at')
            if created_at and created_at.isdigit():
                readable_date = datetime.fromtimestamp(int(created_at)).strftime("%d %B %Y")
                self.ui.al_createdAt_label.setText(f'Account created : {readable_date}')
            
            self.ui.al_anime_count_label.setText(f"Anime count : {self.al_db.get('anime_count', '0')}")
            
            banner_path = self.al_db.get('banner_path', '').replace('\\', '/')
            self.ui.al_widget.setStyleSheet(f"QWidget#al_widget {{ background-image: url({banner_path}); background-position: center; }}")
            
            avatar_path = self.al_db.get('avatar_path')
            if avatar_path and os.path.exists(avatar_path):
                pixmap = QPixmap(avatar_path).scaledToWidth(120, Qt.TransformationMode.SmoothTransformation)
                self.ui.anilist_avatar_label.setPixmap(pixmap)
                self.ui.anilist_avatar_label.setFixedWidth(120)

            self.ui.al_widget.show()

        else:
            self.ui.anilist_logged_in_as_label.setText('Not logged in')
            self.ui.anilist_auth_pushButton.setText('Log in')
            self.ui.al_widget.hide()
            self.ui.anilist_avatar_label.setPixmap(QPixmap())
            
            self.ui.al_createdAt_label.setText('Account created : ')
            self.ui.al_anime_count_label.setText('Anime count : ')
            self.ui.al_widget.setStyleSheet('')

        self.apply_theme_styles()

    def apply_theme_styles(self):
        bg_color = "rgba(30, 30, 30, 160)" if otherUtils.is_dark_theme() else "rgba(255, 255, 255, 160)"
        self.ui.al_widget_2.setStyleSheet(f"QWidget#al_widget_2 {{ background-color: {bg_color} }}")

    def anilist_auth(self):
        os.makedirs("data/anilist", exist_ok=True)
        
        if self.al_logged_in:
            keys_to_clear = ['id', 'username', 'avatar_link', 'banner_link', 'avatar_path', 'banner_path', 'created_at', 'anime_count']
            for key in keys_to_clear:
                self.al_db.set(key, '')
            keyring.set_password('AniList_Token', str(self.al_db.get('id', '')), '')
            
            self.update_anilist_ui()
            return

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
                
            user_id = str(user_data.get('id'))
            username = user_data.get('name', 'N/A')
            avatar_link = user_data.get('avatar', {}).get('large')
            banner_link = user_data.get('bannerImage')
            created_at = user_data.get('createdAt')
            anime_count = user_data.get('statistics', {}).get('anime', {}).get('count', 0)

            self.avatar_link = avatar_link
            self.profile_banner_link = banner_link

            self.ui.anilist_avatar_label.setPixmap(QPixmap())

            profile_links = [link for link in [self.avatar_link, self.profile_banner_link] if link]
            
            if profile_links and self.parent and hasattr(self.parent, 'thread_pool'):
                worker = DownloadPostersWorker(profile_links, 'data/anilist')
                worker.signals.finished.connect(self.on_anilist_media_ready)
                self.parent.thread_pool.start(worker)

            self.al_db.set('id', user_id)
            self.al_db.set('username', username)
            self.al_db.set('avatar_link', avatar_link or '')
            self.al_db.set('banner_link', banner_link or '')
            self.al_db.set('created_at', str(created_at) if created_at else '')
            self.al_db.set('anime_count', str(anime_count))

            self.al_logged_in = True
            self.update_anilist_ui()

    def shikimori_link(self):
        os.makedirs("data/shikimori", exist_ok=True)
        if self.sh_logged_in:
            self.sh_db.set('id', '')
            self.sh_db.set('username', '')
            self.sh_db.set('avatar_link', '')
            self.sh_db.set('avatar_path', '')
            self.ui.shikimori_link_pushButton.setText('Link')
            self.ui.shikimori_username_link_lineEdit.setEnabled(True)
            self.sh_logged_in = False
            self.update_shikimori_ui()

        else:
            username = self.ui.shikimori_username_link_lineEdit.text()
            if username:
                client = ShikimoriClient()
                data = client.get_user_data(username)
                
                if data:
                    user_id = data.get('id')
                    avatar_link = data.get('avatarUrl')

                    if user_id:
                        client.get_user_media_list(user_id)
                        self.sh_db.set('id', str(user_id))
                        self.sh_db.set('username', username)
                        self.sh_db.set('avatar_link', avatar_link or '')

                        self.sh_avatar_link = avatar_link
                        self.ui.shikimori_avatar_label.setPixmap(QPixmap())
                        
                        if avatar_link and self.parent and hasattr(self.parent, 'thread_pool'):
                            worker = DownloadPostersWorker([avatar_link], 'data/shikimori')
                            worker.signals.finished.connect(self.on_shikimori_media_ready)
                            self.parent.thread_pool.start(worker)

                        self.sh_logged_in = True
                        self.update_shikimori_ui()

    def update_shikimori_ui(self):
        username = self.sh_db.get('username', '')
        self.sh_logged_in = bool(username)

        if self.sh_logged_in:
            self.ui.shikimori_logged_in_as_label.setText(f'Logged in as {username}')
            self.ui.shikimori_username_link_lineEdit.setText(username)
            self.ui.shikimori_link_pushButton.setText('Unlink')
            self.ui.shikimori_username_link_lineEdit.setEnabled(False)
            
            avatar_path = self.sh_db.get('avatar_path')
            if avatar_path and os.path.exists(avatar_path):
                pixmap = QPixmap(avatar_path).scaledToWidth(120, Qt.TransformationMode.SmoothTransformation)
                self.ui.shikimori_avatar_label.setPixmap(pixmap)
                self.ui.shikimori_avatar_label.setFixedWidth(120)

            

        else:
            self.ui.shikimori_logged_in_as_label.setText('Not logged in')
            self.ui.shikimori_link_pushButton.setText('Link')
            
            self.ui.shikimori_avatar_label.setPixmap(QPixmap())
            self.ui.shikimori_username_link_lineEdit.setEnabled(True)

    def on_anilist_media_ready(self, posters_data: dict):
        avatar_path = posters_data.get(self.avatar_link) if self.avatar_link else None
        banner_path = posters_data.get(self.profile_banner_link) if self.profile_banner_link else None

        if avatar_path and os.path.exists(avatar_path):
            self.al_db.set('avatar_path', avatar_path)

        if banner_path and os.path.exists(banner_path):
            self.al_db.set('banner_path', banner_path)

        self.update_anilist_ui()

    def on_shikimori_media_ready(self, posters_data: dict):
        avatar_path = posters_data.get(self.sh_avatar_link) if self.sh_avatar_link else None

        if avatar_path and os.path.exists(avatar_path):
            self.sh_db.set('avatar_path', avatar_path)

        self.update_shikimori_ui()

    def accept(self):
        templates = ["files_template", "folder_template", "poster_template", "banner_template", "torrent_template"]
        for t in templates:
            line_edit = getattr(self.ui, f"{t}_lineEdit")
            self.db.set(t, line_edit.text())

        self.db.set("qbit", str(self.ui.qbit_checkBox.isChecked()))
        
        lang_priority = f'{self.ui.lang_priority_1_comboBox.currentText()},{self.ui.lang_priority_2_comboBox.currentText()},{self.ui.lang_priority_3_comboBox.currentText()}'
        self.db.set("title_lang_priority", lang_priority)
        
        self.db.set("qbit_ip", self.ui.ip_lineEdit.text())
        self.db.set("qbit_port", str(int(self.ui.port_doubleSpinBox.value())))
        
        username = self.ui.username_lineEdit.text()
        self.db.set("qbit_username", username)
        
        password = self.ui.password_lineEdit.text()
        if password:
            keyring.set_password("nekodesk", username, password)

        super().accept()