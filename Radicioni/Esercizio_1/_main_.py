from pathlib import Path

from nltk.corpus import wordnet

from Radicioni.Esercizio_1.WordSimReader import word_sim_reader
from Radicioni.Esercizio_1._logic_ import get_max_wordnet_depth, wp_similarity, shortest_path


def main():
    '''
    word_sim = word_sim_reader(Path.cwd() / "WordSim353.csv")
    for row in word_sim:
        print(row)
    '''

    print(shortest_path("shoes", "pizza"))



main()
