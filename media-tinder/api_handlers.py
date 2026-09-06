import requests

# ─── DEMO PLACEHOLDER IMAGE GENERATOR ────────────────────────────────────────
# Generates colourful PIL images locally — zero network dependency for demo mode.

from PIL import Image, ImageDraw

_TYPE_COLORS = {
    "Anime": ((80, 20, 120), (30, 5,  50)),   # purple gradient
    "Movie": ((15, 50, 120), (5,  15, 50)),    # blue gradient
    "Game":  ((10, 90, 40),  (3,  30, 15)),    # green gradient
}

def _make_placeholder(title: str, media_type: str, w: int = 360, h: int = 500) -> Image.Image:
    """Return a gradient PIL Image with the title and type printed on it."""
    top_col, bot_col = _TYPE_COLORS.get(media_type, ((40, 40, 40), (10, 10, 10)))
    img = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(img)

    # vertical gradient
    for y in range(h):
        t = y / h
        r = int(top_col[0] + (bot_col[0] - top_col[0]) * t)
        g = int(top_col[1] + (bot_col[1] - top_col[1]) * t)
        b = int(top_col[2] + (bot_col[2] - top_col[2]) * t)
        draw.line([(0, y), (w, y)], fill=(r, g, b))

    # subtle grid lines for depth
    for x in range(0, w, 40):
        draw.line([(x, 0), (x, h)], fill=(255, 255, 255, 15))
    for y in range(0, h, 40):
        draw.line([(0, y), (w, y)], fill=(255, 255, 255, 15))

    # type label (top-left)
    draw.rectangle([20, 20, 100, 42], fill=top_col)
    draw.text((24, 23), media_type.upper(), fill=(220, 220, 255))

    # title (centered, wrapped manually)
    words  = title.split()
    lines, cur = [], ""
    for word in words:
        test = (cur + " " + word).strip()
        if len(test) > 22:
            lines.append(cur)
            cur = word
        else:
            cur = test
    if cur:
        lines.append(cur)

    line_h = 28
    total  = len(lines) * line_h
    y0     = (h - total) // 2 - 10
    for i, line in enumerate(lines):
        x0 = (w - len(line) * 13) // 2      # rough centering
        draw.text((x0, y0 + i * line_h), line, fill=(240, 240, 255))

    # bottom divider hint
    draw.rectangle([0, h - 160, w, h - 159], fill=(255, 255, 255, 30))

    return img

