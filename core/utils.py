import os
import shutil
import requests
from PySide6.QtGui import QColor, QIcon, QPixmap
from PySide6.QtCore import QRunnable, Slot, QObject, Signal
import winreg

import urllib


class ImageManager:
    def __init__(self, posters_path="data\\posters", temp_posters_path = "data\\temp\\posters"):
        """
        Initialize the manager with a directory to store downloaded posters.
        """
        self.posters_path = posters_path
        self.temp_posters_path = temp_posters_path
        os.makedirs(self.posters_path, exist_ok=True)


    def clear_temp_folder(self):
        os.makedirs(self.temp_posters_path, exist_ok=True)
        shutil.rmtree(self.temp_posters_path)
        os.makedirs(self.temp_posters_path, exist_ok=True)
        return True


    def get_color_icon(self, hex_color: str, width=64, height=96):
        pixmap = QPixmap(width, height)
        
        color = QColor(hex_color) if hex_color else QColor("#cccccc")

        pixmap.fill(color)
        
        return QIcon(pixmap)
    
    def get_color_pixmap(self, hex_color: str, width=64, height=96):
        pixmap = QPixmap(width, height)
        
        color = QColor(hex_color) if hex_color else QColor("#cccccc")

        pixmap.fill(color)
        
        return pixmap
    
class PostersSignals(QObject):
    # dict[link, path]
    finished = Signal(dict)

class DownloadPostersWorker(QRunnable):
    def __init__(self, links: list, posters_path: str):
        super().__init__()
        self.links = links
        self.posters_path = posters_path
        self.signals = PostersSignals()

    @Slot()
    def run(self):
        os.makedirs(self.posters_path, exist_ok=True)
        posters_data = {}
        
        with requests.Session() as s:
            for link in self.links:
                if not link: 
                    continue

                clean_link = urllib.parse.urlparse(link).path
                parts = clean_link.split("/")
                file_name = f"{parts[-2]}_{parts[-1]}"
                file_path = os.path.join(self.posters_path, file_name).replace('\\', '/')
                

                try:
                    if os.path.exists(file_path):
                        posters_data[link] = file_path
                        continue

                    response = s.get(link, timeout=10)
                    if response.status_code == 200:
                        with open(file_path, "wb") as f:
                            f.write(response.content)
                        posters_data[link] = file_path
                    else:
                        posters_data[link] = None

                except Exception as e:
                    print(f"Download error {link}: {e}")
                    posters_data[link] = None

        self.signals.finished.emit(posters_data)
    
class FileManager:
    def __init__(self):
        ...

    def rename_file(self, old_path, new_path):
        if os.path.exists(old_path):
            os.rename(old_path, new_path)

    def rename_folder(self, old_folder_path, new_folder_name) -> str | None:
        parent_dir = os.path.dirname(old_folder_path)

        new_folder_path = os.path.join(parent_dir, new_folder_name).replace('\\', '/')

        if os.path.exists(old_folder_path) and os.path.isdir(old_folder_path):
            if not os.path.exists(new_folder_path):
                try:
                    os.rename(old_folder_path, new_folder_path)
                    print(f"Folder successfully renamed:\n{old_folder_path} -> {new_folder_path}")
                    return new_folder_path
                except Exception as e:
                    print(f"Rename error:\n{old_folder_path} : {e}")
            else:
                print(f"Error: {new_folder_path} is already exists!")
        else:
            print(f"Error: {old_folder_path} does not exists!")

class PreferencesManager:
    def __init__(self, db):
        from core.db import SettingsDB
        self.ldb = db
        self.sdb = SettingsDB()
        
    def get_title_title(self, anilist_id: str) -> str:
        if not anilist_id:
            return None
        title_lang_priority = self.sdb.get("title_lang_priority", "Romaji,English,Native").split(",")
        title_data = self.ldb.get_title(anilist_id)
        title_langs = {
            "romaji": title_data.get("title_romaji"),
            "english": title_data.get("title_english"),
            "native": title_data.get("title_native")
        }

        for lang in title_lang_priority:
            lang_key = lang.lower()
            title_value = title_langs.get(lang_key)

            if title_value:
                return title_value
                
        return title_langs["romaji"] or title_langs["english"] or title_langs["native"] or ""

class otherUtils():
    @staticmethod
    def is_dark_theme():
        try:
            registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
            key = winreg.OpenKey(registry, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            return value == 0
        except Exception:
            return True