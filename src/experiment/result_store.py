import config;
import json;
from pathlib import Path

class ResultStore:

    def __init__(self):
        # path to results directory
        self.results_dir = Path(config.RESULTS_DIR)

    # Serialize the experiment data into a JSON file at data/results/{exp_id}/{topic}.json
    def save(self, experiment_id, topic, results):
        self.results_dir.mkdir(parents=True, exist_ok=True)
        path = self.results_dir / f"{experiment_id}_{topic}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        print(f"Results saved: {path}")


    # Deserialize the results and load into memory
    def load(self, experiment_id, topic):
        path = self.results_dir / f"{experiment_id}_{topic}.json"
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

