import sys
import os

# Add backend root to path
BACKEND_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(BACKEND_ROOT, "automation"))

try:
    from src.quality_score import final_quality_score
except ImportError:
    def final_quality_score(path): return {"final_quality": 0.0, "metrics": {}}

def quality_score(image_path):
    """Bridge to automation/src/quality_score.py"""
    try:
        result = final_quality_score(image_path)
        return result
    except Exception:
        return {"final_quality": 0.0, "metrics": {}}