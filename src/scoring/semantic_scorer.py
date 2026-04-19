from scoring.base_scorer import BaseScorer

class SemanticScorer(BaseScorer):
    def score(self, candidate, wiki_graph, query, query_embedding):
        # TODO: calc cos similarity between candidate's vector embedding and query_embedding
        # dependent on the embedding model wrapper class :)
        print("TODO: We calculate the cosine similarity between candidate and query's embeddings")
