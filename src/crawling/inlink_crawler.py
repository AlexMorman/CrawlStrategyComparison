from crawling.base_crawler import BaseCrawler
from scoring.inlink_scorer import InLinkScorer

class InLinkCrawler(BaseCrawler):
    def __init__(self):
        super().__init__(InLinkScorer());

