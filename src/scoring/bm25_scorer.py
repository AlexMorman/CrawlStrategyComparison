from scoring.base_scorer import BaseScorer
from common.utils import tokenize
import config

class BM25Scorer(BaseScorer):

    # we read the K1 & B values from the config.py
    def __init__(self):
        self.k1 = config.BM25_K1
        self.b = config.BM25_B

    def score(self, candidate, wiki_graph, query, query_embedding):
        tokens = tokenize(wiki_graph.abstracts.get(candidate, ""))
        query_terms = tokenize(query)
        document_length = wiki_graph.document_lengths.get(candidate, 0)
        avg_document_length = wiki_graph.avg_document_length

        score = 0.0
        for term in query_terms:
            # no impact on score if query term is not present in the subgraph's idf
            # this is because each article in subgraph is "equally" lacking that query term
            if term not in wiki_graph.idf:
                continue
            # count the term frequency
            tf = tokens.count(term)
            idf = wiki_graph.idf[term]

            # OK - now we know all of the necessary information to perform BM25
            # Numerator is the tf, scaled by k1+1
            # Denominator is the tf + document length normalized by b & k1
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * (document_length / avg_document_length))

            # Score is "cumulative" in the case that multiple query terms are involved
            score += idf * (numerator / denominator)

        return score
