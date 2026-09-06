"""
Media Matcher — Awwwards/Dribbble Edition
Dark Luxury Cinematic Theme | Letterboxd × Apple TV+
"""

import customtkinter as ctk
from PIL import Image
import requests
import io
import threading
import random
from api_handlers import APIHandler, _make_placeholder

try:
    import pywinstyles
except ImportError:
    pywinstyles = None

# ─── DPI: tell Windows NOT to scale the window so geometry is exact ──────────
ctk.deactivate_automatic_dpi_awareness()

# ─── CONFIGURATION ───────────────────────────────────────────────────────────
TMDB_API_KEY = "YOUR_TMDB_API_KEY"
RAWG_API_KEY = "YOUR_RAWG_API_KEY"

# ─── DESIGN SYSTEM ───────────────────────────────────────────────────────────
COLORS = {
    "bg":           "#0a0a0f",
    "bg_secondary": "#111118",
    "surface":      "#16161f",
    "surface_2":    "#1e1e2a",
    "border":       "#2a2a3a",
    "border_glow":  "#3a3a5a",
    "neon_like":    "#00f5a0",
    "neon_pass":    "#ff4d6d",
    "badge_anime":  "#a855f7",
    "badge_movie":  "#3b82f6",
    "badge_game":   "#22c55e",
    "text_primary":   "#f0f0ff",
    "text_secondary": "#9090a8",
    "text_muted":     "#505068",
}

FONTS = {
    "title":    ("Segoe UI", 19, "bold"),
    "subtitle": ("Segoe UI", 13, "bold"),
    "body":     ("Segoe UI", 11),
    "caption":  ("Segoe UI", 10),
    "badge":    ("Segoe UI", 10, "bold"),
    "btn":      ("Segoe UI", 14, "bold"),
    "logo":     ("Segoe UI", 17, "bold"),
    "counter":  ("Segoe UI", 10),
}

BADGE_COLORS = {
    "Anime": COLORS["badge_anime"],
    "Movie": COLORS["badge_movie"],
    "Game":  COLORS["badge_game"],
}

CARD_W, CARD_H = 360, 490


# ─── ANIMATED BUTTON ─────────────────────────────────────────────────────────
class AnimatedButton(ctk.CTkButton):
    def __init__(self, *args, **kwargs):
        self._base_w = kwargs.get("width", 100)
        self._base_h = kwargs.get("height", 40)
        super().__init__(*args, **kwargs)
        self.bind("<ButtonPress-1>",   self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)

    def _on_press(self, _):
        self.configure(width=self._base_w - 4, height=self._base_h - 4)

    def _on_release(self, _):
        self.configure(width=self._base_w, height=self._base_h)


