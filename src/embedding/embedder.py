from sentence_transformers import SentenceTransformer
import config
import torch

# This class is a wrapper for the embedding model. We want the class to be model-agnostic, so that we can plug-and-play different models to tweak results
class Embedder:

    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.batch_size = batch_size=config.EMBEDDING_BATCH_SIZE
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2', device=self.device)

    # encode serially
    def encode(self, text):
        return self.model.encode(text, convert_to_numpy=True).tolist()

    # encode in parallel
    def encode_batch(self, texts):
        embeddings = self.model.encode(texts, convert_to_numpy=True, batch_size=self.batch_size, show_progress_bar=True)
        return [e.tolist() for e in embeddings]
