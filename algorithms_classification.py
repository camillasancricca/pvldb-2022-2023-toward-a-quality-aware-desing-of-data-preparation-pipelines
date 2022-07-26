import pandas as pd
from sklearn.model_selection import ShuffleSplit, cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import SGDClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, BaggingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import numpy as np

def encode_and_bind(original_dataframe, feature_to_encode):
    dummies = pd.get_dummies(original_dataframe[[feature_to_encode]], dummy_na=True)
    res = pd.concat([original_dataframe, dummies], axis=1)
    res = res.drop([feature_to_encode], axis=1)
    return(res)

def classification(dataset, class_name, classifier):

    feature_cols = list(dataset.columns)
    feature_cols.remove(class_name)

    X = dataset[1:][feature_cols] # Features
    y = dataset[1:][class_name] # Target variable

    numeric_columns=list(X.select_dtypes(include=['int64','float64']).columns)
    categorical_columns=list(X.select_dtypes(include=['bool','object']).columns)

    for col in X.columns:
        if col in categorical_columns:
            X = encode_and_bind(X,col)

    feature_columns = list(X.columns)

    if len(numeric_columns)!=0 and len(categorical_columns)==0:
        X = StandardScaler().fit_transform(X)

    X = np.nan_to_num(X)
    X = pd.DataFrame(X, columns=feature_columns)

    clf = DecisionTreeClassifier()

    #Choose classifier
    if classifier == "dt":
        clf = DecisionTreeClassifier()
    elif classifier == "knn":
        clf = KNeighborsClassifier()
    elif classifier == "nb":
        clf = GaussianNB()
    elif classifier == "sgd":
        clf = SGDClassifier()
    elif classifier == "svm":
        clf = SVC(kernel="linear")
    elif classifier == "svm-rbf":
        clf = SVC()
    elif classifier == "gpc":
        clf = GaussianProcessClassifier()
    elif classifier == "rf":
        clf = RandomForestClassifier()
    elif classifier == "ada":
        clf = AdaBoostClassifier()
    elif classifier == "bag":
        clf = BaggingClassifier()

    dt_fit = clf.fit(X, y)

    cv = ShuffleSplit(n_splits=3, test_size=0.3, random_state=0)
    dt_scores = cross_val_score(dt_fit, X, y, cv = cv, scoring="f1_weighted")
    print(dt_scores.mean())
    return dt_scores.mean()

def logisticRegression(dataset, class_name):

    feature_cols = list(dataset.columns)
    feature_cols.remove(class_name)

    X = dataset[1:][feature_cols] # Features
    y = dataset[1:][class_name] # Target variable

    numeric_columns=list(X.select_dtypes(include=['int64','float64']).columns)
    categorical_columns=list(X.select_dtypes(include=['bool','object']).columns)

    for col in X.columns:
        if col in categorical_columns:
            X = encode_and_bind(X,col)

    feature_columns = list(X.columns)

    if len(numeric_columns)!=0:
        X = X.where(X.notnull(), 0)
        X = StandardScaler().fit_transform(X)
        X = pd.DataFrame(X, columns = feature_columns)

    #Choose classifier
    clf = LogisticRegression(max_iter=1000)

    dt_fit = clf.fit(X, y)

    cv = ShuffleSplit(n_splits=3, test_size=0.3, random_state=0)
    dt_scores = cross_val_score(dt_fit, X, y, cv = cv, scoring="f1_weighted")
    print(dt_scores.mean())
    return dt_scores.mean()