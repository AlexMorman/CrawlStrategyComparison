import config;
import json;
from pathlib import Path

class ResultStore:

    def __init__(self):
        # path to results directory
        self.results_dir = Path(config.RESULTS_DIR)

    def _experiment_dir(self, experiment_id):
        path = self.results_dir / experiment_id
        path.mkdir(parents=True, exist_ok=True)
        return path


    # Serialize the experiment data into a JSON file at data/results/{exp_id}/{topic}.json
    def save(self, experiment_id, topic, results):
        path = self._experiment_dir(experiment_id) / f"{topic}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        print(f"Results saved: {path}")


    # Deserialize the results and load into memory
    def load(self, experiment_id, topic):
        path = self._experiment_dir(experiment_id) / f"{topic}.json"
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)


