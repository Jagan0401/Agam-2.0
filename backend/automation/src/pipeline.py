import json
import os
from pathlib import Path

try:
    from src.clip_utils import generate_tags
    from src.faiss_index import build_faiss_index
    from src.object_detection import detect_objects
    from src.predict_room import predict_room
    from src.quality_score import final_quality_score
    from src.ranking import rank_listing_images, rerank_search_results, select_cover_image
    from src.semantic_search import search_images
except ImportError:
    from clip_utils import generate_tags
    from faiss_index import build_faiss_index
    from object_detection import detect_objects
    from predict_room import predict_room
    from quality_score import final_quality_score
    from ranking import rank_listing_images, rerank_search_results, select_cover_image
    from semantic_search import search_images


PROJECT_ROOT = Path(__file__).resolve().parents[1]
UPLOADS_DIR = str(PROJECT_ROOT / "data" / "uploads")
OUTPUT_DIR = str(PROJECT_ROOT / "outputs" / "predictions")
OUTPUT_FILE = "pipeline_output.json"


def analyze_single_image(image_path: str):
    room_result = predict_room(image_path)
    quality_result = final_quality_score(image_path)
    tags = generate_tags(image_path, top_k=3)
    detections = detect_objects(image_path)

    return {
        "filename": os.path.basename(image_path),
        "image_path": image_path,
        "room_type": room_result["room_type"],
        "confidence": room_result["confidence"],
        "quality_score": quality_result["final_quality"],
        "quality_metrics": quality_result,
        "tags": tags,
        "objects": detections,
    }


def run_pipeline(upload_dir: str = UPLOADS_DIR, query: str = "modern kitchen", top_k: int = 5):
    image_paths = [
        str(path)
        for path in Path(upload_dir).glob("*")
        if path.suffix.lower() in {".jpg", ".jpeg", ".png"}
    ]

    if not image_paths:
        raise ValueError(f"No images found in {upload_dir}")

    analyzed_images = [analyze_single_image(path) for path in image_paths]

    build_info = build_faiss_index(image_folder=upload_dir)
    semantic_results = search_images(query=query, top_k=top_k)

    path_to_analysis = {item["image_path"]: item for item in analyzed_images}
    enriched_search = []
    for result in semantic_results:
        meta = path_to_analysis.get(result["image_path"], {})
        enriched_search.append({
            **result,
            "filename": meta.get("filename"),
            "room_type": meta.get("room_type", ""),
            "quality_score": meta.get("quality_score", 0.0),
            "tags": meta.get("tags", []),
        })

    reranked_search = rerank_search_results(enriched_search, query=query)
    ranked_listing = rank_listing_images(analyzed_images)
    cover_image = select_cover_image(analyzed_images)

    output = {
        "pipeline": {
            "room_classification": "EfficientNet-B0",
            "quality_scoring": "OpenCV",
            "feature_tag_generation": "CLIP",
            "semantic_search": "CLIP",
            "fast_retrieval": "FAISS",
            "cover_recommendation": "Rule-based ranking",
            "search_reranking": "Hybrid rule-based scoring",
            "object_detection": "YOLOv8",
        },
        "build_info": build_info,
        "query": query,
        "cover_image": cover_image,
        "listing_ranked": ranked_listing,
        "search_results": reranked_search,
    }

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    return output, output_path


if __name__ == "__main__":
    data, path = run_pipeline()
    print(f"Pipeline completed. Output saved to: {path}")
    print(f"Recommended cover: {data['cover_image']['filename'] if data.get('cover_image') else 'N/A'}")
