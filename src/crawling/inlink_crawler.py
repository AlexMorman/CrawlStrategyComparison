import heapq
from crawling.base_crawler import BaseCrawler
from scoring.inlink_scorer import InlinkScorer

# Crawler for the in-link count strategy
# Raw in-link count, which is computed during the pre-processing step is used as a score, with no normalization factor applied
class InlinkCrawler(BaseCrawler):

    def __init__(self):
        super().__init__(InlinkScorer())

    def _init_frontier(self):
        self.frontier = []

    def _push(self, node, score):
        # Note: we invert score because we are using a minheap
        heapq.heappush(self.frontier, (-score, node))

    def _pop(self):
        return heapq.heappop(self.frontier)[1]

    def _is_empty(self):
        return len(self.frontier) == 0
