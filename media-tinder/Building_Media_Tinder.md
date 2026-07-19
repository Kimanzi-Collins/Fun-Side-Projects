# Building My "Media Tinder" From Scratch 🍿

Here is exactly how I built my swipe-based recommender app from the ground up! Instead of relying on pre-built templates, I engineered the entire logic, from fetching data over the internet to managing a modern graphical interface.

## 1. Choosing My Tech Stack
When building a GUI (Graphical User Interface) app in Python, the standard library is `tkinter`. However, `tkinter` can look very outdated. To make my app look modern and feel like Tinder, I chose **CustomTkinter**. It provides beautiful, rounded, dark-mode components right out of the box, making my app look premium with minimal styling effort.

For data, I needed a way to get a constant stream of movies, anime, and games. I decided to use three main APIs (Application Programming Interfaces, which are basically websites designed for code to read):
*   **Jikan (MyAnimeList):** Free, no API key needed. Great for Anime!
*   **TMDB (The Movie Database):** Free, needs an API key. 
*   **RAWG:** Free, needs an API key. Great for games!

---

## 2. Setting Up the APIs (`api_handlers.py`)

First, I created a way to fetch data from the internet. I used the `requests` library, which allows Python to send HTTP requests just like a web browser does.

```python
import requests

class APIHandler:
    def __init__(self, tmdb_key="", rawg_key=""):
        self.tmdb_key = tmdb_key
        self.rawg_key = rawg_key

    def get_anime(self, page=1):
        # 1. I format the URL that points to the API's server
        url = f"https://api.jikan.moe/v4/top/anime?page={page}"
        
        # 2. I send a GET request to the URL
        response = requests.get(url)
        
        # 3. HTTP status code 200 means "OK" (success)
        if response.status_code == 200:
            # 4. I convert the massive text response into a Python Dictionary
            data = response.json()['data']
            
            # 5. I create a clean list to hold only the exact data my app needs
            results = []
            for d in data:
                if d.get('images'):
                    results.append({
                        "title": d.get('title_english') or d.get('title'),
                        "image": d['images']['jpg']['large_image_url'],
                        "type": "Anime"
                    })
            return results
```
### Breaking down the API Logic
When an API responds, it sends a massive block of JSON (JavaScript Object Notation). It contains hundreds of details I don't care about (like the producer's name or the exact runtime). 

By calling `response.json()`, I convert that data into a Python Dictionary. Then, I loop through it (`for d in data:`) and extract *only* what my UI needs: the title, the image URL, and the type of media. This keeps my app lightweight and fast.

> [!TIP]
> **Where I got my API Keys:**
> *   **TMDB (Movies/Series):** I went to [themoviedb.org](https://www.themoviedb.org/), created an account, and went to Settings -> API.
> *   **RAWG (Games):** I went to [rawg.io/apidocs](https://rawg.io/apidocs) to grab a free key.

---

## 3. Building the GUI (`main.py`)

I created my main application by designing a class `MediaTinderApp` that inherits from `customtkinter.CTk`. This means my class *is* the main window.

### The Layout Strategy
I designed the layout by stacking elements vertically. In `customtkinter`, `pack()` is the layout manager that physically places elements onto the screen.

```python
def setup_ui(self):
    # 1. Main Title
    self.title_label = ctk.CTkLabel(self, text="Media Matcher 🍿", font=("Helvetica", 28, "bold"))
    self.title_label.pack(pady=(20, 10))
    
    # 2. The Card Frame (My Tinder-like Card)
    self.card_frame = ctk.CTkFrame(self, width=340, height=500, corner_radius=20)
    self.card_frame.pack(pady=10, padx=20, fill="both", expand=True)
    self.card_frame.pack_propagate(False) # This forces the card to stay its exact size!
```
### The UI Components
1.  **`CTkLabel`:** I used this for text (like the title) but also for images. Tkinter displays images by attaching them to Labels!
2.  **`CTkFrame`:** This acts as a container. My `card_frame` groups the image and the text together into one solid block with a rounded corner (`corner_radius=20`).
3.  **`pack_propagate(False)`:** This is a crucial detail! Normally, a frame shrinks to perfectly fit whatever is inside it. By turning propagation off, my card stays a rigid 340x500 pixels, preventing the app from violently resizing every time a new image loads.

---

## 4. Multithreading (My Secret Sauce) 🤫

If I download images on the main UI thread, my entire app will freeze and say "Not Responding" while it waits for the image to download from the internet. This creates a terrible user experience.

To solve this, I used **Threading**. This tells my computer's processor to split its attention: keep drawing the UI smoothly on one thread, while quietly downloading the image in the background on another.

```python
import threading

def show_next_item(self):
    # ... setup text ...
    
    # I tell Python: "Hey, go execute _load_image_thread in the background, don't freeze my app!"
    # I pass the image URL as an argument to that background task.
    threading.Thread(target=self._load_image_thread, args=(self.current_item['image'],)).start()
```

---

## 5. The "Swipe" Logic

To manage the Tinder-like flow, I utilized a Queue system using standard Python Lists.

I keep a list called `self.media_queue`. It starts full of movies, anime, and games.
When I click "Yeah" or "Nah", the following logic fires:

```python
def swipe_right(self):
    print(f"Liked: {self.current_item['title']}")
    # 1. Save it to my liked list
    self.liked_items.append(self.current_item)
    # 2. Trigger the next item to show up
    self.show_next_item() 

def show_next_item(self):
    # .pop(0) removes the very first item from my list and gives it to me.
    # The list shrinks by 1, and the next item takes its place at the front!
    self.current_item = self.media_queue.pop(0)
```
1. I `pop(0)` the first item off the queue.
2. If I clicked "Yeah", I `append()` it to my `self.liked_items` list to remember it for later.
3. The UI automatically updates to show the *new* first item in the queue.

And that is how I built a fast, multi-threaded, API-driven GUI application entirely from scratch!