# ─── MEDIA CARD ──────────────────────────────────────────────────────────────
class MediaCard(ctk.CTkFrame):
    """
    Self-contained card:
    - Poster image (or gradient placeholder)
    - Info panel: badge, rating, title, synopsis flip
    - Drag left/right to swipe with animation
    - Keyboard shortcuts via trigger_like / trigger_pass
    """
    DRAG_THRESHOLD = 80
    FLY_DISTANCE   = 600
    SNAP_STEPS     = 10
    FLY_STEPS      = 12

    def __init__(self, master, on_like, on_pass, **kwargs):
        super().__init__(
            master,
            width=CARD_W, height=CARD_H,
            corner_radius=22,
            fg_color=COLORS["surface"],
            border_width=1,
            border_color=COLORS["border"],
            **kwargs,
        )
        self.pack_propagate(False)

        self.on_like     = on_like
        self.on_pass     = on_pass
        self._flipped    = False
        self._flip_anim  = False
        self._drag_x     = 0
        self._drag_total = 0
        self._offset     = 0
        self._animating  = False

        # ── Poster (full card) ────────────────────────────────────────────────
        self.poster_label = ctk.CTkLabel(
            self, text="", fg_color=COLORS["surface"],
        )
        self.poster_label.place(x=0, y=0, relwidth=1, relheight=1)

        # ── Skeleton ──────────────────────────────────────────────────────────
        self.skeleton = ctk.CTkFrame(
            self, fg_color=COLORS["surface_2"], corner_radius=22,
        )
        self.skeleton.place(x=0, y=0, relwidth=1, relheight=1)
        self._pulse = 0.0
        self._pulse_dir = 1
        self._tick_skeleton()

        self.skeleton_text = ctk.CTkLabel(
            self.skeleton,
            text="✦  Loading…",
            font=FONTS["body"],
            text_color=COLORS["text_muted"],
        )
        self.skeleton_text.place(relx=0.5, rely=0.5, anchor="center")

        # ── Swipe hints ───────────────────────────────────────────────────────
        self.hint_like = ctk.CTkLabel(
            self, text="LIKE ✓",
            font=("Segoe UI", 28, "bold"),
            text_color=COLORS["neon_like"],
            fg_color=COLORS["surface"],
        )
        self.hint_pass = ctk.CTkLabel(
            self, text="PASS ✕",
            font=("Segoe UI", 28, "bold"),
            text_color=COLORS["neon_pass"],
            fg_color=COLORS["surface"],
        )

        # ── Info panel ────────────────────────────────────────────────────────
        self.info_panel = ctk.CTkFrame(
            self, fg_color=COLORS["surface"],
            corner_radius=0, height=150,
        )
        self.info_panel.place(x=0, rely=1.0, anchor="sw", relwidth=1)
        self.info_panel.pack_propagate(False)

        badge_row = ctk.CTkFrame(self.info_panel, fg_color="transparent")
        badge_row.pack(fill="x", padx=18, pady=(12, 0))

        self.badge = ctk.CTkLabel(
            badge_row, text="", font=FONTS["badge"], text_color="#fff",
            fg_color=COLORS["badge_anime"], corner_radius=6,
            width=55, height=20,
        )
        self.badge.pack(side="left")

        self.rating_label = ctk.CTkLabel(
            badge_row, text="", font=FONTS["badge"],
            text_color=COLORS["text_secondary"],
        )
        self.rating_label.pack(side="right")

        self.title_label = ctk.CTkLabel(
            self.info_panel, text="", font=FONTS["title"],
            text_color=COLORS["text_primary"],
            wraplength=CARD_W - 40, justify="left", anchor="w",
        )
        self.title_label.pack(fill="x", padx=18, pady=(5, 0))

        self.flip_hint = ctk.CTkLabel(
            self.info_panel, text="tap here for synopsis  ↺",
            font=FONTS["caption"], text_color=COLORS["text_muted"], anchor="w",
        )
        self.flip_hint.pack(fill="x", padx=18, pady=(3, 8))

        # ── Synopsis panel ────────────────────────────────────────────────────
        self.synopsis_panel = ctk.CTkFrame(
            self, fg_color=COLORS["surface_2"], corner_radius=22,
        )
        self.synopsis_title = ctk.CTkLabel(
            self.synopsis_panel, text="", font=FONTS["subtitle"],
            text_color=COLORS["text_primary"],
            wraplength=CARD_W - 50, justify="left", anchor="w",
        )
        self.synopsis_title.pack(fill="x", padx=22, pady=(24, 6))

        self.synopsis_text = ctk.CTkLabel(
            self.synopsis_panel, text="", font=FONTS["body"],
            text_color=COLORS["text_secondary"],
            wraplength=CARD_W - 44, justify="left", anchor="nw",
        )
        self.synopsis_text.pack(fill="x", padx=22)

        ctk.CTkLabel(
            self.synopsis_panel, text="tap to flip back  ↺",
            font=FONTS["caption"], text_color=COLORS["text_muted"], anchor="w",
        ).pack(side="bottom", fill="x", padx=22, pady=14)

        # ── Drag bindings on poster + card root ───────────────────────────────
        for w in (self, self.poster_label):
            w.bind("<ButtonPress-1>",   self._drag_start)
            w.bind("<B1-Motion>",       self._drag_motion)
            w.bind("<ButtonRelease-1>", self._drag_end)

        # ── Flip bindings on info panel ───────────────────────────────────────
        for w in (self.info_panel, self.flip_hint, self.title_label,
                  self.badge, self.rating_label):
            w.bind("<ButtonPress-1>",   self._drag_start)
            w.bind("<B1-Motion>",       self._drag_motion)
            w.bind("<ButtonRelease-1>", self._drag_end_or_flip)

        for w in (self.synopsis_panel, self.synopsis_title, self.synopsis_text):
            w.bind("<Button-1>", lambda _: self._toggle_flip())

    # ── Skeleton pulse ────────────────────────────────────────────────────────
    def _tick_skeleton(self):
        if not self.winfo_exists():
            return
        self._pulse += self._pulse_dir * 0.04
        if self._pulse >= 1.0:
            self._pulse_dir = -1
        elif self._pulse <= 0.0:
            self._pulse_dir = 1
        v = int(28 + self._pulse * 22)
        if self.skeleton.winfo_exists():
            self.skeleton.configure(fg_color=f"#{v:02x}{v:02x}{v+6:02x}")
        self.after(40, self._tick_skeleton)

    # ── Public API ────────────────────────────────────────────────────────────
    def load(self, item: dict):
        self._flipped = False
        self._hide_synopsis()
        title = item.get("title", "Unknown")
        self.title_label.configure(text=title)
        self.synopsis_title.configure(text=title)

        desc = item.get("desc", "No description available.")
        if len(desc) > 320:
            desc = desc[:317] + "…"
        self.synopsis_text.configure(text=desc)

        mtype = item.get("type", "Unknown")
        self.badge.configure(
            text=f"  {mtype.upper()}  ",
            fg_color=BADGE_COLORS.get(mtype, COLORS["border_glow"]),
        )
        r = item.get("rating", "")
        self.rating_label.configure(text=f"★  {r}" if r else "")

    def show_loading(self):
        self.skeleton.place(x=0, y=0, relwidth=1, relheight=1)
        self.skeleton.tkraise()
        self.skeleton_text.configure(text="✦  Loading…")
        self.poster_label.configure(image=None)

    def show_image(self, img):
        if img:
            self.skeleton.place_forget()
            self.poster_label.configure(image=img)
        else:
            self.skeleton_text.configure(text="⚠  Image unavailable")

    # ── Flip ──────────────────────────────────────────────────────────────────
    def _toggle_flip(self):
        if self._flip_anim:
            return
        if self._flipped:
            self._hide_synopsis()
        else:
            self._show_synopsis()
        self._flipped = not self._flipped

    def _show_synopsis(self):
        self._flip_anim = True
        self.synopsis_panel.place(x=0, y=0, relwidth=1, relheight=1)
        self.synopsis_panel.tkraise()
        self.after(150, lambda: setattr(self, "_flip_anim", False))

    def _hide_synopsis(self):
        self._flip_anim = True
        self.synopsis_panel.place_forget()
        self.after(150, lambda: setattr(self, "_flip_anim", False))

    # ── Drag / swipe ──────────────────────────────────────────────────────────
    def _drag_start(self, event):
        if not self._animating:
            self._drag_x     = event.x_root
            self._drag_total = 0

    def _drag_motion(self, event):
        if self._animating:
            return
        delta = event.x_root - self._drag_x
        self._drag_total = abs(delta)
        self._move(delta)
        if delta > 15:
            self.hint_like.place(x=18, y=28)
            self.hint_pass.place_forget()
        elif delta < -15:
            self.hint_pass.place(relx=1.0, x=-145, y=28)
            self.hint_like.place_forget()
        else:
            self.hint_like.place_forget()
            self.hint_pass.place_forget()

    def _drag_end(self, event):
        if self._animating:
            return
        delta = event.x_root - self._drag_x
        self._clear_hints()
        if delta > self.DRAG_THRESHOLD:
            self._fly("right", self.on_like)
        elif delta < -self.DRAG_THRESHOLD:
            self._fly("left", self.on_pass)
        else:
            self._snap_back()

    def _drag_end_or_flip(self, event):
        if self._animating:
            return
        delta = event.x_root - self._drag_x
        self._clear_hints()
        if delta > self.DRAG_THRESHOLD:
            self._fly("right", self.on_like)
        elif delta < -self.DRAG_THRESHOLD:
            self._fly("left", self.on_pass)
        elif self._drag_total < 8:
            self._toggle_flip()
        else:
            self._snap_back()

    def _clear_hints(self):
        self.hint_like.place_forget()
        self.hint_pass.place_forget()

    def _move(self, delta):
        self._offset = delta
        px = self.winfo_x() - self._offset + delta
        # Use place to shift card within its parent
        self.place_configure(x=px)

    def _snap_back(self):
        self._animating = True
        start_x = self.winfo_x()
        # target = original centered x
        parent_w = self.master.winfo_width()
        target_x = (parent_w - CARD_W) // 2

        def _step(i):
            if i > self.SNAP_STEPS or not self.winfo_exists():
                if self.winfo_exists():
                    self.place_configure(x=target_x)
                self._animating = False
                self._offset = 0
                return
            t = i / self.SNAP_STEPS
            ease = 1 - (1 - t) ** 3
            x = int(start_x + (target_x - start_x) * ease)
            self.place_configure(x=x)
            self.after(16, lambda: _step(i + 1))

        _step(1)

    def _fly(self, direction, callback):
        self._animating = True
        start_x  = self.winfo_x()
        parent_w = self.master.winfo_width()
        center_x = (parent_w - CARD_W) // 2
        target_x = center_x + (self.FLY_DISTANCE if direction == "right" else -self.FLY_DISTANCE)

        def _step(i):
            if i > self.FLY_STEPS or not self.winfo_exists():
                if self.winfo_exists():
                    # Reset position silently, then fire callback
                    self.place_configure(x=center_x)
                self._animating = False
                self._offset = 0
                callback()
                return
            t = i / self.FLY_STEPS
            ease = t * t * (3 - 2 * t)
            x = int(start_x + (target_x - start_x) * ease)
            self.place_configure(x=x)
            self.after(14, lambda: _step(i + 1))

        _step(1)

    def trigger_like(self):
        if not self._animating:
            self._fly("right", self.on_like)

    def trigger_pass(self):
        if not self._animating:
            self._fly("left", self.on_pass)


