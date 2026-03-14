MANDATORY_PIPELINE = {
	"room_classification": "EfficientNet-B0",
	"quality_scoring": "OpenCV",
	"feature_tag_generation": "CLIP",
	"semantic_search": "CLIP",
	"fast_retrieval": "FAISS",
	"cover_image_recommendation": "Rule-based ranking",
	"search_reranking": "Hybrid rule-based scoring",
	"object_detection": "YOLOv8",
}

PATHS = {
	"uploads": "data/uploads",
	"model_classifier": "models/room_classifier_best.pth",
	"faiss_index": "models/image_index.faiss",
	"faiss_ids": "models/image_ids.pkl",
	"predictions_output": "outputs/predictions/pipeline_output.json",
}
