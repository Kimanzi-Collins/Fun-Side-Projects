import requests

class APIHandler:
    def __init__(self, tmdb_key="", rawg_key=""):
        self.tmdb_key = tmdb_key
        self.rawg_key = rawg_key

    def get_anime(self, page=1):
        """
        Fetches Top Anime from Jikan API.
        No API Key required!
        """
        print(f"Fetching anime page {page}...")
        url = f"https://api.jikan.moe/v4/top/anime?page={page}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()['data']
            results = []
            for d in data:
                # We need items with images
                if d.get('images'):
                    results.append({
                        "title": d.get('title_english') or d.get('title'),
                        "image": d['images']['jpg']['large_image_url'],
                        "desc": d.get('synopsis', 'No description available.'),
                        "type": "Anime"
                    })
            return results
        print("Failed to fetch anime.")
        return []

    def get_movies(self, page=1):
        """
        Fetches Popular Movies from TMDB.
        Requires TMDB API Key.
        """
        if not self.tmdb_key or self.tmdb_key == "YOUR_TMDB_API_KEY": 
            return []
            
        print(f"Fetching movies page {page}...")
        url = f"https://api.themoviedb.org/3/movie/popular?api_key={self.tmdb_key}&language=en-US&page={page}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()['results']
            results = []
            for d in data:
                if d.get('poster_path'):
                    results.append({
                        "title": d['title'],
                        "image": f"https://image.tmdb.org/t/p/w500{d['poster_path']}",
                        "desc": d.get('overview', ''),
                        "type": "Movie"
                    })
            return results
        print("Failed to fetch movies.")
        return []

    def get_games(self, page=1):
        """
        Fetches Popular Games from RAWG.
        Requires RAWG API Key.
        """
        if not self.rawg_key or self.rawg_key == "YOUR_RAWG_API_KEY": 
            return []
            
        print(f"Fetching games page {page}...")
        url = f"https://api.rawg.io/api/games?key={self.rawg_key}&page={page}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()['results']
            results = []
            for d in data:
                if d.get('background_image'):
                    results.append({
                        "title": d['name'],
                        "image": d['background_image'],
                        "desc": f"Rating: {d.get('rating', 'N/A')}/5\nReleased: {d.get('released', 'Unknown')}",
                        "type": "Game"
                    })
            return results
        print("Failed to fetch games.")
        return []
