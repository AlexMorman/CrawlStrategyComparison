import config;

class TopicLoader:

    def __init__(self):
        # Number of topics to include in experiment, defined in config
        self.n = config.NUMBER_OF_TOPICS;
        # Where to save the topics; data/topics.JSON
        self.output_path = config.TOPICS_PATH;

    # public method, fetch Wikipedia's pageview API, and save the top N topics to the topics.JSON file
    def fetch(self):
        print("TODO");

    # save the given topics to the topics.JSON file
    def _save(self, topics):
        print("TODO");

