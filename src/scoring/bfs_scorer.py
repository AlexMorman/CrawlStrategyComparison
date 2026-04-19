from scoring.base_scorer import BaseScorer

class BFSScorer(BaseScorer):
    # Since BFS relies soley on the FIFO nature of the frontier queue, we don't need to score each article
    def score(self, candidate, wiki_graph, query, query_embedding):
        return 0.0
