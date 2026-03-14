import os

from dotenv import load_dotenv

# Load .env file
load_dotenv()

# 10 Groq API Keys for rotation
GROQ_API_KEYS = [
    os.getenv("GROQ_API_KEY_1"),
    os.getenv("GROQ_API_KEY_2"),
    os.getenv("GROQ_API_KEY_3"),
    os.getenv("GROQ_API_KEY_4"),
    os.getenv("GROQ_API_KEY_5"),
    os.getenv("GROQ_API_KEY_6"),
    os.getenv("GROQ_API_KEY_7"),
    os.getenv("GROQ_API_KEY_8"),
    os.getenv("GROQ_API_KEY_9"),
    os.getenv("GROQ_API_KEY_10"),
]

# Filter out None values in case some keys aren't provided
GROQ_API_KEYS = [k for k in GROQ_API_KEYS if k]

CURRENT_KEY_INDEX = 0

def get_groq_key():
    """Get the current API key."""
    global CURRENT_KEY_INDEX
    return GROQ_API_KEYS[CURRENT_KEY_INDEX]

def rotate_groq_key():
    """Rotate to the next API key."""
    global CURRENT_KEY_INDEX
    CURRENT_KEY_INDEX = (CURRENT_KEY_INDEX + 1) % len(GROQ_API_KEYS)
    print(f"DEBUG: Rotated to Groq API Key index {CURRENT_KEY_INDEX}")
    return GROQ_API_KEYS[CURRENT_KEY_INDEX]
