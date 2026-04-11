import sqlite3



def create_api_key_table():
    db = sqlite3.connect('data/settings.db')
    c = db.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS api_keys (
            service TEXT PRIMARY KEY,
            key TEXT
        )
    ''')
    db.commit()
    db.close()

def save_api_key(service, api_key):
    create_api_key_table()
    db = sqlite3.connect('data/settings.db')
    c = db.cursor()

    query = "INSERT OR REPLACE INTO api_keys (service, key) VALUES (?, ?)"
    
    c.execute(query, (service, api_key))
    db.commit()
    db.close()



def get_api_key(service):
    db = sqlite3.connect('data/settings.db')
    c = db.cursor()
    
    query = "SELECT key FROM api_keys WHERE service = ?"
    c.execute(query, (service,))
    
    result = c.fetchone()
    db.close()

    return result[0] if result else None

