import json
import config
from pathlib import Path
from collections import deque
import math
from common.utils import tokenize
from embedding.embedder import Embedder

class GraphBuilder:

    def __init__(self, links, abstracts):
        # Parsed links dictionary from DBPediaParser
        self.links = links;
        # Parsed abstracts dictionary from DBPediaParser
        self.abstracts = abstracts;
        # how deep do we want to build sub-graph
        self.depth = config.DEPTH;
        # how many nodes are we allowed to fit in graph
        self.max_nodes = config.MAX_NODES
        # where do we save output: path to data/graphs/
        self.output_dir = Path(config.OUTPUT_DIR)
        # embedding model
        self.embedder = Embedder()

    # Breadth-first search from the seed to build out a sub-graph according to the depth & max nodes determined in config file
    def _bfs(self, seed):
        adjacency = {seed: []}

        queue = deque([(seed, 0)])

        while queue:
            node, current_depth = queue.popleft()
            neighbors = self.links.get(node, [])

            for neighbor in neighbors:
                # skip if neighbor not in links
                if neighbor not in self.links:
                    continue

                # record edge if our neighbor is in the subgraph
                if neighbor in adjacency:
                    if neighbor not in adjacency[node]:
                        adjacency[node].append(neighbor)
                    continue

                # check if hit max_nodes
                if len(adjacency) >= self.max_nodes:
                    continue
                # check fi hit max depth
                if current_depth >= self.depth:
                    continue

                # add the neighbor to the subgraph
                adjacency[neighbor] = []
                adjacency[node].append(neighbor)
                queue.append((neighbor, current_depth + 1))

        return adjacency

    # private method to check if a subgraph for given seed has been pre-computed. Check if output_dir/{seed}.json exists
    def _exists(self, seed):
        return (self.output_dir / f"{seed}.json").exists()

    # build the tokenized version of each abstract
    def _tokenize(self, adjacency):
        tokenized = {}
        for node in adjacency:
            abstract = self.abstracts.get(node, "")
            tokenized[node] = tokenize(abstract)

        return tokenized

    # calculates the in-link count of each node in the sub-graph.
    # NOTICE: We are only counting in-links from elements in the subgraph. This gives a distinct advantage to articles closer to the center of the graph
    # For example: if "F16 Fighter Jet" is located 3 jumps away from the seed NASA, it may have a lower in-link count than if it was 1 jump away from seed "US Air Force"
    def _inlink_count(self, adjacency):
        # Start with 0 in each position of inlink_counts array
        inlink_counts = {node: 0 for node in adjacency}
        # For each node, increment the inlink count of each of it's outgoing neighbors
        for node, neighbors in adjacency.items():
            for neighbor in neighbors:
                if neighbor in inlink_counts:
                    inlink_counts[neighbor] += 1
        return inlink_counts


    # calculate the IDF of the sub-graph, according to BM25 specification
    def _inverse_document_frequency(self, adjacency, tokenized):
        # Compute IDF over the total subgraph corpus!
        N = len(adjacency)
        doc_freq = {}
        # for each node in subgraph: grab all tokenized terms and sum their frequencies.
        for node, tokens in tokenized.items():
            for term in set(tokens):
                doc_freq[term] = doc_freq.get(term, 0) + 1
        # Finally, compute IDF of each term according to BM25
        idf = {
            term: math.log((N - df + 0.5) / (df + 0.5))
            for term, df in doc_freq.items()
        }
        return idf;

    # Public method to build sub-graph surrounding the given seed. It will check if we have a pre-saved graph from this seed first
    def build(self, seed):
        # if cache exists: exit
        # else: call _bfs and save
        if self._exists(seed):
            print(f"Graph for the seed ${seed} has already been cached")
            return
        # build adjacency matrix via BFS of the seed
        adjacency = self._bfs(seed)

        # Tokenize the abstracts
        tokenized = self._tokenize(adjacency);
        # Calculate the in-link count and idf of the subgraph
        inlink_counts = self._inlink_count(adjacency)
        idf = self._inverse_document_frequency(adjacency, tokenized)

        # Gather len of each docco and avg docco len - needed for BM25 to normalize over docco len.
        document_lengths = {node: len(tokens) for node, tokens in tokenized.items()}
        # Sum up lengths, and divide by the number of documents
        avg_document_length = sum(document_lengths.values()) / len(document_lengths)

        # Embed the abstracts
        embeddings = self._embed_abstracts(adjacency)

        self._save(seed, adjacency, inlink_counts, idf, document_lengths, avg_document_length, embeddings)

    # Batch-embed all abstracts in adjacency, returns title -> embedding map.
    def _embed_abstracts(self, adjacency):
        titles = list(adjacency.keys())
        abstracts = [self.abstracts.get(title, "") for title in titles]
        embeddings = self.embedder.encode_batch(abstracts)
        return dict(zip(titles, embeddings))

    # saves the sub-graph generated by bfs to outpur_dir/{seed}.json
    def _save(self, seed, adjacency, inlink_counts, idf, document_lengths, avg_document_length, embeddings):
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Construct the JSON format. Seed tells us the root, nodes has each node, it's abstract, links, and in-link count. Finally, we have the idf for the entire corpus.
        output = {
            "seed": seed,
            "avg_document_length": avg_document_length,
            "nodes": {
                node: {
                    "abstract": self.abstracts.get(node, ""),
                    "links": neighbors,
                    "inlink_count": inlink_counts[node],
                    "document_length": document_lengths[node],
                    "embedding": embeddings[node]
                }
                for node, neighbors in adjacency.items()
            },
            "idf": idf
        }

        # write the JSON to file @ output dir
        path = self.output_dir / f"{seed}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(output, f)
        print(f"Sub-graph saved: {path} ({len(adjacency):,} nodes in sub-graph)")

