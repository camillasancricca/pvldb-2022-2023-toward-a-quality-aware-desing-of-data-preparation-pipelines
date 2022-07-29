import random as rd
import numpy as np

# imputing missing values

def imputing_missing_values(dataset):

    for col in dataset.columns:
        if (dataset[col].dtype != "object"):
            dataset[col] = dataset[col].fillna(dataset[col].mean())
        else:
            dataset[col] = dataset[col].fillna(dataset[col].mode()[0])
            #dataset[col] = dataset[col].fillna("Missing")

    return dataset

# delete missing values

def delete_missing_values(dataset):
    dataset = dataset.dropna(axis=0, how='any')
    return dataset

# outlier correction

def outlier_correction(dataset, outlier_range, targeted_class):

    for col in dataset.columns:
        if col != targeted_class:
            index = dataset.columns.get_loc(col)

            if (dataset[col].dtype != "object"):
                if ((dataset[col].mean() < outlier_range[index][0]) | (dataset[col].mean() > outlier_range[index][1])):
                    dataset.loc[((dataset[col] < outlier_range[index][0]) | (dataset[col] > outlier_range[index][1])) & dataset[col].notnull(),col]=rd.uniform(outlier_range[index][0],outlier_range[index][1])
                else:
                    dataset.loc[((dataset[col] < outlier_range[index][0]) | (dataset[col] > outlier_range[index][1])) & dataset[col].notnull(),col]=dataset[col].mean()
            else:
                dataset.loc[~dataset[col].isin(outlier_range[index]) & dataset[col].notnull(),col]=dataset[col].mode()[0]
                #dataset.loc[~dataset[col].isin(outlier_range[index]) & dataset[col].notnull(), col] = np.nan

    return dataset

def correct_incorrect_depedences(dataset, rules, targeted_class, mask):

    columns = dataset.columns
    for r in rules:
        targeted_rows = dataset

        #for lhs in r["lhs"]:
        for lhs in r.lhs:
            targeted_rows = targeted_rows.loc[targeted_rows[columns[lhs[1]]] == lhs[0]] #seleziono le lhs (valore a destra della fd)

        #for rhs in r["rhs"]:
        for rhs in r.rhs:
            if dataset.columns[rhs[1]] != targeted_class:
                indexes = targeted_rows.index.tolist()
                for i in indexes:
                    OK = True
                    if dataset.columns[rhs[1]] != targeted_class:
                        if mask[targeted_rows.columns.get_loc(columns[rhs[1]])][i] == 2:

                            #for lhs in r["lhs"]:
                            for lhs in r.lhs:
                                if dataset.columns[lhs[1]] != targeted_class:
                                    if mask[targeted_rows.columns.get_loc(columns[lhs[1]])][i] == 2:
                                        OK = False

                            if (OK):
                                if dataset[columns[rhs[1]]].dtype != "object":
                                    dataset.loc[i:i,columns[rhs[1]]] = float(rhs[0])
                                else:
                                    dataset.loc[i:i,columns[rhs[1]]] = rhs[0]

    return dataset