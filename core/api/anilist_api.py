import time
import webbrowser
import requests
import keyring

CLIENT_ID = 38975
MEDIA_FIELDS_FRAGMENT = '''
fragment mediaFields on Media {
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
'''

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
                        ...mediaFields
                    }
                }
            }
        ''' + MEDIA_FIELDS_FRAGMENT

        self.single_title_query_string = '''
            query ($id: Int, $isMain: Boolean) {
                Media (id: $id, type: ANIME) {
                    ...mediaFields
                }
            }
        ''' + MEDIA_FIELDS_FRAGMENT
        
        self.media_list_collection_query = '''
            query ($userId: Int, $isMain: Boolean) {
                MediaListCollection(userId: $userId, type: ANIME) {
                    lists {
                        name
                        status
                        entries {
                            id
                            progress
                            score(format: POINT_10)
                            media {
                                ...mediaFields
                            }
                        }
                    }
                }
            }
        ''' + MEDIA_FIELDS_FRAGMENT

        self.viewer_info_query = """
            query {
                Viewer {
                    id
                    name
                    avatar { large }
                    bannerImage
                    siteUrl
                    createdAt
                    statistics {
                        anime { count }
                    }
                }
            }
        """

    def _post(self, query: str = '', variables: dict = None, headers: dict = None) -> dict:
        """Internal basic post function."""
        if variables is None:
            variables = {}

        while True:
            try:
                response = self.session.post(self.url, 
                json={'query': query, 'variables': variables},
                headers=headers
                )
                resp_headers = response.headers

                # 429
                if response.status_code == 429:
                    retry_after = int(resp_headers.get('Retry-After', 60))
                    print(f"[AniList API] 429 Rate Limit! Sleeping for {retry_after} sec...")
                    time.sleep(retry_after)
                    continue

                # 500, 502, 503, 504
                if response.status_code in [500, 502, 503, 504]:
                    print(f"[AniList API] {response.status_code} Server Error. Waiting for 15 sec...")
                    time.sleep(15)
                    continue

                if response.status_code == 200:
                    remaining = resp_headers.get('X-RateLimit-Remaining')
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

    def get_title(self, anilist_id: int | str) -> dict | None:
        """Gets one title by AniList ID."""
        variables = {
            'id': int(anilist_id),
            'isMain': True
        }
        res_json = self._post(self.single_title_query_string, variables)
        return res_json.get('data', {}).get('Media')
    
    def open_auth_url(self):
        webbrowser.open(f'https://anilist.co/api/v2/oauth/authorize?client_id={CLIENT_ID}&response_type=token')

    def save_token(self, token) -> dict | None:
        headers = {
            "Authorization": f"Bearer {token}",
            'User-Agent': 'NekoDesk (Python/Requests)',
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        res_json = self._post(self.viewer_info_query, headers=headers)

        if res_json:
            user_id = res_json.get('data', {}).get('Viewer', {}).get('id')
        else:
            user_id = ''

        if user_id and token:
            keyring.set_password('AniList_Token', str(user_id), token)
            return res_json
        else:
            return

    def get_user_media_list(self, user_id: int | str) -> dict | None:
        if user_id:
            token = keyring.get_password('AniList_Token', str(user_id))
        else:
            return
        
        headers = {
        'Authorization': f'Bearer {token}',
        'User-Agent': 'NekoDesk (Python/Requests)',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        }

        variables = {
            'userId': int(user_id),
            'isMain': True
        }

        res_json = self._post(self.media_list_collection_query, variables=variables, headers=headers)
        
        return res_json if res_json else None