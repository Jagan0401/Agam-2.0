import torch
import clip
from PIL import Image
import numpy as np

# Standard CLIP loading (Agam default)
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=DEVICE)

def generate_tags(image_path, tags_list=None):
    if not tags_list:
        tags_list = ["sofa", "balcony", "bed", "window", "dining table", "modern kitchen", "wooden floor", "swimming pool"]
    
    image = preprocess(Image.open(image_path)).unsqueeze(0).to(DEVICE)
    text = clip.tokenize(tags_list).to(DEVICE)

    with torch.no_grad():
        image_features = model.encode_image(image)
        text_features = model.encode_text(text)
        similarity = (image_features @ text_features.T).softmax(dim=-1)

    best = similarity[0].topk(min(3, len(tags_list)))
    return [tags_list[i] for i in best.indices]

def generate_embedding(image_path):
    image = preprocess(Image.open(image_path)).unsqueeze(0).to(DEVICE)
    with torch.no_grad():
        embedding = model.encode_image(image)
    return embedding.cpu().numpy()[0]

def encode_text(query):
    text = clip.tokenize([query]).to(DEVICE)
    with torch.no_grad():
        embedding = model.encode_text(text)
    return embedding.cpu().numpy()