THEMES = {
    "dark": {"bg": "#0f172a", "fg": "#ffffff", "card": "#334155", "btn": "#22c55e"},
    "light": {"bg": "#f8fafc", "fg": "#000000", "card": "#e2e8f0", "btn": "#2563eb"}
}

current = "dark"

def toggle():
    global current
    current = "light" if current == "dark" else "dark"

def get():
    return THEMES[current]
