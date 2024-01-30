import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn.metrics import davies_bouldin_score

docs = {} #dictionary mapping document id to document contents

srcfolder = os.path.dirname(os.path.abspath(__file__))

def choose_file(datapath = "Data\cluster19_1000_3_3.dat"):
    datafolder = os.path.join(srcfolder, "Data\\"+ datapath) 
    df = pd.read_csv(datafolder, header=None, skiprows=1, delimiter=";")

    x = df[df.columns[0]]
    y = df[df.columns[1]]
    if df.shape[1] == 4:
        z = df[df.columns[2]]
        scatter_z = np.array(z)
    else:
        scatter_z = [0]
    scatter_x = np.array(x)
    scatter_y = np.array(y)
    
    return df, scatter_x, scatter_y, scatter_z

def plotd(scatter_x, scatter_y, scatter_z, group, cdict):
    fig = plt.figure()
    if len(scatter_z) > 1:
        ax = fig.add_subplot(projection='3d')
        for g in np.unique(group):
            ix = np.where(group == g)
            ax.scatter(scatter_x[ix], scatter_y[ix], scatter_z[ix], c = cdict[g], label = g)
        ax.legend()
        plt.show()

    else:
        fig, ax = plt.subplots()
        for g in np.unique(group):
            ix = np.where(group == g)
            ax.scatter(scatter_x[ix], scatter_y[ix], c = cdict[g], label = g)
        ax.legend()
        plt.show()

cdict = {-1: "yellow", 0:"black", 1: 'red', 2: 'blue', 3: 'green', 4:"magenta", 5:"gray", 6:"olive", 7:"orange"}
clustering_dict = {0:"Hierachial", 1:"K-Means", 2:"DBSCAN"}

def clustering_algorithms(method, scatter_x, scatter_y, scatter_z, n, e, m, plot=False):
    clustering_method = clustering_dict[method]

    if clustering_method == "Hierachial":
        if len(scatter_z) > 1:
            clustering = AgglomerativeClustering(n_clusters=n).fit(np.array([scatter_x, scatter_y, scatter_z]).T)
            clustering
            labels=clustering.labels_
            dbscore = davies_bouldin_score(np.array([scatter_x, scatter_y, scatter_z]).T, labels)

        else:
            clustering = AgglomerativeClustering(n_clusters=n).fit(np.array([scatter_x, scatter_y]).T)
            clustering
            labels=clustering.labels_
            dbscore = davies_bouldin_score(np.array([scatter_x, scatter_y]).T, labels)
        
    if clustering_method == "K-Means":
        if len(scatter_z) > 1:
            clustering = KMeans(n_clusters=n,random_state=0,n_init="auto").fit(np.array([scatter_x, scatter_y, scatter_z]).T)
            clustering
            labels=clustering.labels_
            dbscore = davies_bouldin_score(np.array([scatter_x, scatter_y, scatter_z]).T, labels)

        else:
            clustering = KMeans(n_clusters=n,random_state=0,n_init="auto").fit(np.array([scatter_x, scatter_y]).T)
            clustering
            labels=clustering.labels_
            dbscore = davies_bouldin_score(np.array([scatter_x, scatter_y]).T, labels)


    if clustering_method == "DBSCAN":
        if len(scatter_z) > 1:
            clustering = DBSCAN(eps=e, min_samples=m).fit(np.array([scatter_x, scatter_y, scatter_z]).T)
            clustering
            labels=clustering.labels_
            dbscore = davies_bouldin_score(np.array([scatter_x, scatter_y, scatter_z]).T, labels)

        else:
            clustering = DBSCAN(eps=e, min_samples=m).fit(np.array([scatter_x, scatter_y]).T)
            clustering
            labels=clustering.labels_
            dbscore = davies_bouldin_score(np.array([scatter_x, scatter_y]).T, labels)

    
    if plot:
        plotd(scatter_x, scatter_y, scatter_z, labels, cdict)

    return dbscore


all_datafolder = os.path.join(srcfolder, "Data")
dbscore_docs = {}

hierachial_scores = []
kmeans_scores = []
DBSCAN_scores = []

for file in os.listdir(all_datafolder):
    df, scatter_x, scatter_y, scatter_z = choose_file(file)
    dbscore_hierachial = clustering_algorithms(0, scatter_x, scatter_y, scatter_z, n=2, e=0.2, m=2)
    dbscore_kmeans = clustering_algorithms(1, scatter_x, scatter_y, scatter_z, n=2, e=0.2, m=2)
    dbscore_DBSCAN = clustering_algorithms(2, scatter_x, scatter_y, scatter_z, n=2, e=0.2, m=2)
    dbscore_docs[file] = [dbscore_hierachial, dbscore_kmeans, dbscore_DBSCAN]
    hierachial_scores.append(float(dbscore_hierachial))
    kmeans_scores.append(float(dbscore_kmeans))
    DBSCAN_scores.append(float(dbscore_DBSCAN))



#dbscore = clustering_algorithms(0, df, scatter_x, scatter_y, scatter_z, n=2, e=0.2, m=2, plot=True)
#print(dbscore)
clustering_algorithms(2, scatter_x=np.array(hierachial_scores), scatter_y=np.array(kmeans_scores), scatter_z=[0], n=3, e=0.2, m=2, plot=True)