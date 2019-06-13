import sqlite3, csv
from collections import defaultdict
from pathlib import Path
from nltk.corpus import stopwords
from DiCaro.MSongsDB.PythonSrc import hdf5_getters
from DiCaro._init_ import *


def loading_info(db_file, h5_file, data):
    """
    Loads from a Database and a Hierarchical Data Format the following attributes for each track:
    track_id, title, artist_name, artist_hotttnesss, artist_familiarity
    :param db_file: Database file whose tuples has to be extracted
    :param h5_file: Hierarchical Data Format file whose content has to be extracted
    :param data: data structure in which all the information are collected
    """
    conn = sqlite3.connect(str(db_file))
    q = "SELECT track_id, title, artist_name, artist_hotttnesss, artist_familiarity FROM songs"
    res = conn.execute(q)

    h5 = hdf5_getters.open_h5_file_read(h5_file)

    for row in res:
        track_id = row[0]
        title = row[1]
        artist_name = row[2]
        artist_hotttnesss = row[3]
        artist_familiarity = row[4]
        data[track_id, "info"] = title, artist_name, artist_hotttnesss, artist_familiarity, get_infos_by_track_id(h5, track_id) \
                                 # , get_infos_by_song_and_artist_id(h5, song_id, artist_id)
    h5.close()


def get_infos_by_track_id(h5, track_id) -> tuple:
    """
    Extracts information, about a track whose id is given, from a Hierarchical Data Format analysis file
    :param h5: Hierarchical Data Format file whose content has to be extracted
    :param track_id: track unique identifier
    :return: a tuple containing analysis information associated to the track id
    """
    for record in h5.root.analysis.songs.where('track_id=="' + track_id + '"'):
        return record["tempo"], record["loudness"] # , record["energy"], record["danceability"] sono sempre 0 nel dataset ridotto


def get_infos_by_song_and_artist_id(h5, song_id, artist_id) -> tuple:
    """
    Extracts information, about a track whose id is given, from a Hierarchical Data Format metadata file
    :param h5: Hierarchical Data Format file whose content has to be extracted
    :param track_id: track unique identifier
    :return: a tuple containing metadata information associated to the `track_id`
    """
    for record in h5.root.metadata.songs.where('song_id=="' + song_id + '"', 'artist_id=="' + artist_id + '"'):
        return record["song_hotttnesss"], record["genre"].decode()


def get_lyrics(musiXmatch_file, data) -> list:
    """
    Extracts all the tracks lyrics and associates them to the corresponding track through their `track_id`
    :param musiXmatch_file: textual file whose content is the lyrics dataset
    :param data: data structure in which all the information are collected
    :return: list of the words contained in the lyrics dataset
    """
    with open(musiXmatch_file, encoding="utf8") as musiXmatch:
        for i, row in enumerate(musiXmatch):
            frequencies = {}

            if i == 17:
                words = ['%'] + row[1:-1].split(",")
            elif i >= 18:
                row = row[:-1].split(",")
                for frequency in row[2:]:
                    idx, cnt = frequency.split(":")
                    frequencies[idx] = cnt

                if (row[0], "info") in data:
                    data[row[0], "lyrics"] = frequencies
    return words


def load_from_dataset(db_file, h5_file, musiXmatch_file, data) -> list:
    """
    Collect information from all the different sources and merge them into `data`
    :param db_file: Database file whose tuples has to be extracted
    :param h5_file: Hierarchical Data Format file whose content has to be extracted
    :param musiXmatch_file: textual file whose content is the lyrics dataset
    :param data: data structure in which all the information are collected
    :return: list of the words contained in the lyrics dataset
    """
    print("Loading infos...")
    loading_info(db_file, h5_file, data)
    print("Getting lyrics...")
    return get_lyrics(musiXmatch_file, data)


def write_into_csv(data, words, output_csv, words_dataset_csv):
    """
    Writes into a csv output file the collected and merged information
    :param data: data structure in which all the information are collected
    :param words: list of the words contained in the lyrics dataset
    """
    writer = csv.writer(open(output_csv, "w+", newline=''))
    for row in data.items():
        writer.writerow(row)

    writer = csv.writer(open(words_dataset_csv, "w+", newline='', encoding="utf-8"))
    writer.writerow(words)


def read_from_csv(data, output_csv, words_dataset_csv) -> list:
    """
    Reads from the csv output file the collected and merged information
    :param data: data structure in which all the information are collected
    :return: list of the words contained in the lyrics dataset
    """
    reader = csv.reader(open(output_csv), delimiter=',')
    for row in reader:
        keys = row[0][1:-1].split(", ")
        values = row[1][1:-1].split(", ")
        value = []

        if keys[1][1:-1] == "info":
            for elem in values:
                value.append(elem[1:-1])

            data[keys[0][1:-1], "info"] = value

        elif keys[1][1:-1] == "lyrics":
            frequencies = {}
            for words in values:
                idx, cnt = words.split(": ")
                frequencies[idx[1:-1]] = cnt[1:-1]

            data[keys[0][1:-1], "lyrics"] = frequencies

    reader = csv.reader(open(words_dataset_csv, encoding="utf-8"), delimiter=',')
    for row in reader:
        return row


