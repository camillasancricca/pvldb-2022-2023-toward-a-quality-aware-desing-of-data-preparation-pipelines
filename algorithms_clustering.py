from sklearn import metrics
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN

def encode_and_bind(original_dataframe, feature_to_encode):
    dummies = pd.get_dummies(original_dataframe[[feature_to_encode]], dummy_na=True)
    res = pd.concat([original_dataframe, dummies], axis=1)
    res = res.drop([feature_to_encode], axis=1)
    return(res)

def encode_and_null(df):
    #if attributes are categorical: one hot encoding

    for col in df.columns:
        if df[col].dtype == "object" or df[col].dtype == "bool":
            df = encode_and_bind(df,col)

    #if there are some null values substitute with 0
    df = np.nan_to_num(df)
    return df

def preprocess(df):
    """Preprocess data for clustering"""
    df_log = abs(df)
    df_log = np.log1p(df_log)
    scaler = StandardScaler()
    scaler.fit(df_log)
    df_norm = scaler.transform(df_log)
    #df_norm = np.nan_to_num(df_norm)

    return df_norm

def clustering(df, method, k, eps, metric):

    df = df[1:][:]
    df = encode_and_null(df)
    df_norm = preprocess(df)

    if (method == "kmeans"):

        kmeans = KMeans(n_clusters=k, random_state=1)
        kmeans.fit(df_norm)
        model = kmeans

    if (method == "agglomerative"):

        agglomerative = AgglomerativeClustering(linkage="ward", n_clusters=k) #linkage = "ward", "average", "complete", "single"
        agglomerative.fit(df_norm)
        model = agglomerative

    if (method == "dbscan"):

        dbscan = DBSCAN(eps=eps, metric="euclidean")
        dbscan.fit(df_norm)
        model = dbscan

    try:
        silhouette = metrics.silhouette_score(df, model.labels_, metric=metric)
    except:
        return -1
    print(silhouette)
    #return [silhouette,model.labels_]
    return silhouette