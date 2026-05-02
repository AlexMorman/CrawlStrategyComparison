from common.utils import cosine_similarity

class Evaluator:

    def __init__(self, wiki_graph):
        self.wiki_graph = wiki_graph;

    # Given the list of visited pages (aka the Index,) and the embedded query, calculate the average cosine similarity of each page to the embedded query
    def evaluate(self, visited, query_embedding):
        scores = []
        # for each crawled page
        for title in visited:
            # grab the embedding from wikigraph
            embedding = self.wiki_graph.embeddings.get(title)
            # check embedding is truthy
            if embedding:
                # calc cos sim between candidate and query
                scores.append(cosine_similarity(embedding, query_embedding))
        if not scores:
            return 0.0
        # return the overall average score :)
        return sum(scores) / len(scores)


