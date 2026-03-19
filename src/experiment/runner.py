import config;
import json;
from graph.wiki_graph import WikiGraph
from embedding.embedder import Embedder
from evaluation.evaluator import Evaluator
from experiment.result_store import ResultStore
from crawling.bfs_crawler import BFSCrawler
from crawling.inlink_crawler import InLinkCrawler
from crawling.bm25_crawler import BM25Crawler
from crawling.semantic_crawler import SemanticCrawler

class ExperimentRunner:

    def __init__(self):
        self.topics = [];
        self.budget = config.BUDGET;
        self.embedder = Embedder();
        self.result_store = ResultStore();

    # Main execution of the overall experiment. loop thru all topics, and and call _run_topic() on each of them
    def run(self):
        print("TODO");

    # For one given topic, do the following: 
    # Precompute tasks, load WikiGraph, instantiate the 4 Crawlers, run each of the crawlers, and finally store results via ResultStore
    def _run_topic(self, topic):
        print("TODO");

    # Runs the precompute routine associated with a wiki_graph and query
    def _precompute(self, wiki_graph, query):
        print("TODO");

