// ─── DEMO DATA ─────────────────────────────────────────────────────────────
const _TMDB_IMG = "https://image.tmdb.org/t/p/w500";

const DEMO_DATA = [
    { title: "Fullmetal Alchemist: Brotherhood", image: `${_TMDB_IMG}/5ZFUEOULaVml7GQfqfd4Adsk1uB.jpg`, desc: "Two brothers search for a Philosopher's Stone after an attempt to revive their deceased mother goes wrong. A sweeping story of sacrifice, loss, and the cost of playing god.", type: "Anime", rating: "9.1" },
    { title: "Attack on Titan", image: `${_TMDB_IMG}/hTP1DtLGFamjfu8WqjnuQdP1n4i.jpg`, desc: "In a world where humanity lives inside cities surrounded by enormous walls due to the Titans, one boy vows revenge after his mother is eaten.", type: "Anime", rating: "9.0" },
    { title: "Interstellar", image: `${_TMDB_IMG}/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg`, desc: "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival. Christopher Nolan's breathtaking sci-fi epic.", type: "Movie", rating: "8.6" },
    { title: "The Dark Knight", image: `${_TMDB_IMG}/qJ2tW6WMUDux911r6m7haRef0WH.jpg`, desc: "Batman raises the stakes in his war on crime. With the help of Lt. Jim Gordon and District Attorney Harvey Dent, he sets out to dismantle the remaining criminal organizations in Gotham.", type: "Movie", rating: "9.0" },
    { title: "The Witcher 3: Wild Hunt", image: `${_TMDB_IMG}/c9YMeXqBxbXUm8rRVCPLaqHPJJz.jpg`, desc: "As war rages on throughout the Northern Realms, you take on the role of a professional monster hunter and navigate a morally complex open world.", type: "Game", rating: "9.3" },
    { title: "Red Dead Redemption 2", image: `${_TMDB_IMG}/oxwHZAMHDNkRHUq6DufGBOT8z9L.jpg`, desc: "America, 1899. Arthur Morgan and the Van der Linde gang are outlaws on the run. Arthur must choose between his own ideals and loyalty to the gang who raised him.", type: "Game", rating: "9.7" },
    { title: "Steins;Gate", image: `${_TMDB_IMG}/pNIb1CSpRrDVMF4E3xd6KYHzqtd.jpg`, desc: "A self-proclaimed mad scientist accidentally discovers time travel via a microwave and must navigate the consequences of altering the past.", type: "Anime", rating: "8.8" },
    { title: "Parasite", image: `${_TMDB_IMG}/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg`, desc: "Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.", type: "Movie", rating: "8.5" },
    { title: "Elden Ring", image: `${_TMDB_IMG}/m3V8GGcHBIOPJXJQBFnRFqRYNQ0.jpg`, desc: "Rise, Tarnished, and be guided by grace to brandish the power of the Elden Ring and become an Elden Lord in the Lands Between.", type: "Game", rating: "9.5" },
    { title: "Dune: Part One", image: `${_TMDB_IMG}/d5NXSklXo0qyIYkgV94XAgMIckC.jpg`, desc: "Paul Atreides, a brilliant and gifted young man born into a great destiny, must travel to the most dangerous planet in the universe.", type: "Movie", rating: "8.0" }
];

// Shuffle array
const queue = [...DEMO_DATA].sort(() => Math.random() - 0.5);

// State
let likeCount = 0;
let passCount = 0;
let currentCardEl = null;

// DOM Elements
const cardArea = document.getElementById("card-area");
const likeStat = document.getElementById("like-count");
const passStat = document.getElementById("pass-count");
const queueStat = document.getElementById("queue-count");

const wlPanel = document.getElementById("watchlist-panel");
const wlToggle = document.getElementById("watchlist-toggle");
const wlClose = document.getElementById("watchlist-close");
const wlItems = document.getElementById("watchlist-items");
const wlCount = document.getElementById("watchlist-count");
const wlEmpty = document.getElementById("wl-empty");

const btnLike = document.getElementById("btn-like");
const btnPass = document.getElementById("btn-pass");

// ─── INIT ────────────────────────────────────────────────────────────────
function init() {
    gsap.registerPlugin(Draggable);
    updateStats();
    loadNextCard();

    // Watchlist Sidebar Logic
    wlToggle.addEventListener("click", () => {
        gsap.to(wlPanel, { x: "0%", duration: 0.6, ease: "power4.out" });
    });
    wlClose.addEventListener("click", () => {
        gsap.to(wlPanel, { x: "100%", duration: 0.5, ease: "power3.inOut" });
    });

    // Buttons
    btnLike.addEventListener("click", () => {
        if (!currentCardEl || gsap.isTweening(currentCardEl)) return;
        animateCardOut(currentCardEl, 1);
    });
    btnPass.addEventListener("click", () => {
        if (!currentCardEl || gsap.isTweening(currentCardEl)) return;
        animateCardOut(currentCardEl, -1);
    });

    // Keyboard shortcuts
    window.addEventListener("keydown", (e) => {
        if (!currentCardEl || gsap.isTweening(currentCardEl)) return;
        if (e.key === "ArrowRight" || e.key === "d") animateCardOut(currentCardEl, 1);
        if (e.key === "ArrowLeft" || e.key === "a") animateCardOut(currentCardEl, -1);
        if (e.key === "Escape") gsap.to(wlPanel, { x: "100%", duration: 0.5, ease: "power3.inOut" });
    });
}

