from scoring.base_scorer import BaseScorer

class BFSScorer(BaseScorer):

    def __init__(self):
        self.counter = 0;

    # for BFS, we invert the current counter as our score, and then increment the counter
    def score(self, candidate, wiki_graph, query, query_embedding):
        print("TODO");