DEMO_DATA = {
    "anime": [
        {
            "title": "Fullmetal Alchemist: Brotherhood",
            "image": None,
            "desc": (
                "Two brothers search for a Philosopher's Stone after an attempt "
                "to revive their deceased mother goes wrong, leaving them in "
                "broken bodies. A sweeping story of sacrifice, loss, and the cost "
                "of playing god."
            ),
            "type": "Anime",
            "rating": "9.1",
        },
        {
            "title": "Attack on Titan",
            "image": None,
            "desc": (
                "In a world where humanity lives inside cities surrounded by "
                "enormous walls due to the Titans, gigantic humanoid creatures "
                "who devour humans seemingly without reason, one boy vows revenge "
                "after his mother is eaten."
            ),
            "type": "Anime",
            "rating": "9.0",
        },
        {
            "title": "Death Note",
            "image": None,
            "desc": (
                "A high school student discovers a supernatural notebook that "
                "grants its user the ability to kill anyone whose name and face "
                "they know. He decides to use it to cleanse the world of criminals."
            ),
            "type": "Anime",
            "rating": "8.6",
        },
        {
            "title": "Demon Slayer",
            "image": None,
            "desc": (
                "A young boy becomes a demon slayer after his family is slaughtered "
                "and his younger sister is turned into a demon. A visually stunning "
                "journey of brotherhood, grief, and breathtaking battles."
            ),
            "type": "Anime",
            "rating": "8.7",
        },
        {
            "title": "Steins;Gate",
            "image": None,
            "desc": (
                "A self-proclaimed mad scientist accidentally discovers time travel "
                "via a microwave and must navigate the consequences of altering the "
                "past. A slow-burn thriller that becomes one of the most emotional "
                "anime ever made."
            ),
            "type": "Anime",
            "rating": "8.8",
        },
        {
            "title": "Hunter x Hunter",
            "image": None,
            "desc": (
                "Gon Freecss dreams of becoming a Hunter like his absent father. "
                "After passing a brutal exam, he enters a world of danger, friendship, "
                "and dark ambition. Features one of the most complex power systems "
                "in anime."
            ),
            "type": "Anime",
            "rating": "9.0",
        },
        {
            "title": "One Punch Man",
            "image": None,
            "desc": (
                "Saitama is a superhero who can defeat any enemy with a single punch, "
                "but this immense power has left him bored. A brilliant satire of the "
                "superhero genre wrapped in stunning action sequences."
            ),
            "type": "Anime",
            "rating": "8.5",
        },
        {
            "title": "Neon Genesis Evangelion",
            "image": None,
            "desc": (
                "Teenager Shinji Ikari is recruited by his father to pilot a giant "
                "biomechanical mecha called Evangelion to fight monstrous beings "
                "called Angels. A landmark in psychological anime storytelling."
            ),
            "type": "Anime",
            "rating": "8.5",
        },
        {
            "title": "Vinland Saga",
            "image": None,
            "desc": (
                "Set in medieval Europe, young Thorfinn joins a band of mercenaries "
                "and seeks revenge against the man who killed his father. An epic "
                "Viking saga about war, vengeance, and ultimately, peace."
            ),
            "type": "Anime",
            "rating": "8.8",
        },
        {
            "title": "Jujutsu Kaisen",
            "image": None,
            "desc": (
                "A boy swallows a cursed talisman and joins a secret organization "
                "of Jujutsu Sorcerers to fight powerful Curses. Fast-paced, "
                "stylish, and emotionally heavy — modern shonen at its best."
            ),
            "type": "Anime",
            "rating": "8.6",
        },
    ],
    "movies": [
        {
            "title": "Interstellar",
            "image": None,
            "desc": (
                "A team of explorers travel through a wormhole in space in an "
                "attempt to ensure humanity's survival. Christopher Nolan's "
                "breathtaking sci-fi epic about love, time, and the cosmos."
            ),
            "type": "Movie",
            "rating": "8.6",
        },
        {
            "title": "The Dark Knight",
            "image": None,
            "desc": (
                "Batman raises the stakes in his war on crime. With the help of "
                "Lt. Jim Gordon and District Attorney Harvey Dent, he sets out to "
                "dismantle the remaining criminal organizations in Gotham. But a "
                "new menace, the Joker, arises."
            ),
            "type": "Movie",
            "rating": "9.0",
        },
        {
            "title": "Inception",
            "image": None,
            "desc": (
                "A thief who steals corporate secrets through the use of "
                "dream-sharing technology is given the inverse task of planting "
                "an idea into the mind of a CEO. Nolan's mind-bending masterpiece."
            ),
            "type": "Movie",
            "rating": "8.8",
        },
        {
            "title": "Parasite",
            "image": None,
            "desc": (
                "Greed and class discrimination threaten the newly formed symbiotic "
                "relationship between the wealthy Park family and the destitute Kim "
                "clan. Bong Joon-ho's Oscar-winning dark masterpiece."
            ),
            "type": "Movie",
            "rating": "8.5",
        },
        {
            "title": "Dune: Part One",
            "image": None,
            "desc": (
                "Paul Atreides, a brilliant and gifted young man born into a great "
                "destiny, must travel to the most dangerous planet in the universe "
                "to ensure the future of his family and his people."
            ),
            "type": "Movie",
            "rating": "8.0",
        },
        {
            "title": "Everything Everywhere All at Once",
            "image": None,
            "desc": (
                "An aging Chinese immigrant is swept up in an insane adventure where "
                "she alone can save existence by exploring other universes and "
                "connecting with the lives she could have led."
            ),
            "type": "Movie",
            "rating": "7.8",
        },
        {
            "title": "The Shawshank Redemption",
            "image": None,
            "desc": (
                "Two imprisoned men bond over a number of years, finding solace "
                "and eventual redemption through acts of common decency. Widely "
                "regarded as one of the greatest films ever made."
            ),
            "type": "Movie",
            "rating": "9.3",
        },
        {
            "title": "Blade Runner 2049",
            "image": None,
            "desc": (
                "A young blade runner's discovery of a long-buried secret leads "
                "him to track down former blade runner Rick Deckard. A visually "
                "astonishing sequel that expands the philosophical depth of the original."
            ),
            "type": "Movie",
            "rating": "8.0",
        },
        {
            "title": "Mad Max: Fury Road",
            "image": None,
            "desc": (
                "In a post-apocalyptic wasteland, a woman rebels against a tyrannical "
                "ruler in search of her homeland with the aid of a group of female "
                "prisoners, a psychotic worshiper, and a drifter named Max."
            ),
            "type": "Movie",
            "rating": "8.1",
        },
        {
            "title": "Whiplash",
            "image": None,
            "desc": (
                "A promising young drummer enrolls at a cut-throat music conservatory "
                "where his dreams of greatness are mentored by an abusive instructor "
                "who will stop at nothing to realize a student's potential."
            ),
            "type": "Movie",
            "rating": "8.5",
        },
    ],
    "games": [
        {
            "title": "The Witcher 3: Wild Hunt",
            "image": None,
            "desc": (
                "As war rages on throughout the Northern Realms, you take on the "
                "role of a professional monster hunter and navigate a morally complex "
                "open world. Arguably the greatest RPG ever made."
            ),
            "type": "Game",
            "rating": "9.3",
        },
        {
            "title": "Red Dead Redemption 2",
            "image": None,
            "desc": (
                "America, 1899. Arthur Morgan and the Van der Linde gang are outlaws "
                "on the run. In a world that is closing in on them, Arthur must choose "
                "between his own ideals and loyalty to the gang who raised him."
            ),
            "type": "Game",
            "rating": "9.7",
        },
        {
            "title": "Elden Ring",
            "image": None,
            "desc": (
                "Rise, Tarnished, and be guided by grace to brandish the power of "
                "the Elden Ring and become an Elden Lord in the Lands Between. "
                "FromSoftware's most ambitious open-world challenge."
            ),
            "type": "Game",
            "rating": "9.5",
        },
        {
            "title": "The Last of Us Part I",
            "image": None,
            "desc": (
                "Joel, a hardened survivor, is hired to smuggle Ellie, a 14-year-old "
                "girl, out of an oppressive quarantine zone. What starts as a job "
                "becomes a brutal, heart-wrenching journey across a post-apocalyptic America."
            ),
            "type": "Game",
            "rating": "9.5",
        },
        {
            "title": "God of War (2018)",
            "image": None,
            "desc": (
                "Kratos, the Ghost of Sparta, must navigate the treacherous Norse "
                "realms with his son Atreus after the death of his wife. A stunning "
                "reinvention of a beloved franchise about fatherhood and legacy."
            ),
            "type": "Game",
            "rating": "9.3",
        },
        {
            "title": "Cyberpunk 2077",
            "image": None,
            "desc": (
                "In the megalopolis of Night City, you play as V — a mercenary "
                "outlaw going after a one-of-a-kind implant that is the key to "
                "immortality. An immersive open-world RPG with incredible writing."
            ),
            "type": "Game",
            "rating": "8.7",
        },
        {
            "title": "Hollow Knight",
            "image": None,
            "desc": (
                "A challenging 2D action-adventure through a vast ruined kingdom of "
                "insects and heroes. Explore twisting caverns, battle tainted "
                "creatures and befriend bizarre bugs — all created with hand-crafted "
                "detail."
            ),
            "type": "Game",
            "rating": "9.1",
        },
        {
            "title": "Hades",
            "image": None,
            "desc": (
                "Defy the god of the dead as you hack and slash your way out of the "
                "Underworld in this rogue-like dungeon crawler from the creators of "
                "Bastion and Transistor. Every run reveals more of the story."
            ),
            "type": "Game",
            "rating": "9.2",
        },
        {
            "title": "Disco Elysium",
            "image": None,
            "desc": (
                "You're a detective with a ruined reputation, piecing together your "
                "past while solving a murder in a decaying city. One of the most "
                "politically complex and wildly original RPGs ever written."
            ),
            "type": "Game",
            "rating": "9.0",
        },
        {
            "title": "Sekiro: Shadows Die Twice",
            "image": None,
            "desc": (
                "Carve your own clever path to vengeance in the brutal game of life "
                "and death of Sekiro. Set in the late 1500s Sengoku period Japan, "
                "take on the role of a hard-hearted shinobi seeking revenge."
            ),
            "type": "Game",
            "rating": "9.0",
        },
    ],
}


