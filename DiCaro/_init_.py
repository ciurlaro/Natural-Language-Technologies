from DiCaro._logic_ import *
from pathlib import Path


dataset_folder = Path.cwd() / 'Dataset'
musiXmatch_file = dataset_folder / 'musiXmatch' / "mxm_dataset_train.txt"
db_file = dataset_folder / 'MillionSongSubset' / 'AdditionalFiles' / 'subset_track_metadata.db'
h5_file = dataset_folder / 'MillionSongSubset' / 'AdditionalFiles' / 'subset_msd_summary_file.h5'

data = {}
read_from_csv(data)
# load_from_dataset(db_file, h5_file, musiXmatch_file, data)
# write_into_csv(data)
# print(data[('TRAAABD128F429CF47', 'lyrics')], data[('TRACCVZ128F4291A8A', 'lyrics')])
print("Fetched", len(data), "songs")

examples = []
for keys in filter(lambda keys: keys[1] == "info", data.keys()):
    if float(data[keys][2]) != 0 and float(data[keys][3]) != 0:
        examples.append((float(data[keys][2]), float(data[keys][3])))



####################################################################################################
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA


pca = PCA(n_components=2)
X = pca.fit_transform(examples)

# create scatter plot
plt.scatter(X[:, 0], X[:, 1], cmap=plt.cm.get_cmap('gist_rainbow', 10))
plt.show()

