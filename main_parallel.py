from multiprocessing import Pool
from itertools import repeat
import numpy as np
import dirty_functions
import algorithms_classification
import algorithms_clustering

def generate_seed(n_seed,n_elements):
    seed = []
    seeds = []
    for r in range(0,n_seed):
        for i in range(0,n_elements):
            seed.append(int(np.random.randint(0, 100)))
        seeds.append(seed)
        seed = []
    return seeds

def performances(name, name_class, columns_indexes, seed, n_clusters, eps):

    consistency = np.zeros((7, 10))
    accuracy = np.zeros((7, 10))
    completeness = np.zeros((7, 10))

    for k in range(0,len(seed)):

        datasets_consistency = dirty_functions.dirty_consistency(seed[k], name, name_class, columns_indexes)
        datasets_accuracy = dirty_functions.dirty_syn_accuracy(seed[k], name, name_class)
        datasets_completeness = dirty_functions.dirty_completeness(seed[k], name, name_class)

        i = 0
        for dataset in datasets_consistency:

            #Apply the algorithms_classification for consistency
            consistency[0][i] = consistency[0][i] + algorithms_classification.classification(dataset, name_class, "dt")
            consistency[1][i] = consistency[1][i] + algorithms_classification.classification(dataset, name_class, "knn")
            consistency[2][i] = consistency[2][i] + algorithms_classification.classification(dataset, name_class, "nb")
            consistency[3][i] = consistency[3][i] + algorithms_classification.logisticRegression(dataset, name_class)
            consistency[4][i] = consistency[4][i] + algorithms_clustering.clustering(dataset, "kmeans", n_clusters,eps, "manhattan")
            consistency[5][i] = consistency[5][i] + algorithms_clustering.clustering(dataset, "agglomerative", n_clusters,eps, "manhattan")
            consistency[6][i] = consistency[6][i] + algorithms_clustering.clustering(dataset, "dbscan", n_clusters,eps, "manhattan")
            i = i+1

        i = 0
        for dataset in datasets_accuracy:

            #Apply the algorithms_classification for accuracy
            accuracy[0][i] = accuracy[0][i] + algorithms_classification.classification(dataset, name_class, "dt")
            accuracy[1][i] = accuracy[1][i] + algorithms_classification.classification(dataset, name_class, "knn")
            accuracy[2][i] = accuracy[2][i] + algorithms_classification.classification(dataset, name_class, "nb")
            accuracy[3][i] = accuracy[3][i] + algorithms_classification.logisticRegression(dataset, name_class)
            accuracy[4][i] = accuracy[4][i] + algorithms_clustering.clustering(dataset, "kmeans", n_clusters,eps, "manhattan")
            accuracy[5][i] = accuracy[5][i] + algorithms_clustering.clustering(dataset, "agglomerative", n_clusters,eps, "manhattan")
            accuracy[6][i] = accuracy[6][i] + algorithms_clustering.clustering(dataset, "dbscan", n_clusters,eps, "manhattan")
            i = i+1

        i = 0
        for dataset in datasets_completeness:

            #Apply the algorithms_classification for completeness
            completeness[0][i] = completeness[0][i] + algorithms_classification.classification(dataset, name_class, "dt")
            completeness[1][i] = completeness[1][i] + algorithms_classification.classification(dataset, name_class, "knn")
            completeness[2][i] = completeness[2][i] + algorithms_classification.classification(dataset, name_class, "nb")
            completeness[3][i] = completeness[3][i] + algorithms_classification.logisticRegression(dataset, name_class)
            completeness[4][i] = completeness[4][i] + algorithms_clustering.clustering(dataset, "kmeans", n_clusters,eps, "manhattan")
            completeness[5][i] = completeness[5][i] + algorithms_clustering.clustering(dataset, "agglomerative", n_clusters,eps, "manhattan")
            completeness[6][i] = completeness[6][i] + algorithms_clustering.clustering(dataset, "dbscan", n_clusters,eps, "manhattan")
            i = i+1

    consistency = consistency/len(seed)
    accuracy = accuracy/len(seed)
    completeness = completeness/len(seed)

    return [consistency,accuracy,completeness]

if __name__ == '__main__':

    n_instances_tot = 24
    n_parallel_jobs = 12
    n_instances_x_job = int(n_instances_tot/n_parallel_jobs)
    name = "users_class"
    class_name = "TS"

    n_clusters = 2
    eps = 3

    #the indexes to dirt in consistency (the one included in the functional dependencies)
    indexes = []

    con = np.zeros((7, 10))
    acc = np.zeros((7, 10))
    com = np.zeros((7, 10))

    seed = generate_seed(n_parallel_jobs, n_instances_x_job)

    itr = zip(repeat(name), repeat(class_name), repeat(indexes), seed, repeat(n_clusters), repeat(eps))
    with Pool(processes=n_parallel_jobs) as pool:
        results = pool.starmap(performances, itr)

        results_final = np.array([con,acc,com])
        for instance in range(0,n_parallel_jobs):
            results_final = results_final + results[instance]

        results_final = results_final/n_parallel_jobs
        print(results_final)

    with open(name + "_results.txt", "w") as file:
        for r1 in results_final:
            for r2 in r1:
                file.write(np.array2string(r2, separator=','))
                file.write("\n")
            file.write("\n")