# ─── WATCHLIST SIDEBAR ───────────────────────────────────────────────────────
class WatchlistPanel(ctk.CTkFrame):
    PANEL_W = 270
    STEPS   = 10

    def __init__(self, master, **kwargs):
        super().__init__(
            master, width=self.PANEL_W,
            fg_color=COLORS["bg_secondary"],
            border_width=1, border_color=COLORS["border"],
            corner_radius=0, **kwargs,
        )
        self._visible = False
        self._anim    = False

        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.pack(fill="x", padx=18, pady=(18, 8))
        ctk.CTkLabel(hdr, text="✦  Watchlist", font=FONTS["subtitle"],
                     text_color=COLORS["text_primary"]).pack(side="left")
        ctk.CTkButton(hdr, text="✕", width=26, height=26, corner_radius=13,
                      fg_color=COLORS["surface_2"], hover_color=COLORS["border"],
                      text_color=COLORS["text_secondary"], font=FONTS["caption"],
                      command=self.hide).pack(side="right")

        ctk.CTkFrame(self, height=1, fg_color=COLORS["border"]).pack(fill="x")

        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent",
                                              scrollbar_button_color=COLORS["border"])
        self.scroll.pack(fill="both", expand=True, padx=8, pady=8)

        self.empty = ctk.CTkLabel(self.scroll,
                                  text="Nothing liked yet.\nSwipe right on something! →",
                                  font=FONTS["body"], text_color=COLORS["text_muted"],
                                  justify="center")
        self.empty.pack(pady=40)
        self.count = 0

    def add_item(self, item):
        self.count += 1
        self.empty.pack_forget()
        row = ctk.CTkFrame(self.scroll, fg_color=COLORS["surface"],
                           corner_radius=10, border_width=1, border_color=COLORS["border"])
        row.pack(fill="x", pady=3, padx=3)
        bc = BADGE_COLORS.get(item.get("type", ""), COLORS["border_glow"])
        ctk.CTkLabel(row, text=f"  {item.get('type','?').upper()}  ",
                     font=FONTS["badge"], text_color="#fff", fg_color=bc,
                     corner_radius=5, width=44, height=16).pack(side="left", padx=(8,6), pady=8)
        ctk.CTkLabel(row, text=item.get("title", "Unknown"),
                     font=FONTS["caption"], text_color=COLORS["text_primary"],
                     anchor="w", wraplength=155).pack(side="left", pady=8)

    def show(self):
        if self._visible or self._anim:
            return
        self._visible = self._anim = True
        app_w = self.master.winfo_width()
        s, e = app_w, app_w - self.PANEL_W
        self.place(x=s, y=0, relheight=1)
        self.tkraise()
        def step(i):
            if i > self.STEPS:
                self.place(x=e); self._anim = False; return
            t = i / self.STEPS
            self.place(x=int(s + (e-s)*(1-(1-t)**3)))
            self.after(14, lambda: step(i+1))
        step(1)

    def hide(self):
        if not self._visible or self._anim:
            return
        self._anim = True
        app_w = self.master.winfo_width()
        s, e = app_w - self.PANEL_W, app_w
        def step(i):
            if i > self.STEPS:
                self.place_forget(); self._visible = self._anim = False; return
            t = i / self.STEPS
            self.place(x=int(s + (e-s)*(t*t*(3-2*t))))
            self.after(14, lambda: step(i+1))
        step(1)

    def toggle(self):
        self.hide() if self._visible else self.show()


