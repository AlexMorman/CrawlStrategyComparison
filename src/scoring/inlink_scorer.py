# inlink_scorer.py
from scoring.base_scorer import BaseScorer

class InlinkScorer(BaseScorer):

    # Simply return the raw in-link count as a score. no sophisticated calculation is required!
    def score(self, candidate, wiki_graph, query, query_embedding):
        return wiki_graph.inlink_counts.get(candidate, 0)
