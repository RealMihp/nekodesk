import os, anitopy
from pathlib import Path
from core.db import *


VIDEO_EXTS = ('.mp4', '.mkv', '.avi')
BLACKLIST = {'SP', 'OVA', 'NC', 'OP', 'ED', 'NCED', 'NCOP'}
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
        
    @staticmethod    
    def get_title_local_data(folder_path: str) -> dict: 
        """Scans the directory for anime video files to extract metadata.

        This method performs a two-step scan (root and first-level subdirectories) 
        to find video files. It parses filenames to identify fansub groups 
        and determine the highest episode number while filtering out 
        specials (SP), OVAs, and numeric noise.

        Args:
            folder_path (str): The absolute path to the directory to be scanned.

        Returns:
            dict: A dictionary containing:
                - 'groups' (list[str]): Sorted unique names of identified fansub groups.
                - 'max_ep' (int): The highest episode number found. Returns 0 if none.
        """
        if not folder_path:
            return   

        raw_items = os.listdir(folder_path)
        video_files = set()
        dirs = set()
        funsubs = set()
        eps_set = set()
        max_ep = 0

        # First roll
        for name in raw_items:
            full_path = os.path.join(folder_path, name).replace('\\', '/')
            
            if os.path.isdir(full_path):
                dirs.add(full_path)
            else:
                if name.endswith(VIDEO_EXTS):
                    video_files.add(full_path)
        
        # Second roll
        if not video_files:
            for dir in dirs:
                second_list = os.listdir(dir)

                
                for file in second_list:
                    if file.endswith(VIDEO_EXTS):
                        video_files.add(file)
                        
        # Final
        if video_files:
            for video in video_files:
                # Parse fansub groups
                parsed = anitopy.parse(video)
                group = parsed.get('release_group')
                if group and group.upper() not in BLACKLIST: 
                    is_special = 'SP' in group.upper() or group.isdigit()
                    if not is_special:
                        funsubs.add(group)

                # Count episodes in folder
                ep_num = parsed.get('episode_number')
                if ep_num:
                    try:
                        eps_set.add(int(ep_num))
                    except (ValueError, TypeError):
                        pass
            
            max_ep = max(eps_set) if eps_set else 0

        else:
            return {
            'groups': [],
            'max_ep': 0
        }

        return {
            'groups': sorted(list(funsubs)),
            'max_ep': max(eps_set) if eps_set else 0
        }
        
