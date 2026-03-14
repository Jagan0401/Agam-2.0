import os
import sys
from typing import List, Dict, Any
from app.services.room_classifier import classify_room
from app.services.object_detection import detect_property_objects
from app.services.quality_service import quality_score
from app.services.clip_service import generate_tags
from app.services.groq_service import GroqService

class AutomationPipeline:
    """
    Agam AI Property Automation Pipeline
    Follows parallel model architecture with fusion and insight engine.
    """
    
    @staticmethod
    def analyze_image(image_path: str) -> Dict[str, Any]:
        # 1. Parallel Execution
        # In a real sync environment we call them sequentially or use ThreadPool
        room_type = classify_room(image_path)
        detections = detect_property_objects(image_path)
        quality_data = quality_score(image_path)
        tags = generate_tags(image_path)

        # 2. Result Fusion Layer & Feature Extraction
        # Map detected objects to semantic features
        detected_labels = [d["label"] for d in detections]
        features = AutomationPipeline._extract_features(detected_labels, room_type)
        
        # 3. Property Insight Engine
        insights = AutomationPipeline._generate_insights(room_type, detected_labels, features)
        
        return {
            "room_type": room_type,
            "quality_score": quality_data.get("final_quality", 0.0),
            "detections": detected_labels,
            "tags": list(set(tags + features)),
            "insights": insights,
            "verification_status": "Verified" if quality_data.get("final_quality", 0) > 7 else "Needs Improvement"
        }

    @staticmethod
    def _extract_features(objects: List[str], room_type: str) -> List[str]:
        features = []
        mapping = {
            "bed": "bedroom",
            "sofa": "living area",
            "tv": "entertainment ready",
            "sink": "kitchen/washroom",
            "refrigerator": "modular kitchen",
            "dining table": "dining area",
            "bathtub": "luxury bath",
            "toilet": "sanitized washroom"
        }
        for obj in objects:
            if obj in mapping:
                features.append(mapping[obj])
        
        # Room specific features
        if room_type == "kitchen" and "sink" in objects:
            features.append("fully functional kitchen")
        
        return list(set(features))

    @staticmethod
    def _generate_insights(room_type: str, objects: List[str], features: List[str]) -> Dict[str, Any]:
        richness = "Standard"
        if len(objects) > 5: richness = "High-End"
        elif len(objects) > 2: richness = "Moderate"
        
        return {
            "furniture_richness": richness,
            "detected_room": room_type.capitalize(),
            "detected_features": features,
            "smart_home_potential": "Enabled" if "tv" in objects or "refrigerator" in objects else "Unknown"
        }

    @staticmethod
    def _generate_description(room_type: str, objects: List[str], insights: Dict[str, Any]) -> str:
        prompt = f"""
        Generate a short, premium real estate selling description for a {room_type}.
        Detected items: {', '.join(objects)}.
        Key features: {', '.join(insights['detected_features'])}.
        Style: Professional, inviting, and luxury-focused.
        Max 3 sentences.
        """
        try:
            return GroqService.generate_response(prompt, system_message="You are Agam Intelligence, a luxury real estate copywriter.")
        except Exception:
            return f"A beautifully designed {room_type} featuring {', '.join(objects[:3])}. Perfect for modern living."

