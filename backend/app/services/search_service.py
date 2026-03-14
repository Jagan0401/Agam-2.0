from app.services.room_classifier import classify_room
from app.services.clip_service import generate_tags, generate_embedding, encode_text
from app.services.quality_service import quality_score
from app.services.object_detection import detect_property_objects
from app.vector_store.faiss_index import store_vector, search_vector

from app.services.automation_pipeline import AutomationPipeline

def analyze_image(image_path: str):
    """
    Unified analysis pipeline combining all Agam AI models with fusion logic.
    """
    pipeline_result = AutomationPipeline.analyze_image(image_path)
    
    # Maintain compatibility with previous schema if needed, but return enriched data
    return pipeline_result

def search_properties_semantic(query: str):
    """Semantic search using CLIP embeddings and FAISS retrieval."""
    query_vector = encode_text(query)
    results = search_vector(query_vector)
    return results # Note: These are IDs, would need DB join in real usage