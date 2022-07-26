from multiprocessing import Pool
from itertools import repeat
import numpy as np
import algorithms_classification
import dirty_functions
import improve_quality
import pandas as pd
import associationRules
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

def improve_dimension(dim, d, ranges, rules, name_class, mask_d):
    if dim == "accuracy":
        print("improve accuracy...")
        d = improve_quality.outlier_correction(d, ranges, name_class)
    elif dim == "completeness":
        print("improve completeness...")
        d = improve_quality.imputing_missing_values(d)
    elif dim == "consistency":
        print("improve consistency...")
        d = improve_quality.correct_incorrect_depedences(d, rules, name_class, mask_d)
    else:
        return d
    return d

def performances(name, name_class, columns_indexes, seed, ranges, rules, n_clusters, eps, n_attr):

    performance1 = [np.zeros((7, 10)),np.zeros((7, 10)),np.zeros((7, 10)),np.zeros((7, 10))]
    performance2 = [np.zeros((7, 10)),np.zeros((7, 10)),np.zeros((7, 10)),np.zeros((7, 10))]
    performance3 = [np.zeros((7, 10)),np.zeros((7, 10)),np.zeros((7, 10)),np.zeros((7, 10))]
    performance4 = [np.zeros((7, 10)),np.zeros((7, 10)),np.zeros((7, 10)),np.zeros((7, 10))]
    performance5 = [np.zeros((7, 10)),np.zeros((7, 10)),np.zeros((7, 10)),np.zeros((7, 10))]
    performance6 = [np.zeros((7, 10)),np.zeros((7, 10)),np.zeros((7, 10)),np.zeros((7, 10))]

    for k in range(0,len(seed)):

        df_all = dirty_functions.dirty_all_with_return_consistency(k, name, name_class, columns_indexes)
        df = df_all[0].copy()
        mask = df_all[1]

        dimensions = ["accuracy", "consistency", "completeness", "0"]
        #first ranking validation
        i = 0
        t = 0
        for ds in df:
            d = ds.copy()

            mask_d = mask[t:t+n_attr]
            t += n_attr

            j = 0
            for p in performance1:

                print("compute performance: ")
                p[0][i] = p[0][i] + algorithms_classification.classification(d, name_class, "dt")
                p[1][i] = p[1][i] + algorithms_classification.classification(d, name_class, "knn")
                p[2][i] = p[2][i] + algorithms_classification.classification(d, name_class, "nb")
                p[3][i] = p[3][i] + algorithms_classification.logisticRegression(d, name_class)
                p[4][i] = p[4][i] + algorithms_clustering.clustering(d, "kmeans", n_clusters, eps, "manhattan")
                p[5][i] = p[5][i] + algorithms_clustering.clustering(d, "agglomerative", n_clusters, eps, "manhattan")
                p[6][i] = p[6][i] + algorithms_clustering.clustering(d, "dbscan", n_clusters, eps, "manhattan")

                d = improve_dimension(dimensions[j], d, ranges, rules, name_class, mask_d)
                j += 1

            i += 1

        dimensions = ["accuracy", "completeness", "consistency", "0"]
        #second ranking validation
        i = 0
        t = 0
        for ds in df:
            d = ds.copy()

            mask_d = mask[t:t+n_attr]
            t += n_attr

            j = 0
            for p in performance2:

                print("compute performance: ")
                p[0][i] = p[0][i] + algorithms_classification.classification(d, name_class, "dt")
                p[1][i] = p[1][i] + algorithms_classification.classification(d, name_class, "knn")
                p[2][i] = p[2][i] + algorithms_classification.classification(d, name_class, "nb")
                p[3][i] = p[3][i] + algorithms_classification.logisticRegression(d, name_class)
                p[4][i] = p[4][i] + algorithms_clustering.clustering(d, "kmeans", n_clusters, eps, "manhattan")
                p[5][i] = p[5][i] + algorithms_clustering.clustering(d, "agglomerative", n_clusters, eps, "manhattan")
                p[6][i] = p[6][i] + algorithms_clustering.clustering(d, "dbscan", n_clusters, eps, "manhattan")

                d = improve_dimension(dimensions[j], d, ranges, rules, name_class, mask_d)
                j += 1

            i += 1

        dimensions = ["consistency", "accuracy", "completeness", "0"]
        #third ranking validation
        i = 0
        t = 0
        for ds in df:
            d = ds.copy()

            mask_d = mask[t:t+n_attr]
            t += n_attr

            j = 0
            for p in performance3:

                print("compute performance: ")
                p[0][i] = p[0][i] + algorithms_classification.classification(d, name_class, "dt")
                p[1][i] = p[1][i] + algorithms_classification.classification(d, name_class, "knn")
                p[2][i] = p[2][i] + algorithms_classification.classification(d, name_class, "nb")
                p[3][i] = p[3][i] + algorithms_classification.logisticRegression(d, name_class)
                p[4][i] = p[4][i] + algorithms_clustering.clustering(d, "kmeans", n_clusters, eps, "manhattan")
                p[5][i] = p[5][i] + algorithms_clustering.clustering(d, "agglomerative", n_clusters, eps, "manhattan")
                p[6][i] = p[6][i] + algorithms_clustering.clustering(d, "dbscan", n_clusters, eps, "manhattan")

                d = improve_dimension(dimensions[j], d, ranges, rules, name_class, mask_d)
                j += 1

            i += 1

        dimensions = ["consistency", "completeness", "accuracy", "0"]
        #4 ranking validation
        i = 0
        t = 0
        for ds in df:
            d = ds.copy()

            mask_d = mask[t:t + n_attr]
            t += n_attr

            j = 0
            for p in performance4:
                print("compute performance: ")
                p[0][i] = p[0][i] + algorithms_classification.classification(d, name_class, "dt")
                p[1][i] = p[1][i] + algorithms_classification.classification(d, name_class, "knn")
                p[2][i] = p[2][i] + algorithms_classification.classification(d, name_class, "nb")
                p[3][i] = p[3][i] + algorithms_classification.logisticRegression(d, name_class)
                p[4][i] = p[4][i] + algorithms_clustering.clustering(d, "kmeans", n_clusters, eps, "manhattan")
                p[5][i] = p[5][i] + algorithms_clustering.clustering(d, "agglomerative", n_clusters, eps, "manhattan")
                p[6][i] = p[6][i] + algorithms_clustering.clustering(d, "dbscan", n_clusters, eps, "manhattan")

                d = improve_dimension(dimensions[j], d, ranges, rules, name_class, mask_d)
                j += 1

            i += 1

        dimensions = ["completeness", "accuracy", "consistency", "0"]
        #5 ranking validation
        i = 0
        t = 0
        for ds in df:
            d = ds.copy()

            mask_d = mask[t:t + n_attr]
            t += n_attr

            j = 0
            for p in performance5:
                print("compute performance: ")
                p[0][i] = p[0][i] + algorithms_classification.classification(d, name_class, "dt")
                p[1][i] = p[1][i] + algorithms_classification.classification(d, name_class, "knn")
                p[2][i] = p[2][i] + algorithms_classification.classification(d, name_class, "nb")
                p[3][i] = p[3][i] + algorithms_classification.logisticRegression(d, name_class)
                p[4][i] = p[4][i] + algorithms_clustering.clustering(d, "kmeans", n_clusters, eps, "manhattan")
                p[5][i] = p[5][i] + algorithms_clustering.clustering(d, "agglomerative", n_clusters, eps, "manhattan")
                p[6][i] = p[6][i] + algorithms_clustering.clustering(d, "dbscan", n_clusters, eps, "manhattan")

                d = improve_dimension(dimensions[j], d, ranges, rules, name_class, mask_d)
                j += 1

            i += 1

        dimensions = ["completeness", "consistency", "accuracy", "0"]
        #6 ranking validation
        i = 0
        t = 0
        for ds in df:
            d = ds.copy()

            mask_d = mask[t:t + n_attr]
            t += n_attr

            j = 0
            for p in performance6:
                print("compute performance: ")
                p[0][i] = p[0][i] + algorithms_classification.classification(d, name_class, "dt")
                p[1][i] = p[1][i] + algorithms_classification.classification(d, name_class, "knn")
                p[2][i] = p[2][i] + algorithms_classification.classification(d, name_class, "nb")
                p[3][i] = p[3][i] + algorithms_classification.logisticRegression(d, name_class)
                p[4][i] = p[4][i] + algorithms_clustering.clustering(d, "kmeans", n_clusters, eps, "manhattan")
                p[5][i] = p[5][i] + algorithms_clustering.clustering(d, "agglomerative", n_clusters, eps, "manhattan")
                p[6][i] = p[6][i] + algorithms_clustering.clustering(d, "dbscan", n_clusters, eps, "manhattan")

                d = improve_dimension(dimensions[j], d, ranges, rules, name_class, mask_d)
                j += 1

            i += 1

    for i in range(0,4):
        performance1[i] = performance1[i]/len(seed)
        performance2[i] = performance2[i]/len(seed)
        performance3[i] = performance3[i]/len(seed)
        performance4[i] = performance4[i]/len(seed)
        performance5[i] = performance5[i]/len(seed)
        performance6[i] = performance6[i]/len(seed)

    return [[performance1[0],performance1[1],performance1[2],performance1[3]],[performance2[0],performance2[1],performance2[2],performance2[3]],[performance3[0],performance3[1],performance3[2],performance3[3]],
            [performance4[0],performance4[1],performance4[2],performance4[3]],[performance5[0],performance5[1],performance5[2],performance5[3]],[performance6[0],performance6[1],performance6[2],performance6[3]]]

