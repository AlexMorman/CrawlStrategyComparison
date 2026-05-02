from abc import ABC, abstractmethod

# This class contains the abstract scoring logic components which are shared between our 4 algorithms
class BaseScorer(ABC):

    # given a candidate article, score it based on its relevance to the query
    # return float representing the priority of the candidate
    @abstractmethod
    def score(self, candidate, wiki_graph, query, query_embedding):
        pass
