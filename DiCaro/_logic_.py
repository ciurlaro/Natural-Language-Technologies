import sqlite3, csv
from pathlib import Path
from DiCaro.MSongsDB.PythonSrc import hdf5_getters
from DiCaro._init_ import *


def loading_info(db_file, h5_file, data):
    conn = sqlite3.connect(str(db_file))
    q = "SELECT track_id, title, artist_name, artist_hotttnesss, artist_familiarity  FROM songs"
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


def get_infos_by_track_id(h5, track_id):
    for record in h5.root.analysis.songs.where('track_id=="' + track_id + '"'):
        return record["tempo"], record["loudness"] # , record["energy"], record["danceability"]


def get_infos_by_song_and_artist_id(h5, song_id, artist_id):
    for record in h5.root.metadata.songs.where('song_id=="' + song_id + '"', 'artist_id=="' + artist_id + '"'):
        return record["song_hotttnesss"], record["genre"].decode()


def get_lyrics(musiXmatch_file, data):
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


def load_from_dataset(db_file, h5_file, musiXmatch_file, data):
    print("Loading infos...")
    loading_info(db_file, h5_file, data)
    print("Getting lyrics...")
    return get_lyrics(musiXmatch_file, data)


def write_into_csv(data, words):
    writer = csv.writer(open("output.csv", "w", newline=''))
    for row in data.items():
        writer.writerow(row)

    writer = csv.writer(open("words.csv", "w", newline='', encoding="utf-8"))
    writer.writerow(words)


def read_from_csv(data):
    reader = csv.reader(open("output.csv"), delimiter=',')
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

    reader = csv.reader(open("words.csv", encoding="utf-8"), delimiter=',')
    for row in reader:
        return row


def pre_process_tracks(data):
    examples = []
    for keys in filter(lambda keys: keys[1] == "info", data.keys()):
        artist_hotttnesss = float(data[keys][2]) if data[keys][2] != "." else 0.0
        artist_familiarity = float(data[keys][3]) if data[keys][3] != "." else 0.0
        tempo = float(data[keys][4])
        loudness = float(data[keys][5])

        if artist_familiarity != 0 and artist_hotttnesss != 0 and tempo != 0 and loudness != 0:
            example = [tempo, loudness, artist_hotttnesss, artist_familiarity]
            examples.append(example)
    return examples


def pre_process_occurrences(data, track_ids):
    tracks_co_occurrences = []
    for track_lyrics in filter(lambda key: key[1] == "lyrics", data.keys()):
        for word_key in data[track_lyrics].keys():
            track_index = track_ids.index(track_lyrics[0])
            word = int(word_key) # words[int(word_key)] is the word
            count = data[track_lyrics][word_key]
            tracks_co_occurrences.append([track_index, word, count])
    return tracks_co_occurrences


def data_loading(data):
    if not (Path.cwd() / "output.csv").exists():
        words = load_from_dataset(db_file, h5_file, musiXmatch_file, data)
        write_into_csv(data, words)
    words = read_from_csv(data)
    track_ids = list(map(lambda key: key[0], filter(lambda key: key[1] == "info", data.keys())))
    print("Fetched", len(data), "songs")

    return words, track_ids