import requests

from core.db import SettingsDB

class TVDBClient:
    def __init__(self, api_key):
        """
        Initialize the client with the user's API key
        """
        self.api_key = api_key
        self.base_url = "https://api4.thetvdb.com/v4"
        self.token = None # Temporary Bearer token

    def authenticate(self):
        """
        Exchange API Key for a temporary Bearer Token
        """
        url = f"{self.base_url}/login"
        payload = {"apikey": self.api_key}
        
        try:
            # POST request to get the session token
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                self.token = response.json().get('data', {}).get('token')
                return True
            return False
        except Exception as e:
            print(f"Auth error: {e}")
            return False

    def search(self, query: str) -> dict | None:
        """
        Search for a series/anime by its title
        """
        if not self.token:
            return None
            
        url = f"{self.base_url}/search"
        headers = {"Authorization": f"Bearer {self.token}"}
        params = {"q": query, "type": "series"}
        
        response = requests.get(url, headers=headers, params=params)
        return response.json() if response.status_code == 200 else None

    def series(self, tvdb_id: str) -> dict | None:
        """
        Get series data
        """
        if not self.token:
            return None
            
        url = f"{self.base_url}/series/{tvdb_id}"
        headers = {"Authorization": f"Bearer {self.token}"}
        params = {}
        
        response = requests.get(url, headers=headers, params=params)
        return response.json() if response.status_code == 200 else None
    
    def ext_series(self, tvdb_id: str) -> dict | None:
        """
        Get extended series data
        """
        if not self.token:
            return None
            
        url = f"{self.base_url}/series/{tvdb_id}/extended"
        headers = {"Authorization": f"Bearer {self.token}"}
        params = {}
        
        response = requests.get(url, headers=headers, params=params)
        return response.json() if response.status_code == 200 else None