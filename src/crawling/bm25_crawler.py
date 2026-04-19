import heapq
from crawling.base_crawler import BaseCrawler
from scoring.bm25_scorer import BM25Scorer

# We use the standard BM25 specification to crawl thru the articles
# K1 & B params can be configured in config.property
class BM25Crawler(BaseCrawler):

    def __init__(self):
        super().__init__(BM25Scorer())

    def _init_frontier(self):
        self.frontier = []

    def _push(self, node, score):
        # Note: we invert score because we are using a minheap
        heapq.heappush(self.frontier, (-score, node))

    def _pop(self):
        return heapq.heappop(self.frontier)[1]

    def _is_empty(self):
        return len(self.frontier) == 0
