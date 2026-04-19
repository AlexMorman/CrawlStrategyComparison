from collections import deque
from crawling.base_crawler import BaseCrawler
from scoring.bfs_scorer import BFSScorer

# For BFS, we simply use the neighbors to populate the frontier
# Frontier is accessed with a simple FIFO policy
# No scoring is necessary. The BFSScorer class returns 0 always, providing no special priority to an article
class BFSCrawler(BaseCrawler):

    def __init__(self):
        super().__init__(BFSScorer())

    def _init_frontier(self):
        self.frontier = deque()

    def _push(self, node, score):
        self.frontier.append(node)

    def _pop(self):
        return self.frontier.popleft()

    def _is_empty(self):
        return len(self.frontier) == 0
