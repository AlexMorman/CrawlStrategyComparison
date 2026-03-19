from scoring.base_scorer import BaseScorer

class BM25Scorer(BaseScorer):

    def __init__(self):
        pass;

    # Compute the BM25 score of the candidate's abstract against the query
    # Warning: query_embedding is NOT used here. That param is used only for SemanticScoring algorithm
    def score(self, candidate, wiki_graph, query, query_embedding):
        print("TODO");

