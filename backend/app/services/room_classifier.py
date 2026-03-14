import sys
import os
from pathlib import Path

# Add backend root to path
BACKEND_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(BACKEND_ROOT, "automation"))

try:
    # This works if automation is in the path
    from src.predict_room import predict_room
except ImportError:
    # Local fallback
    def predict_room(path): return {"room_type": "living_room", "confidence": 0.0}

def classify_room(image_path):
    """Bridge to automation/src/predict_room.py"""
    try:
        result = predict_room(image_path)
        return result["room_type"]
    except Exception:
        return "unknown"