import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.cluster import MiniBatchKMeans as KMeans
from sklearn.cluster import AgglomerativeClustering
from mpl_toolkits.mplot3d import Axes3D


def plot_cluster(examples, components, n_clusters, decompose=True, clustering="hierarchical", three_dimensions=False):
    """
    Plots the examples into a plotting area
    :param examples: instances of the dataset to be plotted
    :param components: list of components of the instances
    :param n_clusters: number of cluster in which the dataset will be divided
    :param decompose: if True, PCA decomposition is computed before plotting
    :param clustering: defines the clustering algorithm. Possible values: "hierarchical" and "kmeans"
    :param three_dimensions: if True, the generated plot is 3 dimensional
    :return:
    """
    global predicted
    examples = np.array(examples)

    if decompose:
        pca = PCA(3)
        examples = pca.fit_transform(examples)

    if clustering == "hierarchical":
        hc = AgglomerativeClustering(n_clusters)# , linkage='complete')
        predicted = hc.fit_predict(examples)
    elif clustering == "kmeans":
        kmeans = KMeans(n_clusters)
        predicted = kmeans.fit_predict(examples)
    else:
        print("Clustering permessi:", "hierarchical", "kmeans")

    fig = plt.figure()
    if three_dimensions:
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

    return predicted

