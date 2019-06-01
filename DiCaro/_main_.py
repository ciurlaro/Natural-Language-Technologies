from DiCaro._init_ import *
from DiCaro._logic_ import *
from DiCaro._view_ import *

if __name__ == '__main__':
    tracks_examples = pre_process_tracks(data)
    plot_cluster(tracks_examples, subj_clustering_components, third_dimension=True)

    tracks_co_occurrences = pre_process_occurrences(data, track_ids)
    plot_cluster(tracks_co_occurrences, text_clustering_components, clustering="kmeans", third_dimension=True)

