from scipy.spatial.distance import cosine

class Evaluator:

    def __init__(self, wiki_graph):
        self.wiki_graph = wiki_graph;

    # Given the list of visited pages (aka the Index,) and the embedded query, calculate the average cosine similarity of each page to the embedded query
    def evaluate(self, visited, query_embedding):
        print("TODO");

