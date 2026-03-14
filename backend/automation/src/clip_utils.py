import torch
import clip
from PIL import Image
from typing import Dict, List
import numpy as np

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=DEVICE)

# -----------------------------
# Prompt groups
# -----------------------------
STYLE_PROMPTS = [
    "a modern interior",
    "a luxury interior",
    "a minimalist interior",
    "a traditional interior",
    "a contemporary interior",
]

ATTRIBUTE_PROMPTS = [
    "a bright room",
    "a dark room",
    "a clean room",
    "a cluttered room",
    "a spacious room",
    "a compact room",
    "a furnished room",
    "an unfurnished room",
    "a well-lit room",
]

ROOM_SPECIFIC_PROMPTS = [
    "a modern bedroom",
    "a luxury bedroom",
    "a minimalist bedroom",

    "a modern kitchen",
    "a luxury kitchen",
    "a modular kitchen",
    "a minimalist kitchen",

    "a modern bathroom",
    "a luxury bathroom",
    "a clean bathroom",

    "a modern living room",
    "a luxury living room",
    "a spacious living room",
    "a minimalist living room",

    "a stylish balcony",
    "a balcony with open view",

    "a modern house exterior",
    "a luxury house exterior",
]

ALL_PROMPTS = STYLE_PROMPTS + ATTRIBUTE_PROMPTS + ROOM_SPECIFIC_PROMPTS


# -----------------------------
# Helper functions
# -----------------------------
def _encode_image(image_path: str) -> torch.Tensor:
    image = preprocess(Image.open(image_path).convert("RGB")).unsqueeze(0).to(DEVICE)
    with torch.no_grad():
        image_features = model.encode_image(image)
        image_features /= image_features.norm(dim=-1, keepdim=True)
    return image_features


def _encode_text(prompts: List[str]) -> torch.Tensor:
    text_tokens = clip.tokenize(prompts).to(DEVICE)
    with torch.no_grad():
        text_features = model.encode_text(text_tokens)
        text_features /= text_features.norm(dim=-1, keepdim=True)
    return text_features


def encode_image(image_path: str) -> np.ndarray:
    image_features = _encode_image(image_path)
    return image_features.squeeze(0).cpu().numpy().astype("float32")


def encode_text(query: str) -> np.ndarray:
    text_features = _encode_text([query])
    return text_features.squeeze(0).cpu().numpy().astype("float32")


def generate_tags(image_path: str, top_k: int = 3) -> List[str]:
    result = generate_semantic_tags(image_path=image_path, top_k=top_k)
    return result["semantic_tags"]


def _get_similarity_scores(image_features: torch.Tensor, prompts: List[str]) -> Dict[str, float]:
    text_features = _encode_text(prompts)
    with torch.no_grad():
        similarities = (image_features @ text_features.T).squeeze(0)

    scores = {}
    for prompt, score in zip(prompts, similarities.tolist()):
        scores[prompt] = float(score)
    return scores


def _top_k_from_scores(score_dict: Dict[str, float], k: int = 3) -> List[str]:
    sorted_items = sorted(score_dict.items(), key=lambda x: x[1], reverse=True)
    return [item[0] for item in sorted_items[:k]]


def _clean_label(prompt: str) -> str:
    prompt = prompt.lower().strip()
    replacements = {
        "a ": "",
        "an ": "",
        "room": "",
        "interior": "",
        "house": "",
    }
    for old, new in replacements.items():
        prompt = prompt.replace(old, new)

    prompt = " ".join(prompt.split())
    return prompt


# -----------------------------
# Main API
# -----------------------------
def classify_style(image_path: str) -> Dict:
    image_features = _encode_image(image_path)
    style_scores = _get_similarity_scores(image_features, STYLE_PROMPTS)

    best_prompt = max(style_scores, key=style_scores.get)
    return {
        "style": _clean_label(best_prompt),
        "style_prompt": best_prompt,
        "style_score": round(style_scores[best_prompt], 4),
        "all_style_scores": {k: round(v, 4) for k, v in style_scores.items()},
    }


def classify_attributes(image_path: str, top_k: int = 3) -> Dict:
    image_features = _encode_image(image_path)
    attribute_scores = _get_similarity_scores(image_features, ATTRIBUTE_PROMPTS)

    top_prompts = _top_k_from_scores(attribute_scores, k=top_k)
    top_attributes = [_clean_label(p) for p in top_prompts]

    return {
        "attributes": top_attributes,
        "attribute_prompts": top_prompts,
        "all_attribute_scores": {k: round(v, 4) for k, v in attribute_scores.items()},
    }


def generate_semantic_tags(image_path: str, top_k: int = 5) -> Dict:
    image_features = _encode_image(image_path)
    semantic_scores = _get_similarity_scores(image_features, ROOM_SPECIFIC_PROMPTS)

    top_prompts = _top_k_from_scores(semantic_scores, k=top_k)
    tags = [_clean_label(p) for p in top_prompts]

    return {
        "semantic_tags": tags,
        "semantic_prompts": top_prompts,
        "all_semantic_scores": {k: round(v, 4) for k, v in semantic_scores.items()},
    }


def analyze_image_with_clip(image_path: str, attr_top_k: int = 3, tag_top_k: int = 5) -> Dict:
    """
    Main function for your pipeline.
    Returns style, attributes, and semantic tags separately.
    """
    style_result = classify_style(image_path)
    attribute_result = classify_attributes(image_path, top_k=attr_top_k)
    semantic_result = generate_semantic_tags(image_path, top_k=tag_top_k)

    return {
        "style": style_result["style"],
        "style_score": style_result["style_score"],
        "attributes": attribute_result["attributes"],
        "semantic_tags": semantic_result["semantic_tags"],
        "debug": {
            "style_scores": style_result["all_style_scores"],
            "attribute_scores": attribute_result["all_attribute_scores"],
            "semantic_scores": semantic_result["all_semantic_scores"],
        }
    }


# -----------------------------
# Example usage
# -----------------------------
if __name__ == "__main__":
    image_path = "data/test_sample.jpg"

    result = analyze_image_with_clip(image_path)

    print("\nCLIP Analysis Result")
    print("-" * 40)
    print("Style:", result["style"])
    print("Style Score:", result["style_score"])
    print("Attributes:", result["attributes"])
    print("Semantic Tags:", result["semantic_tags"])

    print("\nDebug Scores")
    print("-" * 40)
    print("Style Scores:", result["debug"]["style_scores"])
    print("Attribute Scores:", result["debug"]["attribute_scores"])
    print("Semantic Scores:", result["debug"]["semantic_scores"])