# ─── API HANDLER ─────────────────────────────────────────────────────────────
class APIHandler:
    def __init__(self, tmdb_key="", rawg_key=""):
        self.tmdb_key = tmdb_key
        self.rawg_key = rawg_key

    # ── helpers ──────────────────────────────────────────────────────────────
    def _is_demo(self):
        """Returns True when neither API key has been configured."""
        no_tmdb = not self.tmdb_key or self.tmdb_key == "YOUR_TMDB_API_KEY"
        no_rawg = not self.rawg_key or self.rawg_key == "YOUR_RAWG_API_KEY"
        return no_tmdb and no_rawg

    # ── public methods ───────────────────────────────────────────────────────
    def get_anime(self, page=1):
        """
        Fetches Top Anime from Jikan API (no key needed).
        Falls back to demo data if the request fails or demo mode is on.
        """
        # Anime doesn't need a key — only fall back if we're in full demo mode
        if self._is_demo():
            print("[DEMO] Returning demo anime data.")
            return list(DEMO_DATA["anime"])

        print(f"Fetching anime page {page}...")
        try:
            response = requests.get(
                f"https://api.jikan.moe/v4/top/anime?page={page}", timeout=8
            )
            if response.status_code == 200:
                results = []
                for d in response.json().get("data", []):
                    if d.get("images"):
                        results.append({
                            "title": d.get("title_english") or d.get("title"),
                            "image": d["images"]["jpg"]["large_image_url"],
                            "desc":  d.get("synopsis", "No description available."),
                            "type":  "Anime",
                            "rating": str(d.get("score", "")),
                        })
                return results
        except Exception as e:
            print(f"Anime fetch error: {e}")

        print("Falling back to demo anime data.")
        return list(DEMO_DATA["anime"])

    def get_movies(self, page=1):
        """
        Fetches Popular Movies from TMDB.
        Falls back to demo data if key is missing or request fails.
        """
        if not self.tmdb_key or self.tmdb_key == "YOUR_TMDB_API_KEY":
            print("[DEMO] No TMDB key — returning demo movie data.")
            return list(DEMO_DATA["movies"])

        print(f"Fetching movies page {page}...")
        try:
            url = (
                f"https://api.themoviedb.org/3/movie/popular"
                f"?api_key={self.tmdb_key}&language=en-US&page={page}"
            )
            response = requests.get(url, timeout=8)
            if response.status_code == 200:
                results = []
                for d in response.json().get("results", []):
                    if d.get("poster_path"):
                        results.append({
                            "title": d["title"],
                            "image": f"https://image.tmdb.org/t/p/w500{d['poster_path']}",
                            "desc":  d.get("overview", ""),
                            "type":  "Movie",
                            "rating": str(d.get("vote_average", "")),
                        })
                return results
        except Exception as e:
            print(f"Movies fetch error: {e}")

        print("Falling back to demo movie data.")
        return list(DEMO_DATA["movies"])

    def get_games(self, page=1):
        """
        Fetches Popular Games from RAWG.
        Falls back to demo data if key is missing or request fails.
        """
        if not self.rawg_key or self.rawg_key == "YOUR_RAWG_API_KEY":
            print("[DEMO] No RAWG key — returning demo game data.")
            return list(DEMO_DATA["games"])

        print(f"Fetching games page {page}...")
        try:
            url = f"https://api.rawg.io/api/games?key={self.rawg_key}&page={page}"
            response = requests.get(url, timeout=8)
            if response.status_code == 200:
                results = []
                for d in response.json().get("results", []):
                    if d.get("background_image"):
                        results.append({
                            "title": d["name"],
                            "image": d["background_image"],
                            "desc":  (
                                f"Rating: {d.get('rating', 'N/A')}/5  •  "
                                f"Released: {d.get('released', 'Unknown')}"
                            ),
                            "type":  "Game",
                            "rating": str(d.get("rating", "")),
                        })
                return results
        except Exception as e:
            print(f"Games fetch error: {e}")

        print("Falling back to demo game data.")
        return list(DEMO_DATA["games"])

