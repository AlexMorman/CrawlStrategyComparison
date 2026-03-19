import config;

# This class is a wrapper for the embedding model. We want the class to be model-agnostic, so that we can plug-and-play different models to tweak results
class Embedder:

    def __init__(self):
        self.model = config.EMBEDDING_MODEL;

    # return the embedding of a single text
    def encode(self, text):
        return "TODO";

    # return an array of the embeddings of multiple texts
    def encode_batch(self, texts):
        return "TODO";
