import customtkinter as ctk
from PIL import Image
import requests
import io
import threading
import random
from api_handlers import APIHandler

try:
    import pywinstyles
except ImportError:
    pywinstyles = None

# --- CONFIGURATION ---
TMDB_API_KEY = "YOUR_TMDB_API_KEY"
RAWG_API_KEY = "YOUR_RAWG_API_KEY"
# ---------------------

class MediaTinderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- APPLE LIQUID GLASS THEME ---
        self.title("Media Matcher")
        self.geometry("450x750")
        
        # Soft dark background for the glass effect
        self.configure(fg_color="#1a1a1a")
        
        # Make the window slightly translucent to blend with the desktop
        self.attributes("-alpha", 0.96)
        
        # Apply Windows 11 Acrylic blur effect
        if pywinstyles:
            try:
                pywinstyles.apply_style(self, "acrylic")
                pywinstyles.change_header_color(self, color="#1a1a1a")
            except Exception as e:
                pass
        
        self.api = APIHandler(TMDB_API_KEY, RAWG_API_KEY)
        self.media_queue = []
        self.current_item = None
        self.liked_items = []
        
        self.setup_ui()
        self.fetch_initial_data()

    def setup_ui(self):
        # 1. Main Title (Clean, Minimalist)
        self.title_label = ctk.CTkLabel(
            self, 
            text="Media Matcher", 
            font=("Segoe UI", 24, "bold"),
            text_color="#ffffff" 
        )
        self.title_label.pack(pady=(30, 15))
        
        # 2. The Liquid Glass Card
        # Soft gray with a thin, lighter border to mimic frosted glass
        self.card_frame = ctk.CTkFrame(
            self, 
            width=360, height=520, 
            corner_radius=25,
            fg_color="#2b2b2b", 
            border_width=1,
            border_color="#444444" 
        )
        self.card_frame.pack(pady=10, padx=20, fill="both", expand=True)
        self.card_frame.pack_propagate(False)
        
        # 3. Inside the Card: Image
        self.image_label = ctk.CTkLabel(
            self.card_frame, 
            text="Loading...", 
            font=("Segoe UI", 14),
            text_color="#aaaaaa"
        )
        self.image_label.pack(pady=25)
        
        # 4. Inside the Card: Title and Type
        self.info_title = ctk.CTkLabel(
            self.card_frame, 
            text="", 
            font=("Segoe UI", 22, "bold"), 
            wraplength=300,
            text_color="#ffffff"
        )
        self.info_title.pack(pady=(10, 0))
        
        self.info_type = ctk.CTkLabel(
            self.card_frame, 
            text="", 
            font=("Segoe UI", 14), 
            text_color="#aaaaaa" 
        )
        self.info_type.pack()
        
        # 5. The Buttons Frame
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=30)
        
        # Apple-style pill buttons
        self.btn_nah = ctk.CTkButton(
            self.btn_frame, 
            text="Pass", 
            fg_color="#333333", 
            hover_color="#444444",
            text_color="#ffffff",
            width=130, height=50, 
            corner_radius=25,
            font=("Segoe UI", 16, "bold"), 
            command=self.swipe_left
        )
        self.btn_nah.pack(side="left", padx=15)
        
        self.btn_yeah = ctk.CTkButton(
            self.btn_frame, 
            text="Like", 
            fg_color="#ffffff", 
            hover_color="#e0e0e0",
            text_color="#000000",
            width=130, height=50, 
            corner_radius=25,
            font=("Segoe UI", 16, "bold"), 
            command=self.swipe_right
        )
        self.btn_yeah.pack(side="right", padx=15)

    def fetch_initial_data(self):
        threading.Thread(target=self._fetch_data_thread, daemon=True).start()
        
    def _fetch_data_thread(self):
        anime = self.api.get_anime()
        self.media_queue.extend(anime)
        
        movies = self.api.get_movies()
        self.media_queue.extend(movies)
            
        games = self.api.get_games()
        self.media_queue.extend(games)
            
        random.shuffle(self.media_queue)
        self.after(0, self.show_next_item)

    def load_image_from_url(self, url):
        try:
            response = requests.get(url)
            image_data = Image.open(io.BytesIO(response.content))
            image_data = image_data.resize((300, 380), Image.Resampling.LANCZOS)
            photo = ctk.CTkImage(light_image=image_data, dark_image=image_data, size=(300, 380))
            return photo
        except Exception as e:
            print("Error loading image:", e)
            return None

    def show_next_item(self):
        if not self.media_queue:
            self.image_label.configure(image=None, text="Out of recommendations.\nProvide API Keys.")
            self.info_title.configure(text="")
            self.info_type.configure(text="")
            return
            
        self.current_item = self.media_queue.pop(0)
        
        self.info_title.configure(text=self.current_item['title'])
        self.info_type.configure(text=self.current_item['type'])
        self.image_label.configure(text="Loading image...", image=None)
        
        threading.Thread(target=self._load_image_thread, args=(self.current_item['image'],), daemon=True).start()
        
    def _load_image_thread(self, url):
        img = self.load_image_from_url(url)
        if img:
            self.after(0, lambda: self.image_label.configure(image=img, text=""))
        else:
            self.after(0, lambda: self.image_label.configure(text="Image unavailable"))

    def swipe_left(self):
        print(f"Skipped: {self.current_item['title']}")
        self.show_next_item()
        
    def swipe_right(self):
        print(f"Liked: {self.current_item['title']}")
        self.liked_items.append(self.current_item)
        self.show_next_item()

if __name__ == "__main__":
    app = MediaTinderApp()
    app.mainloop()
