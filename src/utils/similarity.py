from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")


def semantic_similarity(a, b):
    emb1 = model.encode([a])
    emb2 = model.encode([b])

    score = cosine_similarity(emb1, emb2)[0][0]
    return float(score)


def are_similar(a, b, threshold=0.80):
    return semantic_similarity(a, b) >= threshold