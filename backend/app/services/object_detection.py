import sys
import os

# Add backend root to path
BACKEND_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(BACKEND_ROOT, "automation"))

try:
    from src.object_detection import detect_objects
except ImportError:
    def detect_objects(path): return []

def detect_property_objects(image_path):
    """Bridge to automation/src/object_detection.py"""
    try:
        return detect_objects(image_path)
    except Exception:
        return []
