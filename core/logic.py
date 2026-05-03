import os
from pathlib import Path
from core.db import *

class FileScanner:
    @staticmethod
    def get_items(folder_path):
        try:
            folder_path = folder_path.replace('\\', '/')
            raw_items = os.listdir(folder_path)
            
            processed_items = []
            for name in raw_items:
                full_path = os.path.join(folder_path, name).replace('\\', '/')
                processed_items.append({
                    'name': name,
                    'path': full_path,
                    'is_dir': os.path.isdir(full_path)
                })
            return processed_items
        except Exception as e:
            print(f"Failed to get items: {e}")
            return []
        


class FileRenamer:
    def __init__(self):
        self.template = "{title_romaji ({season_year})- S{season_number}E{episode_number}} [{source}] [{quality}]" # load template from settings

    def generate_name(self, title_info: dict, path: str) -> str:
        template = self.template # "{title_romaji ({season_year})- S{season_number}E{episode_number}} [{source}] [{quality}]"

        # {title_romaji} {title_native} {title_english} {season_number} {episode_number} {type} {status} {season} {season_year} {duration} {episodes} {score} {studio} {isAdult} {quality} {source} (BDRip, WEBRip...) {translationStudio}
        original_name = ...

        data = {
            "title_romaji": title_info.get("title_romaji", "Unknown"),
            "title_native": title_info.get("title_native", "Unknown"),
            "title_english": title_info.get("title_english", "Unknown"),
            "type": title_info.get("format", "Unknown"),
            "status": title_info.get("status", "Unknown"),
            "duration": title_info.get("duration", "Unknown"),
            "studio": title_info.get("studio", "Unknown"),
            "isAdult": "NSFW" if title_info.get("format") == 1 else "SFW",
            "season": title_info.get("season", "Unknown"),
            "season_year": title_info.get("season_year", "?"),
            "season_number": title_info.get("season_number", "1"),
            "episode_number": title_info.get("episode_number", "01"),
            "quality": "...", # quality from the original file name
            "source": "...", # source from the original file name
            "translationStudio": "...", # translation studio from the original file name
            
        }

        try:
            return template.format(**data)
        except KeyError as e:
            print(f"Error: Missing key {e} in template")
            return original_name


    def rename(self, path: str, name: str) -> bool:
        file_path = Path(path)

        try: 
            file_path.rename(name)
            return True
        except Exception:
            return False

    def execute(self, title_info: dict, path: str) -> bool:
        """Renames file using template"""
        if path:
            name = self.generate_name(title_info, path)
        else: return False

        if name:
            return self.rename(path, name)
        else: return False

