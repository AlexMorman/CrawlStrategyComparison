from crawling.base_crawler import BaseCrawler
from scoring.bm25_scorer import BM25Scorer

class BM25Crawler(BaseCrawler):
    def __init__(self):
        super().__init__(BM25Scorer());

