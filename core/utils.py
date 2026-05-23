import os
import shutil
import requests
from PySide6.QtGui import QColor, QIcon, QPixmap

class ImageManager:
    def __init__(self, posters_path="data\\posters", temp_posters_path = "data\\temp\\posters"):
        """
        Initialize the manager with a directory to store downloaded posters.
        """
        self.posters_path = posters_path
        self.temp_posters_path = temp_posters_path
        os.makedirs(self.posters_path, exist_ok=True)


    def clear_temp_folder(self):
        shutil.rmtree(self.temp_posters_path)
        os.makedirs(self.temp_posters_path, exist_ok=True)
        return True

    def get_poster(self, link: str, return_pixmap: bool = False, is_temp: bool = False) -> str | QPixmap | None:
        """
        Load a poster from a local file or download it if it doesn't exist.
        :param link: Direct URL to the image
        :param return_pixmap: If True returns QPixmap else returns link (string)
        """
        try:
            parts = link.split("/")
            file_name = f"{parts[-2]}_{parts[-1]}" 
            def_folder_path=os.path.join("data/posters")
            
            if not is_temp:
                folder_path = os.path.join(self.posters_path)
                
            else:
                folder_path = os.path.join(self.temp_posters_path)

            file_path = os.path.join(folder_path, file_name).replace('\\', '/')
            def_file_path = os.path.join(def_folder_path, file_name).replace('\\', '/')
            os.makedirs(folder_path, exist_ok=True)
            os.makedirs(def_folder_path, exist_ok=True)

            # 1. Check if the file already exists locally
            if os.path.exists(file_path):
                if return_pixmap: return QPixmap(file_path) 
                else: return file_path
            
            if os.path.exists(def_file_path):
                if return_pixmap: return QPixmap(def_file_path)
                else: return def_file_path

            # 2. If not, download it
            try:
                response = requests.get(link, timeout=10)
                if response.status_code == 200:
                    # Save the image to the disk
                    with open(file_path, "wb") as f:
                        f.write(response.content)
                    
                    if return_pixmap:
                        # Create QPixmap from the downloaded data
                        pixmap = QPixmap()
                        pixmap.loadFromData(response.content)
                        return pixmap
                    else:
                        return file_path
                    
            except Exception as e:
                print(f"Network error while saving image: {e}")
            
            return None
            
        except Exception as e:
            print(f"Error processing poster link: {e}")
            return None
        

    def get_posters(self, links: list, session=None, is_temp: bool = False) -> dict | None:
        if not is_temp:
            posters_path = self.posters_path
        else:
            posters_path = self.temp_posters_path
        s = session or requests.Session()
        posters_data = {}
        
        os.makedirs(posters_path, exist_ok=True)

        for link in links:
            if not link: continue

            parts = link.split("/")
            file_name = f"{parts[-2]}_{parts[-1]}" 

            file_path = os.path.join(posters_path, file_name).replace('\\', '/')
            pixmap = QPixmap()

            try:
                # 1. Check if the file already exists locally
                if os.path.exists(file_path):
                    if pixmap.load(file_path):
                        posters_data[link] = (pixmap, file_path)
                        continue

                # 2. If not, download it
                response = s.get(link, timeout=10)
                if response.status_code == 200:
                    with open(file_path, "wb") as f:
                        f.write(response.content)
                    if pixmap.loadFromData(response.content):
                        posters_data[link] = (pixmap, file_path)
                else:
                    posters_data[link] = None

            except Exception as e:
                print(f"Error {link}: {e}")
                posters_data[link] = None

        return posters_data

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
