import heapq;

# this class contains the shared logic used across each of the 4 strategies
class BaseCrawler:

    def __init__(self, scorer):
        self.scorer = scorer;

    # main crawl loop
    # manages the visited set, scores neighbors, decrements budget, and finally return a list of the visited article titles - in order of the strategy's score!
    def run(self, seed, budget, wiki_graph, query, query_embedding):
        visited = []
        seen = set()

        self._init_frontier()

        # Score according to my strategy, and push seed to frontier.
        # Note that each of the strategy_crawler classes (ex: bfs_crawler, inlink_crawler, etc.) has a corresponding
        # scoring class (ex: bfs_scorer, inlink_scorer) assigned to it. This class is agnostic of that strategy, and the
        # same procedure is followed in all cases!
        seed_score = self.scorer.score(seed, wiki_graph, query, query_embedding)
        self._push(seed, seed_score)
        seen.add(seed)

        # While we still have budget for more crawling
        while len(visited) < budget:
            # Stop if frontier is exhausted - this should theoretically never happen, unless budget is larger than the subgraph
            # That would likely only happen if we happened to use a seed which was isolated from the main network of wikipedia articles
            # It's local network would need to be smaller than the budget (ex: 10 connected articles which are isolated, with a crawl budget of 1,000)
            # I am not sure if that even exists, but we might as well be careful!
            # Also, if the user for some reason gave bad config, where budget is bigger than max # articles, this could trigger
            if self._is_empty():
                break

            # Visit the node with the best score in the frontier
            # Note: this will include the seed article on the first run through in all cases!
            node = self._pop()
            visited.append(node)

            # Grab all out-going links from the recently visited node
            for neighbor in wiki_graph.adjacency.get(node, []):
                # If we have not seen that link before,
                if neighbor not in seen:
                    # Score it (agnostic to my strategy)
                    score = self.scorer.score(neighbor, wiki_graph, query, query_embedding)
                    # Add it to heap, and mark it as "seen"
                    self._push(neighbor, score)
                    seen.add(neighbor)

        return visited

    def _is_empty(self):
        return len(self.frontier) == 0

    # Each of these 3 functions is due to be implemented by each of the individual crawlers
    # Each strategy has a different way of handling these operations!
    # The main reason this is necessary is because bfs uses a queue, while the other strategies use minheap

    def _init_frontier(self):
        raise NotImplementedError

    def _push(self, node, score):
        raise NotImplementedError

    def _pop(self):
        raise NotImplementedError


