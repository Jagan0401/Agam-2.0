from pathlib import Path

try:
	from src.clip_utils import generate_tags
except ImportError:
	from clip_utils import generate_tags


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def generate_image_tags(image_path: str, top_k: int = 3):
    return generate_tags(image_path=image_path, top_k=top_k)


if __name__ == "__main__":
    print(generate_image_tags(str(PROJECT_ROOT / "data" / "test_sample.jpg")))
