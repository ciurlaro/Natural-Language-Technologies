import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from mpl_toolkits.mplot3d import Axes3D


def plot_cluster(examples, components, decompose=True, clustering="hierarchical", third_dimension=False):
    global predicted
    examples = np.array(examples)

    if decompose:
        pca = PCA(3)
        examples = pca.fit_transform(examples)

    if clustering == "hierarchical":
        hc = AgglomerativeClustering(n_clusters=3, linkage='complete')
        predicted = hc.fit_predict(examples)
    elif clustering == "kmeans":
        kmeans = KMeans(3)
        predicted = kmeans.fit_predict(examples)
    else:
        print("Clustering permessi:", "hierarchical", "kmeans")

    fig = plt.figure()

    if third_dimension:
        ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)
        ax.scatter(examples[:, 0], examples[:, 1], examples[:, 2], c=predicted)
        ax.set_xlabel(components[0])
        ax.set_ylabel(components[1])
        ax.set_zlabel(components[2])
    else:
        plt.scatter(examples[:, 0], examples[:, 1], c=predicted)
        plt.xlabel(components[0])
        plt.ylabel(components[1])
    plt.show()
