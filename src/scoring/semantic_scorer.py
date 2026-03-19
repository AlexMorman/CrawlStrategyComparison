from scoring.base_scorer import BaseScorer

class SemanticScorer(BaseScorer):

    def __init__(self):
        pass;

    # Uses the cosine similarity between wiki_graph.embeddings[candidate] and query_embedding as a scoring mechanism
    def score(self, candidate, wiki_graph, query, query_embedding):
        print("TODO");
