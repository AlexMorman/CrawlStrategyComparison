import heapq
from crawling.base_crawler import BaseCrawler
from scoring.semantic_scorer import SemanticScorer

# This crawler uses the custom-defined Semantic-focused crawling technique
# We vector-embed the abstract text and use the cosine-similarity to the embedded query as a scoring method
class SemanticCrawler(BaseCrawler):

    def __init__(self):
        super().__init__(SemanticScorer())

    def _init_frontier(self):
        self.frontier = []

    def _push(self, node, score):
        # Note: we invert score because we are using a minheap
        heapq.heappush(self.frontier, (-score, node))

    def _pop(self):
        return heapq.heappop(self.frontier)[1]
