import config;
import json;

class ResultStore:

    def __init__(self):
        # path to results directory
        self.results_dir = config.RESULTS_DIR;

    # Serialize the experiment data into a JSON file at data/results/{exp_id}.json
    def save(self, experiment_id, results):
        print("TODO");

    # Deserialize the results and load into memory
    def load(self, experiment_id):
        print("TODO")
