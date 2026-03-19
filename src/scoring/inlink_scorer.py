from scoring.base_scorer import BaseScorer

class InLinkScorer(BaseScorer):

    def __init__(self):
        pass;

    def score(self, candidate, wiki_graph, query, query_embedding):
        return wiki_graph.inlink_counts[candidate];
