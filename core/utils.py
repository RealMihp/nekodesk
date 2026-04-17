import os
import requests
from PySide6.QtGui import QColor, QIcon, QPixmap

class ImageManager:
    def __init__(self, posters_path="data/posters"):
        """
        Initialize the manager with a directory to store downloaded posters.
        """
        self.posters_path = posters_path
        os.makedirs(self.posters_path, exist_ok=True)

    def get_poster(self, link: str) -> QPixmap | None:
        """
        Load a poster from a local file or download it if it doesn't exist.
        :param link: Direct URL to the image
        :return: QPixmap object or None if failed
        """
        try:
            file_name = link.split("/")[-1]
            

            folder_path = os.path.join(self.posters_path)
            file_path = os.path.join(folder_path, file_name)

            os.makedirs(folder_path, exist_ok=True)

            # 1. Check if the file already exists locally
            if os.path.exists(file_path):
                return QPixmap(file_path)

            # 2. If not, download it
            try:
                response = requests.get(link, timeout=10)
                if response.status_code == 200:
                    # Save the image to the disk
                    with open(file_path, "wb") as f:
                        f.write(response.content)
                    
                    # Create QPixmap from the downloaded data
                    pixmap = QPixmap()
                    pixmap.loadFromData(response.content)
                    return pixmap
                    
            except Exception as e:
                print(f"Network error while saving image: {e}")
            
            return None
            
        except Exception as e:
            print(f"Error processing poster link: {e}")
            return None
        

    def get_posters(self, links, session=None) -> dict | None:
        posters_path = self.posters_path
        s = session or requests.Session()
        posters_data = {}
        
        os.makedirs(posters_path, exist_ok=True)

        for link in links:
            if not link: continue
            
            file_name = link.split("/")[-1]
            file_path = os.path.join(posters_path, file_name)
            pixmap = QPixmap()

            try:
                # 1. Check if the file already exists locally
                if os.path.exists(file_path):
                    if pixmap.load(file_path):
                        posters_data[link] = pixmap
                        continue

                # 2. If not, download it
                response = s.get(link, timeout=10)
                if response.status_code == 200:
                    with open(file_path, "wb") as f:
                        f.write(response.content)
                    if pixmap.loadFromData(response.content):
                        posters_data[link] = pixmap
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