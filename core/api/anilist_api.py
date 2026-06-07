import time
import requests

class AniListClient:
    def __init__(self):
        self.url = 'https://graphql.anilist.co'
        self.session = requests.Session()
        self.search_query_string = '''
            query ($search: String, $page: Int, $perPage: Int, $isMain: Boolean) {
                Page (page: $page, perPage: $perPage) {
                    pageInfo {
                    total
                    hasNextPage
                    }
                    media (search: $search, type: ANIME) {
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
                    relations {
                        edges {
                        relationType
                        node {
                            id
                            idMal
                            title {
                            romaji
                            native
                            english
                            }
                            type
                            format
                        }
                        }
                    }
                    }
                }
                }
            '''
        self.single_title_query_string = '''
            query ($id: Int, $isMain: Boolean) {
                Media (id: $id, type: ANIME) {
                    id 
                    idMal 
                    title { 
                        romaji 
                        english 
                        native 
                    }
                    description 
                    type 
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
                    bannerImage
                    coverImage { 
                        color 
                        medium 
                        extraLarge 
                    }
                    studios(isMain: $isMain) {
                        nodes {
                            name
                        }
                    }
                    externalLinks { 
                        site 
                        url 
                    }
                    relations {
                        edges {
                        relationType
                        node {
                            id
                            idMal
                            title {
                            romaji
                            native
                            english
                            }
                            type
                            format
                        }
                        }
                    }
                }
            }
            '''

    def _post(self, query: str, variables: dict) -> dict:
        """Internal basic post function."""
        while True:
            try:
                response = self.session.post(self.url, json={'query': query, 'variables': variables})
                headers = response.headers

                # 429
                if response.status_code == 429:
                    retry_after = int(headers.get('Retry-After', 60))
                    print(f"[AniList API] 429 Rate Limit! Sleeping for {retry_after} sec...")
                    time.sleep(retry_after)
                    continue

                # 500, 502, 503, 504
                if response.status_code in [500, 502, 503, 504]:
                    print(f"[AniList API] {response.status_code} Server Error. Waiting for 15 sec...")
                    time.sleep(15)
                    continue

                if response.status_code == 200:
                    remaining = headers.get('X-RateLimit-Remaining')
                    if remaining is not None and int(remaining) < 8:
                        print(f"[AniList API] Close to limit ({remaining}). Slowing down...")
                        time.sleep(2)
                        
                    return response.json()
                
                print(f"API error: {response.status_code}")
                response.raise_for_status()

            except Exception as e:
                print(f"Network error: {e}")
                raise e

    def search_title(self, search_query: str, page: int = 1, per_page: int = 15) -> list:
        """Searches for titles by query."""
        variables = {
            'search': search_query,
            'page': page,
            'perPage': per_page,
            'isMain': True
        }
        res_json = self._post(self.search_query_string, variables)
        return res_json.get('data', {}).get('Page', {}).get('media', [])

    def get_title(self, anilist_id: int) -> dict | None:
        """Gets one title by AniList ID."""
        variables = {
            'id': anilist_id,
            'isMain': True
        }
        res_json = self._post(self.single_title_query_string, variables)
        return res_json.get('data', {}).get('Media')