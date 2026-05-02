import config;
import json;
from graph.wiki_graph import WikiGraph
from embedding.embedder import Embedder
from evaluation.evaluator import Evaluator
from experiment.result_store import ResultStore
from crawling.bfs_crawler import BFSCrawler
from crawling.inlink_crawler import InlinkCrawler
from crawling.bm25_crawler import BM25Crawler
from crawling.semantic_crawler import SemanticCrawler
from datetime import datetime
from pathlib import Path

class ExperimentRunner:

    def __init__(self):
        self.topics = [];
        self.budget = config.BUDGET;
        self.embedder = Embedder();
        self.result_store = ResultStore();
        self.experiment_id = None;

    # Main execution of the overall experiment. loop thru all topics, and and call _run_topic() on each of them
    def run(self):
        # grab datetime to use as experiment ID
        self.experiment_id = datetime.now().strftime("%Y%m%d_%H%M%S")

        # load topics
        with open(config.TOPICS_PATH, "r", encoding="utf-8") as f:
            self.topics = json.load(f)

        print(f"Running experiment over {len(self.topics)} topics")
        for i, topic in enumerate(self.topics, 1):
            print(f"Topic {i}/{len(self.topics)}: {topic}")
            self._run_topic(topic)
        print("Experiment complete.")


    # For one given topic, do the following: 
    # Precompute tasks, load WikiGraph, instantiate the 4 Crawlers, run each of the crawlers, and finally store results via ResultStore
    def _run_topic(self, topic):
        # De-deserialize the preprocessed subgraph for given topic
        graph_path = Path(config.OUTPUT_DIR) / f"{topic}.json"
        wiki_graph = WikiGraph()
        wiki_graph.load(str(graph_path))

        # we use the topic as our target. it is the only embedding we do at run-time
        query = topic
        query_embedding = self.embedder.encode(query)

        # Assemble 4 crawlers
        crawlers = {
            "bfs":      BFSCrawler(),
            "inlink":   InlinkCrawler(),
            "bm25":     BM25Crawler(),
            "semantic": SemanticCrawler(),
        }

        evaluator = Evaluator(wiki_graph)
        results = {}
        # run each crawler over the topics' subgraph
        for strategy, crawler in crawlers.items():
            print(f"  Crawling with {strategy}")
            # Because each crawler is a BaseCrawler, we can just use crawler.run and it works for all cases
            visited = crawler.run(topic, self.budget, wiki_graph, query, query_embedding)
            # Use evaluator to determine the overall score of the crawler
            score = evaluator.evaluate(visited, query_embedding)
            results[strategy] = {"visited": visited, "score": score}

        self.result_store.save(self.experiment_id, topic, results)



