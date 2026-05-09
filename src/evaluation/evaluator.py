from common.utils import cosine_similarity

class Evaluator:

    def __init__(self, wiki_graph):
        self.wiki_graph = wiki_graph;

    # Given the list of visited pages (aka the Index,) and the embedded query, calculate the average cosine similarity of each page to the embedded query
    def evaluate(self, visited, query_embedding):
        node_scores = {}
        # for each crawled page
        for title in visited:
            # grab the embedding from wikigraph
            embedding = self.wiki_graph.embeddings.get(title)
            # check embedding is truthy
            if embedding:
                # calc cos sim between candidate and query
                node_scores[title] = cosine_similarity(embedding, query_embedding)
        avg_score = sum(node_scores.values()) / len(node_scores) if node_scores else 0.0
        # return the overall average score, and per-node scores for visualization
        return avg_score, node_scores


