from scoring.base_scorer import BaseScorer
from common.utils import cosine_similarity

class SemanticScorer(BaseScorer):
    def score(self, candidate, wiki_graph, query, query_embedding):
        # calc cos similarity between candidate's vector embedding and query_embedding
        candidate_embedding = wiki_graph.embeddings.get(candidate)
        if candidate_embedding is None:
            return 0.0
        return cosine_similarity(candidate_embedding, query_embedding)

