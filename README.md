# Toward a quality-aware design of data preparation pipelines (source code)

## Scripts

- main_parallel.py:
  - extracts the performance scores for a given dataset
  - different algorithms can be analyzed at the same time
  - from line 80 to 87 you have to change the following parameters:
    - _name_ (the name of the dataset, that must be placed in a directory with the same name of the dataset in csv format, for example "iris" refers to iris/iris.csv)
    - _class_name_
    - _indexes_ (the column indexes to dirt in consistency)
    - _n_clusters_
    - _eps_
  - you can copy and past the list of inputs (_n_clusters_ and _eps_) from the parameters.txt file

- main_parallel_validation.py:
  - extracts the set of performance scores to validate the rankings of a given dataset
  - different algorithms can be analyzed at the same time
  - from line 252 to 263 you have to change the following parameters:
    - _name_ (the name of the dataset, that must be placed in a directory with the same name of the dataset in csv format, for example "iris" refers to iris/iris.csv)
    - _class_name_
    - _n_attr_ (the number of attributes)
    - _indexes_ (the column indexes to dirt in consistency)
    - _dataset_ (the original dataset loaded using pandas)
    - _rules_ (the set of founded association rules)
    - _ranges_ (the accuracy ranges for each column)
    - _n_clusters_
    - _eps_
  - you can copy and past the list of inputs (_n_attr_, _indexes_, _dataset_, _rules_, _ranges_, _n_clusters_ and _eps_) from the parameters.txt file

- ranking_extraction.py: extracts the ranking of quality dimensions for an algorithm given their related performance scores extracted using main_parallel.py

- ranking_validation.py: creates a csv table for the validation of a ranking given the set of performance scores extracted using main_parallel_validation.py

## Requirements
You can find all the libraries used in this project in the requirements.txt.