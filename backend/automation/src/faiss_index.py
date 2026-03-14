import os
import pickle
import faiss
import numpy as np
from pathlib import Path

try:
    from src.clip_utils import encode_image
except ImportError:
    from clip_utils import encode_image

PROJECT_ROOT = Path(__file__).resolve().parents[1]
IMAGE_FOLDER = str(PROJECT_ROOT / "data" / "uploads")
INDEX_PATH = str(PROJECT_ROOT / "models" / "image_index.faiss")
IDS_PATH = str(PROJECT_ROOT / "models" / "image_ids.pkl")

def build_faiss_index(image_folder=IMAGE_FOLDER, index_path=INDEX_PATH, ids_path=IDS_PATH):
    image_paths = []
    embeddings = []

    for file_name in os.listdir(image_folder):
        if file_name.lower().endswith((".jpg", ".jpeg", ".png")):
            path = os.path.join(image_folder, file_name)
            emb = encode_image(path)
            image_paths.append(path)
            embeddings.append(emb)

    if not embeddings:
        raise ValueError(f"No images found in: {image_folder}")

    embeddings = np.array(embeddings, dtype="float32")

    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, index_path)
    with open(ids_path, "wb") as f:
        pickle.dump(image_paths, f)

    return {
        "indexed_images": len(image_paths),
        "index_path": index_path,
        "ids_path": ids_path,
    }

if __name__ == "__main__":
    result = build_faiss_index()
    print("FAISS index built successfully.")
    print("Indexed images:", result["indexed_images"])