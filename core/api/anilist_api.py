import requests

class AniListClient:
    def __init__(self):
        self.url = 'https://graphql.anilist.co'
        self.query = '''
        query ($id: Int, $search: String, $isMain: Boolean) {
            Page (page: 1, perPage: 5) {
                pageInfo {
                total
                hasNextPage
                }
                media (id: $id, search: $search, type: ANIME) {
                title {
                    romaji
                    english
                    native
                }
                description
                type
                id
                idMal
                format
                status
                countryOfOrigin
                season
                seasonYear
                episodes
                duration
                genres
                synonyms
                averageScore
                isAdult
                coverImage {
                    color
                    medium
                    extraLarge
                }
                bannerImage
                studios(isMain: $isMain) {
                    nodes {
                        name
                    }
                }
                externalLinks {
                    site
                    url
                }
                }
            }
            }
        '''

    def search_title(self, search_query: str):
        variables = {'search': search_query, "isMain": True}
        
        try:
            response = requests.post(self.url, json={'query': self.query, 'variables': variables})
            if response.status_code == 200:
                res_json = response.json()
                page_data = res_json.get('data', {}).get('Page', {})
                media_list = page_data.get('media', [])
                
                return media_list 
            else:
                print(f"Ошибка API: {response.status_code}")
                return None
        except Exception as e:
            print(f"Ошибка запроса: {e}")
            return None
        
    def get_title(self, anilist_id: int):
        query = self.query 
        
        variables = {
            'id': anilist_id,
            'isMain': True
        }
        
        response = requests.post(self.url, json={'query': query, 'variables': variables})
        
        try:
            response = requests.post(self.url, json={'query': self.query, 'variables': variables})
            if response.status_code == 200:
                res_json = response.json()
                page_data = res_json.get('data', {}).get('Page', {})
                media_list = page_data.get('media', [])
                
                return media_list
            else:
                print(f"Ошибка API: {response.status_code}")
                return None
        except Exception as e:
            print(f"Ошибка запроса: {e}")
            return None