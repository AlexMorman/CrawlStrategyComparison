from crawling.base_crawler import BaseCrawler
from scoring.bfs_scorer import BFSScorer

class BFSCrawler(BaseCrawler):
    def __init__(self):
        super().__init__(BFSScorer());
