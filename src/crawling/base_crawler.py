import heapq;

# this class contains the shared logic used across each of the 4 algorithms
class BaseCrawler:

    def __init__(self, scorer):
        self.scorer = scorer;

    # main crawl loop. Manages the visited set, score neighbors, decrement budget, and finally return an ordered list of the visited article titles.
    def run(self, seed, budget, wiki_graph, query, query_embedding):
        print("TODO");

