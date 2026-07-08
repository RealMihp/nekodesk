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
    def __init__(self, db_path='data/local_library.db'):
        self.db_path = db_path
        self._create_tables()
        self.imgmClient = ImageManager()
    
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
                    season_num INTEGER,
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
            
    
    def add_title(self, title: list, title_id: int | str) -> int | None:
        """
        Saves metadata to the library table.
        title: Title info from API.
        title_id: Title ID to be added.
        client: API client.
        """
        d = None


        if str(title.get('id', '')) == str(title_id):
            d = title
        elif str(title.get('media', {}).get('id', '')) == str(title_id):
            d = title.get('media', {})
        
        if not d:
            return

        with sqlite3.connect(self.db_path) as conn:
            query = '''
                INSERT OR REPLACE INTO library (anilist_id, mal_id, title_romaji, title_english, title_native, desc, format, status, origin_country,season_num, season,
                season_year, episodes, duration, genres, synonyms, score, is_adult, poster_color, poster_small_link, poster_large_link, poster_small_path, poster_large_path,
                banner_link, banner_path, studio
                ) VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
            
            medium = d.get('coverImage', {}).get('medium')
            extraLarge = d.get('coverImage', {}).get('extraLarge')
            banner = d.get('bannerImage')
            links = [medium, extraLarge, banner]

            #paths = self.imgmClient.get_posters(links)
            # path_small = paths.get(medium, (None, None))[1]
            # path_extraLarge = paths.get(extraLarge, (None, None))[1]
            # path_banner = paths.get(banner, (None, None))[1]
            path_small = None
            path_extraLarge = None
            path_banner = None
            
            #season_num = self.get_season_num(d, client)
            season_num = None
            
            values = (
                d.get('id'),
                d.get('idMal'),
                d.get('title', {}).get('romaji'),
                d.get('title', {}).get('english'),
                d.get('title', {}).get('native'),
                d.get('description'),
                d.get('format'),
                d.get('status').capitalize() if d.get('status') else None,
                d.get('countryOfOrigin'),
                season_num,
                d.get('season').capitalize() if d.get('season') else None,
                d.get('seasonYear'),
                d.get('episodes'),
                d.get('duration'),
                ', '.join(d.get('genres') or []),
                ', '.join(d.get('synonyms') or []),
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
        
    def get_season_num(self, d: dict = {}, client = None) -> int:

        format = d.get('format')
        season_num = 1 if format in ('TV', 'TV_SHORT', 'MOVIE') else 0
        
        sequels = set()
        prequels = set()

        session = client.session

        relations_data = d.get('relations', {})
        if isinstance(relations_data, dict):
            relations = relations_data.get('edges', [])
        else:
            relations = []

        relations_set = set()
        if relations:
            for relation in relations:
                relationType = relation.get('relationType') 
                relation_node = relation.get('node', {})
                relation_id = relation_node.get('id')
                relation_type = relation_node.get('type')
                relation_format = relation_node.get('format')

                if relationType:
                    relations_set.add(relationType)
                    if relation_type == 'ANIME' and relation_id:
                        if relationType == 'SEQUEL':
                            sequels.add(relation_id)
                        elif relationType == 'PREQUEL':
                            prequels.add(relation_id)
        
        if prequels:
            # Turn into a list so that we can go through it and change it as we go
            prequels_list = list(prequels)
            
            for prequel_id in prequels_list:
                result = client.get_title(prequel_id)
                if result:
                    p_format = result.get('format')
                    if p_format in ('TV', 'TV_SHORT'):
                        season_num += 1
                    
                    relations_data = result.get('relations', {})
                    if isinstance(relations_data, dict):
                        p_relations = relations_data.get('edges', [])
                    else:
                        p_relations = []

                    if p_relations:
                        for p_rel in p_relations:
                            p_type = p_rel.get('relationType')
                            p_node = p_rel.get('node', {})
                            
                            if p_type == 'PREQUEL' and p_node.get('type') == 'ANIME':
                                next_id = p_node.get('id')
                                if next_id and next_id not in prequels_list:
                                    prequels_list.append(next_id)

        return season_num
        
    def get_all_titles(self) -> dict | None:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute('SELECT * FROM library')
            return [dict(row) for row in cursor.fetchall()]
    
    def get_title(self, anilist_id: str) -> dict | None:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            query = 'SELECT * FROM library WHERE anilist_id = ?'
            c = conn.execute(query, (anilist_id,))
            row = c.fetchone()
            return dict(row) if row else None
        
    def remove_title_by_id(self, anilist_id: str):
        query = "DELETE FROM library WHERE anilist_id = ?"
        with sqlite3.connect(self.db_path) as conn:
            c = conn.execute(query, (anilist_id,))
            return c.rowcount > 0
        
    def copy_title(self, title_data: dict) -> int | None:
        data_copy = title_data.copy()
        
        if 'id' in data_copy:
            del data_copy['id']
            
        columns = ', '.join(data_copy.keys())
        placeholders = ', '.join(['?'] * len(data_copy))
        
        sql = f"REPLACE INTO library ({columns}) VALUES ({placeholders})"
        
        conn = sqlite3.connect(self.db_path)
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute(sql, tuple(data_copy.values()))
                row_id = cursor.lastrowid
            return row_id
        finally:
            conn.close()
            
