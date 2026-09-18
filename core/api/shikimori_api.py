import time
import webbrowser
import requests
import keyring

CLIENT_ID = 2121

ANIME_FIELDS_FRAGMENT = '''
fragment animeFields on Anime {
    id
    malId
    name
    english
    japanese
    russian
    licenseNameRu
    descriptionHtml
    kind
    status
    origin
    season
    releasedOn { year month day date }
    episodes
    duration
    genres { name russian kind }
    synonyms
    score
    rating
    isCensored
    poster { originalUrl mainUrl }
    studios { name }
    externalLinks { kind url }
    related {
        anime {
            id
            malId
            name
            english
            japanese
            russian
            licenseNameRu
            kind
        }
    }
}
'''

class ShikimoriClient:
    def __init__(self):
        self.url = 'https://shikimori.io/api/graphql'
        self.session = requests.Session()

        self.session.headers.update({
            'User-Agent': 'NekoDesk (Python/Requests)',
            'Content-Type': 'application/json'
        })
        
        self.search_query_string = '''
            query ($search: String, $page: Int, $limit: Int) {
                animes(search: $search, page: $page, limit: $limit) {
                    ...animeFields
                }
            }
        ''' + ANIME_FIELDS_FRAGMENT

        self.single_title_query_string = '''
            query ($ids: String) {
                animes(ids: $ids) {
                    ...animeFields
                }
            }
        ''' + ANIME_FIELDS_FRAGMENT
        

        self.media_list_collection_query = '''
            query($userId: ID, $page: Int, $limit: Int) {
                userRates(
                    userId: $userId
                    page: $page
                    limit: $limit
                    targetType: Anime
                ) 
                {
                    id
                    createdAt
                    status
                    anime {
                        ...animeFields
                    }
                }
            }
        ''' + ANIME_FIELDS_FRAGMENT

        self.viewer_info_query = """
            query($username: String) {
                users(search: $username) {
                    id
                    avatarUrl
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
                    print(f"[Shikimori API] 429 Rate Limit! Sleeping for {retry_after} sec...")
                    time.sleep(retry_after)
                    continue

                # 500, 502, 503, 504
                if response.status_code in [500, 502, 503, 504]:
                    print(f"[Shikimori API] {response.status_code} Server Error. Waiting for 15 sec...")
                    time.sleep(15)
                    continue

                if response.status_code == 200:
                    remaining = resp_headers.get('X-RateLimit-Remaining')
                    if remaining is not None and int(remaining) < 8:
                        print(f"[Shikimori API] Close to limit ({remaining}). Slowing down...")
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
            'limit': per_page
        }
        res_json = self._post(self.search_query_string, variables)
        return res_json.get('data', {}).get('animes', res_json)

    def get_title(self, shikimori_id: int | str) -> dict | None:
        """Gets one title by Shikimori ID."""
        variables = {
            'ids': str(shikimori_id)
        }
        res_json = self._post(self.single_title_query_string, variables)
        return res_json.get('data', {}).get('animes', res_json)
    
    def get_user_media_list(self, user_id: int | str) -> dict | None:
        if not user_id:
            return None

        page = 1
        limit = 50
        all_user_rates = []
        seen_ids = set()
        base_response = None

        while True:
            variables = {
                'userId': int(user_id),
                'page': page,
                'limit': limit
            }

            res_json = self._post(self.media_list_collection_query, variables)
            
            if not res_json or 'data' not in res_json:
                break

            user_rates = res_json.get('data', {}).get('userRates', [])
            if not user_rates:
                break

            # Duplicate check
            first_id = user_rates[0].get('id') if isinstance(user_rates[0], dict) else None
            if first_id in seen_ids:
                print('[Shikimori API] Duplication found')
                break
            
            for rate in user_rates:
                if isinstance(rate, dict) and 'id' in rate:
                    seen_ids.add(rate['id'])

            if base_response is None:
                base_response = res_json

            all_user_rates.extend(user_rates)

            if len(user_rates) < limit:
                break

            page += 1

        if base_response:
            base_response['data']['userRates'] = all_user_rates
            return base_response

        return None
    
    def get_user_data(self, username: str) -> dict:
        if not username:
            return

        variables = {
            'username': str(username)
        }

        res_json = self._post(self.viewer_info_query, variables)
        return res_json.get('data', {}).get('users', [])[0] if res_json else {}