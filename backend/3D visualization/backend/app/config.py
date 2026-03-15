# Configuration settings for the Real Estate AI Tour backend

# Server settings
HOST = "0.0.0.0"
PORT = 8000

# File paths
IMAGES_DIR = "images"
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "bmp", "tiff"}

# Room types (for simulation)
ROOM_TYPES = ["living_room", "bedroom", "kitchen", "bathroom"]

# CORS settings
CORS_ORIGINS = [
    "http://localhost:3000",  # React dev server
    "http://localhost:5173",  # Vite dev server
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://localhost:5175",
    "http://localhost:5176",
    "http://127.0.0.1:5174",
    "http://127.0.0.1:5175",
    "http://127.0.0.1:5176",
]