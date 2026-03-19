class WikiGraph:

    def __init__(self):
        # adjacency and abstracts are both loaded from the JSON file during load
        self.adjacency = {};
        self.abstracts = {};

        # these 3 fields will be computed by ExperimentRunner by their respective algorithsm
        self.inlink_counts = {}; # article title -> integer count of links pointing to that article
        self.embeddings = {}; # article title -> numpy array of its embedded content
        self.idf = {}; # inverse term frequency (used for BM25)

    # load into memory a serialized sub-graph which was precomputed and saved to the disk at the given filepath
    def load(self, filepath):
        # populate the adjacency and abstracts fields
        print("TODO");
