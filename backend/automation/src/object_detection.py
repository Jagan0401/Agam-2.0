from pathlib import Path

from ultralytics import YOLO


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CUSTOM_MODEL_PATH = str(PROJECT_ROOT / "outputs" / "yolo" / "roomsense_yolov8" / "weights" / "best.pt")
FALLBACK_MODEL_NAME = "yolov8n.pt"
_YOLO_MODEL = None


def _resolve_model_name(model_name: str = ""):
    if model_name:
        return model_name

    custom_path = Path(CUSTOM_MODEL_PATH)
    if custom_path.exists():
        return str(custom_path)

    return FALLBACK_MODEL_NAME


def load_detector(model_name: str = ""):
    global _YOLO_MODEL
    if _YOLO_MODEL is None:
        _YOLO_MODEL = YOLO(_resolve_model_name(model_name))
    return _YOLO_MODEL


def detect_objects(image_path: str, conf: float = 0.25):
    model = load_detector()
    results = model.predict(image_path, conf=conf, verbose=False)
    detections = []

    for result in results:
        for box in result.boxes:
            class_id = int(box.cls.item())
            score = float(box.conf.item())
            label = result.names[class_id]
            detections.append({
                "label": label,
                "confidence": round(score, 4),
            })

    return detections


if __name__ == "__main__":
    print(detect_objects("data/test_sample.jpg"))
