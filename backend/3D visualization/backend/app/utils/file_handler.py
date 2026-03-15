import os
from pathlib import Path
from PIL import Image
from app.config import IMAGES_DIR, ALLOWED_EXTENSIONS

def get_image_path(room_type: str) -> str:
    """Get the file path for a room type image."""
    return f"/{IMAGES_DIR}/{room_type}.jpg"

def validate_image_file(filename: str) -> bool:
    """Validate if the file is an allowed image type."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_image(file, filename: str) -> str:
    """Save an uploaded image file."""
    images_path = Path(__file__).parent.parent / IMAGES_DIR
    images_path.mkdir(exist_ok=True)

    file_path = images_path / filename
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    return str(file_path)

def get_room_images() -> dict:
    """Get all room images for the virtual tour."""
    images = {}
    for room in ["living_room", "bedroom", "kitchen", "bathroom"]:
        images[room] = get_image_path(room)
    return images