function updateStats() {
    likeStat.textContent = likeCount;
    passStat.textContent = passCount;
    queueStat.textContent = queue.length;
    wlCount.textContent = likeCount;
}

function loadNextCard() {
    if (queue.length === 0) {
        const endMsg = document.createElement("div");
        endMsg.className = "skeleton";
        endMsg.innerHTML = "<div>You've seen everything!</div><div style='font-size:12px; font-weight:normal; margin-top:8px;'>Come back later ✦</div>";
        cardArea.appendChild(endMsg);
        currentCardEl = null;
        updateStats();
        return;
    }

    const item = queue.shift();
    updateStats();

    // Create Card DOM
    const card = document.createElement("div");
    card.className = "media-card";
    
    // Fallback gradient if no image
    const bgStr = item.image ? `url('${item.image}')` : "linear-gradient(45deg, #1e1e2a, #2a2a3a)";
    
    const typeClass = item.type === "Anime" ? "type-anime" : (item.type === "Movie" ? "type-movie" : "type-game");

    card.innerHTML = `
        <img class="poster" src="${item.image}" alt="poster" onerror="this.style.display='none'">
        <div class="card-overlay"></div>
        <div class="card-info">
            <div class="card-badges">
                <span class="type-badge ${typeClass}">${item.type}</span>
                <span class="rating">★ ${item.rating}</span>
            </div>
            <h2 class="card-title">${item.title}</h2>
            <p class="card-desc">${item.desc}</p>
        </div>
        <div class="swipe-hint hint-like">LIKE ✓</div>
        <div class="swipe-hint hint-pass">PASS ✕</div>
    `;

    // Skeleton loader for image
    const skeleton = document.createElement("div");
    skeleton.className = "skeleton";
    skeleton.innerHTML = `<div class="spinner"></div><div>Loading…</div>`;
    card.appendChild(skeleton);

    const img = card.querySelector(".poster");
    if (item.image) {
        img.onload = () => {
            gsap.to(skeleton, { opacity: 0, duration: 0.3, onComplete: () => skeleton.remove() });
        };
    } else {
        skeleton.remove();
    }

    // Set initial transform
    gsap.set(card, { scale: 0.95, opacity: 0, y: 30 });
    cardArea.appendChild(card);
    
    // Entrance Animation (Apple-like fluid spring)
    gsap.to(card, { scale: 1, opacity: 1, y: 0, duration: 0.8, ease: "elastic.out(1, 0.75)" });

    currentCardEl = card;
    card._itemData = item;

    // Draggable Logic
    Draggable.create(card, {
        type: "x,y",
        bounds: null,
        edgeResistance: 0.65,
        onDrag: function() {
            const x = this.x;
            // Rotate slightly based on x
            gsap.set(card, { rotation: x * 0.05 });
            
            // Show hints
            const likeHint = card.querySelector(".hint-like");
            const passHint = card.querySelector(".hint-pass");
            
            if (x > 30) {
                gsap.to(likeHint, { opacity: Math.min(x/100, 1), scale: 1, duration: 0.2 });
                gsap.set(passHint, { opacity: 0, scale: 0.8 });
            } else if (x < -30) {
                gsap.to(passHint, { opacity: Math.min(Math.abs(x)/100, 1), scale: 1, duration: 0.2 });
                gsap.set(likeHint, { opacity: 0, scale: 0.8 });
            } else {
                gsap.to([likeHint, passHint], { opacity: 0, scale: 0.8, duration: 0.2 });
            }
        },
        onDragEnd: function() {
            const x = this.x;
            const threshold = 100;

            if (x > threshold) {
                animateCardOut(card, 1);
            } else if (x < -threshold) {
                animateCardOut(card, -1);
            } else {
                // Snap back (fluid spring)
                gsap.to(card, { x: 0, y: 0, rotation: 0, duration: 0.6, ease: "elastic.out(1, 0.5)" });
                gsap.to(card.querySelectorAll(".swipe-hint"), { opacity: 0, scale: 0.8, duration: 0.2 });
            }
        }
    });
}

function animateCardOut(card, direction) {
    const item = card._itemData;
    // Disable dragging
    const dragInstance = Draggable.get(card);
    if (dragInstance) dragInstance.disable();

    // Show correct hint immediately
    if (direction === 1) {
        gsap.to(card.querySelector(".hint-like"), { opacity: 1, scale: 1, duration: 0.2 });
    } else {
        gsap.to(card.querySelector(".hint-pass"), { opacity: 1, scale: 1, duration: 0.2 });
    }

    // Fly out animation
    const flyX = direction * (window.innerWidth + 200);
    const flyRotation = direction * 20;

    gsap.to(card, {
        x: flyX,
        y: 50,
        rotation: flyRotation,
        opacity: 0,
        duration: 0.6,
        ease: "power2.in",
        onComplete: () => {
            card.remove();
            
            if (direction === 1) {
                likeCount++;
                addToWatchlist(item);
            } else {
                passCount++;
            }
            
            loadNextCard();
        }
    });
}

function addToWatchlist(item) {
    wlEmpty.style.display = "none";
    
    const typeClass = item.type === "Anime" ? "type-anime" : (item.type === "Movie" ? "type-movie" : "type-game");
    
    const el = document.createElement("div");
    el.className = "wl-item";
    el.innerHTML = `
        <span class="wl-item-badge ${typeClass}">${item.type}</span>
        <span class="wl-item-title">${item.title}</span>
    `;
    wlItems.appendChild(el);
}

// Start
document.addEventListener("DOMContentLoaded", init);
