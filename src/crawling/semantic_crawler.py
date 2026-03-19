from crawling.base_crawler import BaseCrawler
from scoring.semantic_scorer import SemanticScorer

class SemanticCrawler(BaseCrawler):
    def __init__(self):
        super().__init__(SemanticScorer());

