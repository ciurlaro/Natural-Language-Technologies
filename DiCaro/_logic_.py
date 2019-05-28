import sqlite3, csv

from DiCaro.MSongsDB.PythonSrc import hdf5_getters


def loading_info(db_file, h5_file, data):
    conn = sqlite3.connect(str(db_file))
    q = "SELECT track_id, title, artist_name  FROM songs"
    res = conn.execute(q)

    h5 = hdf5_getters.open_h5_file_read(h5_file)

    for row in res:
        track_id = row[0]
        title = row[1]
        artist_name = row[2]
        data[track_id, "info"] = title, artist_name, get_infos_by_track_id(h5, track_id) \
                                 # , get_infos_by_song_and_artist_id(h5, song_id, artist_id)
    h5.close()


def get_infos_by_track_id(h5, track_id):
    for record in h5.root.analysis.songs.where('track_id=="' + track_id + '"'):
        return record["tempo"], record["loudness"] # , record["energy"], record["danceability"]


'''
def get_infos_by_song_and_artist_id(h5, song_id, artist_id):
    for record in h5.root.metadata.songs.where('song_id=="' + song_id + '"', 'artist_id=="' + artist_id + '"'):
        return record["song_hotttnesss"], record["genre"].decode()
'''


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


def load_from_dataset(db_file, h5_file, musiXmatch_file, data):
    print("Loading infos...")
    loading_info(db_file, h5_file, data)
    print("Getting lyrics...")
    get_lyrics(musiXmatch_file, data)


def write_into_csv(data):
    writer = csv.writer(open("output.csv", "w", newline=''))
    for row in data.items():
        writer.writerow(row)


def read_from_csv(data):
    reader = csv.reader(open("output.csv"), delimiter=',')
    for row in reader:
        keys = row[0][1:-1].split(", ")
        values = row[1][1:-1].split(", ")
        value = []

        # print(keys[0][1:-1], keys[1][1:-1])
        if keys[1][1:-1] == "info":
            for elem in values:
                # print(value[1:-1])
                value.append(elem[1:-1])

            data[keys[0][1:-1], "info"] = value

        elif keys[1][1:-1] == "lyrics":
            frequencies = {}
            for words in values:
                idx, cnt = words.split(": ")
                frequencies[idx[1:-1]] = cnt[1:-1]

            data[keys[0][1:-1], "lyrics"] = frequencies
