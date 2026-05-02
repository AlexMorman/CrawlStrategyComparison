import re
import numpy as np

# simple regex to grab each individual word/token
# at time of creation, it is used in 2 places (graph_builder for idf calc & bm25 implementation for tf calc)
# ex: abstract of "Alex hates Regular Expressions" would be processed as ["Alex", "hates", "Regular", "Expressions"]
def tokenize(text):
    return re.findall(r'\b\w+\b', text.lower())

# calc cosine similarity between two vectors
def cosine_similarity(a, b):
    a, b = np.array(a), np.array(b)
    denominator = np.linalg.norm(a) * np.linalg.norm(b)
    if denominator == 0:
        return 0.0
    return float(np.dot(a, b) / denominator)
