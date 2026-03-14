import argparse
from pathlib import Path

from ultralytics import YOLO


DEFAULT_DATA_YAML = "data/yolo/dataset.yaml"
DEFAULT_PRETRAINED_MODEL = "yolov8n.pt"
DEFAULT_PROJECT_DIR = "outputs/yolo"


def train_yolo(
    data_yaml: str,
    model_name: str = DEFAULT_PRETRAINED_MODEL,
    epochs: int = 100,
    imgsz: int = 640,
    batch: int = 16,
    project_dir: str = DEFAULT_PROJECT_DIR,
    run_name: str = "roomsense_yolov8",
):
    yaml_path = Path(data_yaml)
    if not yaml_path.exists():
        raise FileNotFoundError(f"Dataset YAML not found: {yaml_path}")

    model = YOLO(model_name)
    results = model.train(
        data=str(yaml_path),
        epochs=epochs,
        imgsz=imgsz,
        batch=batch,
        project=project_dir,
        name=run_name,
    )
    return results


def parse_args():
    parser = argparse.ArgumentParser(description="Train custom YOLOv8 model for RoomSense.")
    parser.add_argument("--data", default=DEFAULT_DATA_YAML, help="Path to YOLO dataset YAML")
    parser.add_argument("--model", default=DEFAULT_PRETRAINED_MODEL, help="Base YOLOv8 model")
    parser.add_argument("--epochs", type=int, default=100, help="Training epochs")
    parser.add_argument("--imgsz", type=int, default=640, help="Input image size")
    parser.add_argument("--batch", type=int, default=16, help="Batch size")
    parser.add_argument("--project", default=DEFAULT_PROJECT_DIR, help="Output directory")
    parser.add_argument("--name", default="roomsense_yolov8", help="Run name")
    return parser.parse_args()


def main():
    args = parse_args()
    train_yolo(
        data_yaml=args.data,
        model_name=args.model,
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        project_dir=args.project,
        run_name=args.name,
    )


if __name__ == "__main__":
    main()
