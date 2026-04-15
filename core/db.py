import sqlite3
import os
import json

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
    
    def _create_tables(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS library (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    anilist_id TEXT UNIQUE,
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
        title_data: A dictionary containing all the info from API.
        """
        title_data = title_data[0]
        d = title_data

        with sqlite3.connect(self.db_path) as conn:
            query = '''
                INSERT OR REPLACE INTO library (anilist_id, mal_id, title_romaji, title_english, title_native, desc, format, status, origin_country, season,
                season_year, episodes, duration, genres, synonyms, score, is_adult, poster_color, poster_small_link, poster_large_link, poster_small_path, poster_large_path,
                banner_link, banner_path, studio
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
            
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
                d.get('coverImage', {}).get('medium'),
                d.get('coverImage', {}).get('extraLarge'),
                None,
                None,
                d.get('bannerImage'),
                None,
                d.get('studios', {}).get('nodes', {})[0].get('name'),
            )
            
            cursor = conn.execute(query, values)
            return cursor.lastrowid  # Returns the ID of the title
        