##Semantic-Focused Crawler - Strategy Comarison Experiment Usage##

**Step 1: Prepare dataset from DBPedia**

* The pre-processing module requires the wikilinks, short-abstracts, and redirects data from DBPedia
  
```
https://databus.dbpedia.org/dbpedia/generic/wikilinks/2022.12.01
https://databus.dbpedia.org/dbpedia/text/short-abstracts/2022.12.01
https://databus.dbpedia.org/dbpedia/generic/redirects/2022.12.01
```

* Download the .ttl.bz2 files for english langauge.
* In theory it should work with other languages, although it is untested at this time.
* The 3 components should be saved to the data/raw directory

**Step 2: Configuration**

* Check the src/config.py file to edit any desired parameters.
* You can configure the paths for data I/O.
* You can also configure the sub-graph shape and size
* On the experiment's end you can decide how many topics should be assessed, as well as set a crawl budget
* You can also adjust the BM25 tuning parameters, if desired.

* Topic selection is done via the data/topics.json file
* If the file is empty, the preprocessing pipeline will randomly select NUMBER_OF_TOPICS seed articles
* If you want to target specific articles, you may do so.
* NOTE: Article titles must be exact text matches. Also, keep in mind that the dataset is a snapshot in the past.
* This means some currently available wikipedia articles do not exist yet, or may have had their name changed at some point.

**Step 3: Environment**

* The project was built with Python 3.14.4
* The following depedencies must be installed via package manager of choice

```
matplotlib==3.10.9
numpy==2.4.4
sentence_transformers==5.4.1
torch==2.11.0
```

* More information about the embedding model used can be found here
https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2

**Step 4: Usage**

* First, you must run preprocess.py to assemble subgraphs. This step lasted around 30 minutes on my hardware and required around 18GB of system RAM
  
```
python preprocess.py
```

* Now that you have the sub-graphs serialized and saved to disk, you can run the experiment with run_experiment.py

```
python run_experiment.py
```

* With experiment results serialized, you can visualize them via visualize.py

```
python visualize.py
```
