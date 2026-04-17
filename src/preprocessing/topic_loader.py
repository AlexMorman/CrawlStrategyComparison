import config;
import random;
import json;
from pathlib import Path

class TopicLoader:

    def __init__(self, abstracts):
        # Number of topics to include in experiment, defined in config
        self.n = config.NUMBER_OF_TOPICS;
        # Where to save the topics; data/topics.JSON
        self.output_path = Path(config.TOPICS_PATH);
        # abstracts from which the random topics will be selected
        self.abstracts = abstracts

    # fetch the randomly selected topics. Use seed=42 for reproducibility
    def fetch(self, seed=42):
        random.seed(seed)
        topics = random.sample(list(self.abstracts.keys()), self.n)
        self._save(topics)
        return topics

    # save the given topics to the topics.JSON file
    def _save(self, topics):
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.output_path, "w", encoding="utf-8") as f:
            json.dump(topics, f, indent=2)
        print(f"Topics saved: {self.output_path} ({len(topics)} topics)")
