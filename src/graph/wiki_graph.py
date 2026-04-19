import json
from pathlib import Path

class WikiGraph:

    def __init__(self):
        # adjacency and abstracts are both loaded from the JSON file during load
        self.adjacency = {};
        self.abstracts = {};
        self.inlink_counts = {}; # article title -> integer count of links pointing to that article
        self.document_lengths = {}
        self.avg_document_length = 0.0
        self.embeddings = {}; # article title -> numpy array of its embedded content
        self.idf = {}; # inverse term frequency (used for BM25)

    # load into memory a serialized sub-graph which was precomputed and saved to the disk at the given filepath
    def load(self, filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.avg_document_length = data["avg_document_length"]
        self.idf = data["idf"]

        for node, content in data["nodes"].items():
            self.adjacency[node] = content["links"]
            self.abstracts[node] = content["abstract"]
            self.inlink_counts[node] = content["inlink_count"]
            self.document_lengths[node] = content["document_length"]

        print("TODO: We would need to load the vector embeddings associated with this wiki graph here!")

        print(f"Sub-graph loaded: {filepath} ({len(self.adjacency):,} nodes present)")
