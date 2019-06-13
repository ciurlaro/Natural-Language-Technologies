from DiCaro._logic_ import *

'''
Environment settings
'''
dataset_folder = Path.cwd() / 'Dataset'
musiXmatch_file = dataset_folder / 'musiXmatch' / "mxm_dataset_train.txt"
db_file = dataset_folder / 'MillionSongSubset' / 'AdditionalFiles' / 'subset_track_metadata.db'
h5_file = dataset_folder / 'MillionSongSubset' / 'AdditionalFiles' / 'subset_msd_summary_file.h5'

subj_clustering_components = ["tempo", "loudness", "artist_hotttnesss", "artist_familiarity"]
text_clustering_components = ["track_id", "word", "count"]


'''
Data loading
'''
data = {}    # print(data[('TRAAABD128F429CF47', 'info')]
words, track_ids = data_loading(db_file, h5_file, musiXmatch_file, data)