def parallel_ranking_validation(n_instances_tot,n_parallel_jobs,name,class_name,indexes,rules,ranges,n_clusters,eps,n_attr):

    n_instances_x_job = int(n_instances_tot/n_parallel_jobs)

    raw = np.zeros((7, 10))
    first = np.zeros((7, 10))
    second = np.zeros((7, 10))
    final = np.zeros((7, 10))

    seed = generate_seed(n_parallel_jobs, n_instances_x_job)

    itr = zip(repeat(name), repeat(class_name), repeat(indexes), seed, repeat(ranges), repeat(rules),repeat(n_clusters),repeat(eps),repeat(n_attr))
    with Pool(processes=n_parallel_jobs) as pool:
        results = pool.starmap(performances, itr)

        results_final = np.array([[raw, first, second, final],[raw, first, second, final],[raw, first, second, final],
                                  [raw, first, second, final],[raw, first, second, final],[raw, first, second, final]])
        results = np.array(results)

        for i in range(0,6):

            for instance in range(0, n_parallel_jobs):
                results_final[i] = results_final[i] + results[instance][i]

        results_final = results_final / n_parallel_jobs
        print(results_final)
        return results_final

if __name__ == '__main__':

    n_instances_tot = 24
    n_parallel_jobs = 12
    name = "users_class"
    class_name = "TS"

    n_attr = 4
    indexes_users = [0, 1, 2, 3]
    users = pd.read_csv("users/users.csv")
    rules = associationRules.rules(users, 0.2, 0.9)
    ranges = [["CT_range_1", "CT_range_2", "CT_range_3", "CT_range_4"],
              ["CU_range_1", "CU_range_2", "CU_range_3", "CU_range_4"],
              ["LT_range_1", "LT_range_2", "LT_range_3", "LT_range_4"], ["ECommerce", "game", "holiday", "sport"]]
    n_clusters = 2
    eps = 3

    results = parallel_ranking_validation(n_instances_tot,n_parallel_jobs,name,class_name,indexes,rules,ranges,n_clusters,eps,n_attr)

    with open(name + "_validation" + "_results.txt", "w") as file:
        i = 0
        for r in results:
            if (i == 0):
                file.write("accuracy -> consistency -> completeness:\n")
            elif (i == 1):
                file.write("accuracy -> completeness -> consistency:\n")
            elif (i == 2):
                file.write("consistency -> accuracy -> completeness:\n")
            elif (i == 3):
                file.write("consistency -> completeness -> accuracy:\n")
            elif (i == 4):
                file.write("completeness -> accuracy -> consistency:\n")
            elif (i == 5):
                file.write("completeness -> consistency -> accuracy:\n")
            for r1 in r:
                for r2 in r1:
                    file.write(np.array2string(r2, separator=','))
                    file.write("\n")
                file.write("\n")
            i += 1