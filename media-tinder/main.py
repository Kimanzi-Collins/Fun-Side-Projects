import customtkinter as ctk
from PIL import Image
import requests
import io
import threading
import random
from api_handlers import APIHandler

# --- CONFIGURATION ---
# Get your keys here:
# TMDB: https://www.themoviedb.org/settings/api (For Movies/Series)
# RAWG: https://rawg.io/apidocs (For Games)
# Note: Anime works out of the box without an API key!
TMDB_API_KEY = "YOUR_TMDB_API_KEY"
RAWG_API_KEY = "YOUR_RAWG_API_KEY"
# ---------------------

class MediaTinderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Setup main window
        self.title("Media Matcher - Swipe your favorites!")
        self.geometry("400x700")
        ctk.set_appearance_mode("dark") # Modern dark mode out of the box
        
        # Initialize our backend API
        self.api = APIHandler(TMDB_API_KEY, RAWG_API_KEY)
        self.media_queue = []
        self.current_item = None
        self.liked_items = []
        
        # Build the UI
        self.setup_ui()
        
        # Start fetching data
        self.fetch_initial_data()

    def setup_ui(self):
        """Builds the visual elements of our app."""
        # 1. Main Title
        self.title_label = ctk.CTkLabel(self, text="Media Matcher 🍿", font=("Helvetica", 28, "bold"))
        self.title_label.pack(pady=(20, 10))
        
        # 2. The "Card" (This holds our media item)
        # We use a frame with rounded corners to look like a modern card
        self.card_frame = ctk.CTkFrame(self, width=340, height=500, corner_radius=20)
        self.card_frame.pack(pady=10, padx=20, fill="both", expand=True)
        self.card_frame.pack_propagate(False) # Prevent frame from shrinking to its contents
        
        # 3. Inside the Card: Image
        self.image_label = ctk.CTkLabel(self.card_frame, text="Fetching cool stuff for you...", font=("Helvetica", 14))
        self.image_label.pack(pady=20)
        
        # 4. Inside the Card: Title and Type
        self.info_title = ctk.CTkLabel(self.card_frame, text="", font=("Helvetica", 20, "bold"), wraplength=300)
        self.info_title.pack(pady=(10, 0))
        
        self.info_type = ctk.CTkLabel(self.card_frame, text="", font=("Helvetica", 14), text_color="gray")
        self.info_type.pack()
        
        # 5. The Buttons Frame (bottom row)
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=20)
        
        # Swipe Left / Swipe Right buttons
        self.btn_nah = ctk.CTkButton(
            self.btn_frame, 
            text="Nah ❌", 
            fg_color="#ef4444", 
            hover_color="#dc2626", 
            width=130, height=50, 
            corner_radius=25,
            font=("Helvetica", 18, "bold"), 
            command=self.swipe_left
        )
        self.btn_nah.pack(side="left", padx=15)
        
        self.btn_yeah = ctk.CTkButton(
            self.btn_frame, 
            text="Yeah ❤️", 
            fg_color="#10b981", 
            hover_color="#059669", 
            width=130, height=50, 
            corner_radius=25,
            font=("Helvetica", 18, "bold"), 
            command=self.swipe_right
        )
        self.btn_yeah.pack(side="right", padx=15)

    def fetch_initial_data(self):
        """Fetches data from APIs in the background so the UI doesn't freeze."""
        threading.Thread(target=self._fetch_data_thread, daemon=True).start()
        
    def _fetch_data_thread(self):
        # 1. Fetch Anime (always works, no key needed)
        anime = self.api.get_anime()
        self.media_queue.extend(anime)
        
        # 2. Fetch Movies (if key is provided)
        movies = self.api.get_movies()
        self.media_queue.extend(movies)
            
        # 3. Fetch Games (if key is provided)
        games = self.api.get_games()
        self.media_queue.extend(games)
            
        # Shuffle the list so you get a random mix of Anime/Movies/Games
        random.shuffle(self.media_queue)
        
        # Back to the main UI thread to update the screen
        self.after(0, self.show_next_item)

    def load_image_from_url(self, url):
        """Downloads an image from a URL and converts it for Tkinter."""
        try:
            response = requests.get(url)
            image_data = Image.open(io.BytesIO(response.content))
            
            # Resize image to fit nicely on our card
            image_data = image_data.resize((280, 380), Image.Resampling.LANCZOS)
            
            # CTkImage handles high-DPI scaling automatically
            photo = ctk.CTkImage(light_image=image_data, dark_image=image_data, size=(280, 380))
            return photo
        except Exception as e:
            print("Error loading image:", e)
            return None

    def show_next_item(self):
        """Updates the card with the next media item in the queue."""
        if not self.media_queue:
            self.image_label.configure(image=None, text="Out of recommendations!\nFetch more or add API keys.")
            self.info_title.configure(text="")
            self.info_type.configure(text="")
            return
            
        self.current_item = self.media_queue.pop(0)
        
        # Update text immediately
        self.info_title.configure(text=self.current_item['title'])
        self.info_type.configure(text=self.current_item['type'])
        self.image_label.configure(text="Loading Image...", image=None)
        
        # Load the image in the background (images take time to download)
        threading.Thread(target=self._load_image_thread, args=(self.current_item['image'],), daemon=True).start()
        
    def _load_image_thread(self, url):
        img = self.load_image_from_url(url)
        if img:
            # Update the image on the main UI thread
            self.after(0, lambda: self.image_label.configure(image=img, text=""))
        else:
            self.after(0, lambda: self.image_label.configure(text="No Image Available"))

    def swipe_left(self):
        """Handles the 'Nah' button click."""
        print(f"Skipped: {self.current_item['title']}")
        self.show_next_item()
        
    def swipe_right(self):
        """Handles the 'Yeah' button click."""
        print(f"Liked: {self.current_item['title']}")
        self.liked_items.append(self.current_item)
        self.show_next_item()

if __name__ == "__main__":
    app = MediaTinderApp()
    app.mainloop()
