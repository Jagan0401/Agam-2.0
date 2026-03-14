import torch
import torch.nn as nn
from PIL import Image
from torchvision import models, transforms
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = str(PROJECT_ROOT / "models" / "room_classifier_best.pth")
IMG_SIZE = 224
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

_MODEL = None
_CLASS_NAMES = None


def _get_transform(img_size: int = IMG_SIZE):
    return transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])


def load_room_classifier(model_path: str = MODEL_PATH, device: str = DEVICE):
    checkpoint = torch.load(model_path, map_location=device)
    class_names = checkpoint["class_names"]
    num_classes = len(class_names)

    model = models.efficientnet_b0(weights=None)
    in_features = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(in_features, num_classes)
    model.load_state_dict(checkpoint["model_state_dict"])
    model = model.to(device)
    model.eval()
    return model, class_names


def predict_room(image_path: str, model_path: str = MODEL_PATH, device: str = DEVICE):
    global _MODEL, _CLASS_NAMES

    if _MODEL is None or _CLASS_NAMES is None:
        _MODEL, _CLASS_NAMES = load_room_classifier(model_path=model_path, device=device)

    image = Image.open(image_path).convert("RGB")
    image_tensor = _get_transform()(image).unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = _MODEL(image_tensor)
        probs = torch.softmax(outputs, dim=1)
        pred_idx = torch.argmax(probs, dim=1).item()
        confidence = probs[0][pred_idx].item()

    return {
        "room_type": _CLASS_NAMES[pred_idx],
        "confidence": round(confidence, 4),
    }


if __name__ == "__main__":
    result = predict_room(str(PROJECT_ROOT / "data" / "test_sample.jpg"))
    print("Predicted Room:", result["room_type"])
    print("Confidence:", result["confidence"])