import pickle
import faiss
from pathlib import Path

try:
    from src.clip_utils import encode_text
except ImportError:
    from clip_utils import encode_text

PROJECT_ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = str(PROJECT_ROOT / "models" / "image_index.faiss")
IDS_PATH = str(PROJECT_ROOT / "models" / "image_ids.pkl")

def load_faiss_assets(index_path=INDEX_PATH, ids_path=IDS_PATH):
    index = faiss.read_index(index_path)
    with open(ids_path, "rb") as f:
        image_paths = pickle.load(f)
    return index, image_paths

def search_images(query, top_k=5, index_path=INDEX_PATH, ids_path=IDS_PATH):
    index, image_paths = load_faiss_assets(index_path=index_path, ids_path=ids_path)
    query_vector = encode_text(query).reshape(1, -1)

    scores, indices = index.search(query_vector, top_k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx == -1:
            continue
        results.append({
            "image_path": image_paths[idx],
            "similarity": float(score)
        })
    return results

if __name__ == "__main__":
    query = "modern kitchen"
    results = search_images(query)
    for r in results:
        print(r)