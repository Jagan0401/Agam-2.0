import cv2
import numpy as np

def final_quality_score(image_path):
    """
    Analyzes image quality using OpenCV metrics:
    1. Sharpness (Laplacian variance)
    2. Brightness (Mean pixel intensity)
    3. Contrast (Standard deviation of intensity)
    """
    try:
        img = cv2.imread(image_path)
        if img is None:
            return {"final_quality": 0.0, "metrics": {"error": "Could not read image"}}
            
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # 1. Blur detection (Sharpness)
        # Higher is sharper. Typically > 100 is good.
        sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()
        sharp_score = min(sharpness / 300.0, 1.0) * 10
        
        # 2. Brightness
        # Mean should be around 127 for balanced lighting.
        brightness = np.mean(gray)
        bright_score = 10 - (abs(brightness - 127) / 127 * 10)
        
        # 3. Contrast
        # Higher is generally better for clarity.
        contrast = gray.std()
        contrast_score = min(contrast / 80.0, 1.0) * 10
        
        # Weighted final score
        final = (sharp_score * 0.5) + (bright_score * 0.3) + (contrast_score * 0.2)
        
        return {
            "final_quality": round(min(max(final, 0), 10), 2),
            "metrics": {
                "sharpness": round(sharpness, 2),
                "brightness": round(brightness, 2),
                "contrast": round(contrast, 2)
            }
        }
    except Exception as e:
        return {"final_quality": 0.0, "error": str(e)}