# ─── MAIN APP ────────────────────────────────────────────────────────────────
class MediaTinderApp(ctk.CTk):

    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        self.title("Media Matcher  ✦")
        self.geometry("480x820")
        self.resizable(False, False)
        self.configure(fg_color=COLORS["bg"])

        if pywinstyles:
            try:
                pywinstyles.apply_style(self, "acrylic")
                pywinstyles.change_header_color(self, color="#0a0a0f")
            except Exception:
                pass

        self.api          = APIHandler(TMDB_API_KEY, RAWG_API_KEY)
        self.media_queue  = []
        self.current_item = None
        self.liked_items  = []
        self.like_count   = 0
        self.pass_count   = 0

        self._build_ui()
        self._bind_keys()
        self.fetch_initial_data()

    # ── Build UI ─────────────────────────────────────────────────────────────
    def _build_ui(self):
        # ── Top bar ──────────────────────────────────────────────────────────
        topbar = ctk.CTkFrame(self, fg_color="transparent", height=60)
        topbar.pack(fill="x", padx=22, pady=(18, 0))
        topbar.pack_propagate(False)

        ctk.CTkLabel(topbar, text="✦ media matcher",
                     font=FONTS["logo"], text_color=COLORS["text_primary"],
                     anchor="w").pack(side="left")

        self.wl_btn = ctk.CTkButton(
            topbar, text="Watchlist  →", font=FONTS["badge"],
            width=105, height=32, corner_radius=16,
            fg_color=COLORS["surface_2"], hover_color=COLORS["border"],
            border_width=1, border_color=COLORS["border"],
            text_color=COLORS["text_secondary"], command=self._toggle_wl,
        )
        self.wl_btn.pack(side="right")

        # ── Stats ─────────────────────────────────────────────────────────────
        stats = ctk.CTkFrame(self, fg_color="transparent", height=26)
        stats.pack(fill="x", padx=22, pady=(6, 0))

        self.like_lbl = ctk.CTkLabel(stats, text="✓  0 liked",
                                     font=FONTS["counter"],
                                     text_color=COLORS["neon_like"], anchor="w")
        self.like_lbl.pack(side="left")

        self.pass_lbl = ctk.CTkLabel(stats, text="0 passed  ✕",
                                     font=FONTS["counter"],
                                     text_color=COLORS["neon_pass"], anchor="e")
        self.pass_lbl.pack(side="right")

        self.queue_lbl = ctk.CTkLabel(stats, text="", font=FONTS["counter"],
                                      text_color=COLORS["text_muted"])
        self.queue_lbl.pack(side="left", padx=12)

        # ── Divider ───────────────────────────────────────────────────────────
        ctk.CTkFrame(self, height=1, fg_color=COLORS["border"]).pack(
            fill="x", padx=22, pady=(10, 0))

        # ── Card row: centred with pack ───────────────────────────────────────
        # A transparent row frame sized to hold exactly the card
        card_row = ctk.CTkFrame(self, fg_color=COLORS["bg"])
        card_row.pack(fill="both", expand=True)

        # Centre the card horizontally with an inner pack frame
        inner = ctk.CTkFrame(card_row, fg_color=COLORS["bg"])
        inner.pack(expand=True)   # expand centres it in card_row

        self.card = MediaCard(inner, on_like=self._do_like, on_pass=self._do_pass)
        self.card.pack(padx=0, pady=16)   # pack — respects pack_propagate(False) size

        # ── Action buttons ────────────────────────────────────────────────────
        btn_row = ctk.CTkFrame(self, fg_color="transparent", height=110)
        btn_row.pack(fill="x", pady=(0, 18))
        btn_row.pack_propagate(False)

        self.btn_pass = AnimatedButton(
            btn_row, text="✕  Pass", font=FONTS["btn"],
            width=148, height=52, corner_radius=26,
            fg_color="transparent", hover_color=COLORS["surface_2"],
            border_width=2, border_color=COLORS["neon_pass"],
            text_color=COLORS["neon_pass"], command=self._do_pass,
        )
        self.btn_pass.place(relx=0.22, rely=0.45, anchor="center")

        self.btn_like = AnimatedButton(
            btn_row, text="Like  ✓", font=FONTS["btn"],
            width=148, height=52, corner_radius=26,
            fg_color=COLORS["neon_like"], hover_color="#00d988",
            text_color="#000000", command=self._do_like,
        )
        self.btn_like.place(relx=0.78, rely=0.45, anchor="center")

        ctk.CTkLabel(btn_row, text="← A / D →  or drag the card",
                     font=FONTS["caption"],
                     text_color=COLORS["text_muted"]).place(relx=0.5, rely=0.85, anchor="center")

        # ── Watchlist ─────────────────────────────────────────────────────────
        self.watchlist = WatchlistPanel(self)

    # ── Keyboard ─────────────────────────────────────────────────────────────
    def _bind_keys(self):
        self.bind("<Left>",   lambda _: self.card.trigger_pass())
        self.bind("<Right>",  lambda _: self.card.trigger_like())
        self.bind("a",        lambda _: self.card.trigger_pass())
        self.bind("d",        lambda _: self.card.trigger_like())
        self.bind("<Escape>", lambda _: self.watchlist.hide())

    # ── Data ─────────────────────────────────────────────────────────────────
    def fetch_initial_data(self):
        self.card.show_loading()
        threading.Thread(target=self._fetch, daemon=True).start()

    def _fetch(self):
        q  = self.api.get_anime()
        q += self.api.get_movies()
        q += self.api.get_games()
        random.shuffle(q)
        self.media_queue = q
        self.after(0, self._show_next)

    def _show_next(self):
        if not self.media_queue:
            self.card.show_loading()
            self.card.skeleton_text.configure(text="You've seen it all!\nCome back later ✦")
            return
        self.current_item = self.media_queue.pop(0)
        self.queue_lbl.configure(text=f"{len(self.media_queue)} left")
        self.card.load(self.current_item)
        self.card.show_loading()
        threading.Thread(target=self._load_img, args=(self.current_item,), daemon=True).start()

    def _load_img(self, item):
        url   = item.get("image")
        title = item.get("title", "Unknown")
        mtype = item.get("type", "Movie")
        pil   = None

        if url:
            try:
                pil = Image.open(io.BytesIO(requests.get(url, timeout=8).content)).convert("RGB")
            except Exception as e:
                print(f"Image fetch failed: {e}")

        if pil is None:
            pil = _make_placeholder(title, mtype, CARD_W, CARD_H)

        # Fit to card
        iw, ih = pil.size
        ratio  = min(CARD_W / iw, CARD_H / ih)
        tw, th = int(iw * ratio), int(ih * ratio)
        pil    = pil.resize((tw, th), Image.Resampling.LANCZOS)
        canvas = Image.new("RGB", (CARD_W, CARD_H), COLORS["surface"])
        canvas.paste(pil, ((CARD_W - tw) // 2, (CARD_H - th) // 2))

        photo = ctk.CTkImage(light_image=canvas, dark_image=canvas, size=(CARD_W, CARD_H))
        self.after(0, lambda: self.card.show_image(photo))

    # ── Actions ───────────────────────────────────────────────────────────────
    def _do_like(self):
        if not self.current_item:
            return
        self.liked_items.append(self.current_item)
        self.watchlist.add_item(self.current_item)
        self.like_count += 1
        self.like_lbl.configure(text=f"✓  {self.like_count} liked")
        self.wl_btn.configure(text=f"Watchlist ({self.like_count})  →")
        print(f"[LIKED]  {self.current_item['title']}")
        self._show_next()

    def _do_pass(self):
        if not self.current_item:
            return
        self.pass_count += 1
        self.pass_lbl.configure(text=f"{self.pass_count} passed  ✕")
        print(f"[PASSED] {self.current_item['title']}")
        self._show_next()

    def _toggle_wl(self):
        self.watchlist.toggle()


# ─── ENTRY POINT ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = MediaTinderApp()
    app.mainloop()
