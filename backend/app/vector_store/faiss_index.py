import faiss
import numpy as np

dimension = 512

index = faiss.IndexFlatL2(dimension)

property_ids = []


def store_vector(vector):

    vector = np.array([vector]).astype("float32")

    index.add(vector)

    property_ids.append(len(property_ids))


def search_vector(query_vector):

    query_vector = np.array(query_vector).astype("float32")

    D, I = index.search(query_vector, 10)

    results = []

    for idx in I[0]:
        if idx < len(property_ids):
            results.append({"property_id": property_ids[idx]})

    return results