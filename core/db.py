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
                    tvdb_id TEXT,
                    tmdb_id TEXT,
                    anilist_id TEXT,
                    mal_id TEXT,
                    type TEXT,          -- Movie, Series, OVA, etc.
                    titles TEXT,        -- JSON: {"en": "...", "ru": "...", "jp": "..."}
                    descriptions TEXT,  -- JSON: {"en": "...", "ru": "...", "jp": "..."}
                    year INTEGER,
                    status TEXT,
                    score INTEGER,
                    seasons INTEGER,
                    avg_runtime INTEGER,
                    genres TEXT,        -- Store as comma-separated or JSON
                    source TEXT,        -- Manga, Light Novel, Original
                    original_country TEXT,
                    original_language TEXT,
                    has_local_path BOOLEAN DEFAULT 0,
                    local_path TEXT,
                    poster_link TEXT,
                    poster_path TEXT
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS episodes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    series_id INTEGER,
                    season_number INTEGER,
                    episode_number INTEGER,
                    titles TEXT,    -- JSON: {"en": "...", "ru": "...", "jp": "..."}
                    descriptions TEXT,  -- JSON: {"en": "...", "ru": "...", "jp": "..."}
                    air_date TEXT,
                    runtime INTEGER,
                    FOREIGN KEY (series_id) REFERENCES library (id) ON DELETE CASCADE
                )
            ''')
    
    def add_series(self, title_data):
        """
        Saves metadata to the library table.
        title_data: A dictionary containing all the info from API.
        """
        title_data = title_data.get("data")
        with sqlite3.connect(self.db_path) as conn:
            query = '''
                INSERT INTO library (
                    tvdb_id) VALUES (?)
            '''
            
            values = (
                title_data.get('id'),
            )
            
            cursor = conn.execute(query, values)
            return cursor.lastrowid  # Returns the ID of the title
        