import sqlite3
import os
import json
from core.utils import *

class SettingsDB:
    def __init__(self, db_path='data/settings.db'):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self._create_table()
        

    def _create_table(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS settings (
                    setting_key TEXT PRIMARY KEY,
                    setting_value TEXT
                )
            ''')


    def set(self, key, value):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO settings (setting_key, setting_value) VALUES (?, ?)",
                (key, str(value))
            )

    def get(self, key, default=None):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT setting_value FROM settings WHERE setting_key = ?", 
                (key,)
            )
            row = cursor.fetchone()
            return row[0] if row else default
        
class LibraryDB:
    def __init__(self, db_path='data/library.db'):
        self.db_path = db_path
        self._create_tables()
        self.utilsClient = ImageManager()
    
    def _create_tables(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS library (
                    anilist_id TEXT PRIMARY KEY UNIQUE,
                    mal_id TEXT UNIQUE,
                    title_romaji TEXT,
                    title_english TEXT,
                    title_native TEXT,
                    desc TEXT,
                    format TEXT,
                    status TEXT,
                    origin_country TEXT,
                    season TEXT,
                    season_year INTEGER,
                    episodes INTEGER,
                    duration INTEGER,
                    genres TEXT,
                    synonyms TEXT,
                    score INTEGER,
                    is_adult BOOLEAN,
                    poster_color TEXT,
                    poster_small_link TEXT,
                    poster_large_link TEXT,
                    poster_small_path TEXT,
                    poster_large_path TEXT,
                    banner_link TEXT,
                    banner_path TEXT,
                    studio TEXT
                )
            ''')
            
    
    def add_title(self, title_data):
        """
        Saves metadata to the library table.
        title_data: A list containing all the info from API.
        """
        #title_data = title_data[number]
        d = title_data

        with sqlite3.connect(self.db_path) as conn:
            query = '''
                INSERT OR REPLACE INTO library (anilist_id, mal_id, title_romaji, title_english, title_native, desc, format, status, origin_country, season,
                season_year, episodes, duration, genres, synonyms, score, is_adult, poster_color, poster_small_link, poster_large_link, poster_small_path, poster_large_path,
                banner_link, banner_path, studio
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
            
            medium = d.get('coverImage', {}).get('medium')
            extraLarge = d.get('coverImage', {}).get('extraLarge')
            banner = d.get('bannerImage')
            links = [medium, extraLarge, banner]

            paths = self.utilsClient.get_posters(links)
            path_small = paths.get(medium, (None, None))[1]
            path_extraLarge = paths.get(extraLarge, (None, None))[1]
            path_banner = paths.get(banner, (None, None))[1]

            
            values = (
                d.get('id'),
                d.get('idMal'),
                d.get('title', {}).get('romaji'),
                d.get('title', {}).get('english'),
                d.get('title', {}).get('native'),
                d.get('description'),
                d.get('format'),
                d.get('status'),
                d.get('countryOfOrigin'),
                d.get('season'),
                d.get('seasonYear'),
                d.get('episodes'),
                d.get('duration'),
                ', '.join(d.get('genres')),
                ', '.join(d.get('synonyms')),
                d.get('averageScore'),
                d.get('isAdult'),
                d.get('coverImage', {}).get('color'),
                medium,
                extraLarge,
                path_small,
                path_extraLarge,
                banner,
                path_banner,
                (d.get('studios', {}).get('nodes', []) or [{}])[0].get('name', 'Unknown'),
            )
            
            cursor = conn.execute(query, values)
            return cursor.lastrowid  # Returns the ID of the title
        
    def get_all_titles(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute('SELECT * FROM library')
            return [dict(row) for row in cursor.fetchall()]
        
    def remove_title_by_id(self, anilist_id):
        query = "DELETE FROM library WHERE anilist_id = ?"
        with sqlite3.connect(self.db_path) as conn:
            c = conn.execute(query, (anilist_id,))
            return c.rowcount > 0
            
            
