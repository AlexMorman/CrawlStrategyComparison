from preprocessing.dbpedia_parser import DBPediaParser;
from preprocessing.topic_loader import TopicLoader;
from preprocessing.graph_builder import GraphBuilder;
import config;
import json;

# Routine for all pre-processing work
# Instantiate & run DBpediaParser on the 3 files
# Instantiate & run TopicLoader to get top N wikipedia topics
# For each topic: instantiate & run GraphBuilder to build out the sub-graphs
def main():
    # First, parse DBPedia files
    parser = DBPediaParser()
    parser.parse_redirects(config.REDIRECTS_PATH)
    parser.parse_abstracts(config.ABSTRACTS_PATH)
    parser.parse_links(config.LINKS_PATH)

    # Next, choose our random seed article topics
    loader = TopicLoader(parser.abstracts)
    topics = loader.fetch(seed=42)
    print(f"Topics selected: {topics}")

    # Finally, build out a subgraph for each topic
    builder = GraphBuilder(parser.links, parser.abstracts)
    for i, topic in enumerate(topics, 1):
        print(f"Building subgraph {i} of {len(topics)} for topic: {topic}")
        builder.build(topic);


if __name__ == "__main__":
    main();
