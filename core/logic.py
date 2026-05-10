import os, anitopy
from pathlib import Path
from core.db import *


VIDEO_EXTS = ('.mp4', '.mkv', '.avi')
BLACKLIST = {'SP', 'OVA', 'NC', 'OP', 'ED', 'NCED', 'NCOP'}
SOURCES = ('BDRIP', 'BDREMUX', 'REMUX', 'BDMV', 'WEB-DL', 'WEBRIP', 'HDTVRIP', 'DVDRIP', 'HDRIP')
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
        to find video files. It parses filenames to identify fansub groups,
        video resolution, source and determine the highest episode number while filtering out 
        specials (SP), OVAs, and numeric noise.

        Args:
            folder_path (str): The absolute path to the directory to be scanned.

        Returns:
            dict: A dictionary containing:
                - 'groups' (list[str]): Sorted unique names of identified fansub groups.
                - 'max_ep' (int): The highest episode number found. Returns 0 if none.
                - 'resolution' (str): Resolution of video.
                - 'source' (str): Source of video files (BDRip, HDTVRip, etc...)
        """
        if not folder_path:
            return {'groups': [], 'max_ep': 0, 'resolution': '', 'source': ''}

        folder_path = folder_path.replace('\\', '/')
        raw_items = os.listdir(folder_path)
        video_files = set()
        dirs = set()
        fansubs = set()
        eps_set = set()
        
        res_val = ''
        src_val = ''

        # First roll
        for name in raw_items:
            full_path = os.path.join(folder_path, name).replace('\\', '/')
            if os.path.isdir(full_path):
                dirs.add(full_path)
                if not res_val:
                    res_val = anitopy.parse(name).get('video_resolution', '')
            elif name.lower().endswith(VIDEO_EXTS):
                video_files.add(full_path)
        
        # Second roll
        if not video_files:
            for d in dirs:
                try:
                    for file in os.listdir(d):
                        if file.lower().endswith(VIDEO_EXTS):
                            video_files.add(os.path.join(d, file).replace('\\', '/'))
                            if not res_val:
                                res_val = anitopy.parse(os.path.basename(d)).get('video_resolution', '')
                except: pass

        # source in dirs
        dirs.add(folder_path)
        for d in dirs:
            dir_name_up = os.path.basename(d).upper()
            for s in SOURCES:
                if s in dir_name_up:
                    src_val = s
                    break
            if src_val: break

        # Final
        if video_files:
            for video in video_files:
                file_name = os.path.basename(video)
                parsed = anitopy.parse(file_name)
                
                # fansub groups
                group = parsed.get('release_group')
                if group and group.upper() not in BLACKLIST:
                    if 'SP' not in group.upper() and not group.isdigit():
                        fansubs.add(group)

                # resolution
                if not res_val:
                    res_val = parsed.get('video_resolution', '')

                # source in videos
                if not src_val:
                    name_up = file_name.upper()
                    for s in SOURCES:
                        if s in name_up:
                            src_val = s
                            break

                # episodes
                ep = parsed.get('episode_number')
                if ep:
                    try:
                        val = ep[-1] if isinstance(ep, list) else ep
                        eps_set.add(int(val))
                    except: pass
            
            max_ep = max(eps_set) if eps_set else 0

            if src_val:
                src_val = src_val.replace('IP', 'ip')
                src_val = src_val.replace('EMUX', 'emux')

        else:
            return {'groups': [], 'max_ep': 0, 'resolution': '', 'source': ''}

        return {
            'groups': sorted(list(fansubs)),
            'max_ep': max_ep,
            'resolution': res_val,
            'source': src_val
        }
        
