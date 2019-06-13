import pprint

from DiCaro._init_ import *
from DiCaro._logic_ import *
from DiCaro._view_ import *


if __name__ == '__main__':

    '''
    Generation of a clustering group based on information such as tempo, loudness, "artist_hotttnesss"
    '''
    tracks_ids, tracks_examples = pre_process_tracks(data)
    subjective_clustering = plot_cluster(tracks_examples, subj_clustering_components, 5, three_dimensions=True)

    '''
    Generation of a clustering group based on information such as lyrics in songs
    '''
    tracks_occurrences = pre_process_occurrences(data, track_ids, words)
    occurrences_ids = list(map(lambda example: track_ids[example[0]], tracks_occurrences))
    textual_clustering = plot_cluster(tracks_occurrences, text_clustering_components, 10,
                                 decompose=False, clustering="kmeans", three_dimensions=True)

    '''
    Extraction and visualization of the most correlated instances between couples of the previous generated clusters groups
    '''
    best_correlation, subjective_cluster_name, textual_cluster_name = \
        get_best_correlation(subjective_clustering, textual_clustering, tracks_ids, occurrences_ids)
    intersection_information = aggregate_clusters_data(tracks_examples, tracks_occurrences, track_ids, words)
    print("Best cluster correlation:", subjective_cluster_name, "<->", textual_cluster_name)
    pprint.pprint(intersection_information)