def pre_process_tracks(data) -> tuple:
    """
    Hadles tracks information format such that they can be used in clustering
    :param data: data structure in which all the information are collected
    :return: tuple of preprocessed associations instances/id's
    """
    examples, examples_ids = [], []
    for keys in filter(lambda keys: keys[1] == "info", data.keys()):
        artist_hotttnesss = float(data[keys][2]) if data[keys][2] != "." else 0.0
        artist_familiarity = float(data[keys][3]) if data[keys][3] != "." else 0.0
        tempo = float(data[keys][4])
        loudness = float(data[keys][5])

        if artist_familiarity != 0 and artist_hotttnesss != 0 and tempo != 0 and loudness != 0:
            example = [tempo, loudness, artist_hotttnesss, artist_familiarity]
            examples.append(example)
            examples_ids.append(keys)
    return examples_ids, examples


def pre_process_occurrences(data, track_ids, words) -> list:
    """
    Hadles tracks occurrences format such that they can be used in clustering
    Also, it filters them according to their frequency and whether they are stop words or not
    :param data: data structure in which all the information are collected
    :param track_id: track unique identifier
    :param words: list of the words contained in the lyrics dataset
    :return: list of lists, each one of those contains a track_index, a word and the count of that word in that track
    """
    stop_words = set(stopwords.words('english'))
    tracks_co_occurrences = []
    for track_lyrics in filter(lambda key: key[1] == "lyrics", data.keys()):
        for word_key in data[track_lyrics].keys():
            track_index = track_ids.index(track_lyrics[0])
            word = int(word_key)
            count = data[track_lyrics][word_key]
            set(stopwords.words('english'))
            if int(count) > 3 and words[int(word_key)] not in stop_words:  # ignores low frequency and stop words
                tracks_co_occurrences.append([track_index, word, int(count)])
    return tracks_co_occurrences


def data_loading(db_file, h5_file, musiXmatch_file, data, output_csv, words_dataset_csv) -> tuple:
    """
    Controls the source from which load the information of the dataset
    :param db_file: Database file whose tuples has to be extracted
    :param h5_file: Hierarchical Data Format file whose content has to be extracted
    :param musiXmatch_file: textual file whose content is the lyrics dataset
    :param data: data structure in which all the information are collected
    :return: a tuple which contains all the associations of each word into each track id
    """
    if not output_csv.exists():
        words = load_from_dataset(db_file, h5_file, musiXmatch_file, data)
        write_into_csv(data, words, output_csv, words_dataset_csv)
    words = read_from_csv(data, output_csv, words_dataset_csv)
    track_ids = list(map(lambda key: key[0], filter(lambda key: key[1] == "info", data.keys())))
    print("Fetched", len(data), "songs")

    return words, track_ids


def get_best_correlation(subjective_clustering, textual_clustering, tracks_ids, occurrences_ids) -> tuple:
    """
    Finds the best correlation between two clustering groups
    :param subjective_clustering: first clustering group
    :param textual_clustering: second clustering group
    :param tracks_ids: first clustering group instances by index
    :param occurrences_ids: second clustering group instances
    :return: tuple containing the best correlated instances and the cluster couple they belong to
    """
    global best_correlation, subjective_cluster_name, textual_cluster_name
    subjective_clusters = defaultdict(set)
    for i in range(0, len(subjective_clustering)):
        subjective_clusters[subjective_clustering[i]].add(tracks_ids[i][0])
    textual_clusters = defaultdict(set)
    for i in range(0, len(textual_clustering)):
        textual_clusters[textual_clustering[i]].add(occurrences_ids[i])
    best_correlation, subjective_cluster_name, textual_cluster_name = set(), str(), str()
    for subjective_cluster in subjective_clusters.keys():
        for textual_cluster in textual_clusters.keys():
            intersection = subjective_clusters[subjective_cluster].intersection(textual_clusters[textual_cluster])
            if len(intersection) > len(best_correlation):
                best_correlation, subjective_cluster_name, textual_cluster_name = intersection, subjective_cluster, textual_cluster

    return best_correlation, subjective_cluster_name, textual_cluster_name


def aggregate_clusters_data(tracks_examples, tracks_occurrences, track_ids, words) -> defaultdict:
    """
    Aggregate in a readable format all the information gathered in input
    :param tracks_examples: instances of a clustering group
    :param tracks_occurrences: instances of another clustering group
    :param track_ids: first clustering group instances by index
    :param words: list of the words contained in the lyrics dataset
    :return: dictionary whose key is a `track_id` and whose value is a list
     which first element is the subjective information stored and the others are couples (word, word_frequency)-like
    """
    stop_words = set(stopwords.words('english'))
    intersection_information = defaultdict(list)
    for track in tracks_occurrences:
        for intersection_track in best_correlation:
            if track_ids[track[0]] == intersection_track and words[int(track[1])] not in stop_words:
                intersection_information[intersection_track].append((words[int(track[1])], track[2]))
                if tracks_examples[track[0]][:-1] and \
                        tracks_examples[track[0]][:-1] not in intersection_information[intersection_track]:
                    intersection_information[intersection_track].insert(0, tracks_examples[track[0]][:-1])

    return intersection_information
