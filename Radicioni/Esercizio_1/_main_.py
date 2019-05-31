from pathlib import Path

from nltk.corpus import wordnet

from Radicioni.Esercizio_1.WordSimReader import word_sim_reader
from Radicioni.Esercizio_1._logic_ import *


def main():

    word_sim = word_sim_reader(Path.cwd() / "WordSim353.csv")

    target_values = []
    wp_res = []
    lc_res = []
    sp_res = []

    for row in word_sim:
        wp_res.append(wp_similarity(row[0], row[1]))
        lc_res.append(lc_similarity(row[0], row[1]))
        sp_res.append(shortest_path(row[0], row[1]))
        target_values.append(float(row[2]) / 10)
        
    print(pearson_correlation_coefficient(target_values, wp_res))
    '''print(pearson_correlation_coefficient(target_values, lc_res))
    print(pearson_correlation_coefficient(target_values, sp_res))'''

    print(spearman_rank_correlation_coefficient(target_values, wp_res))
    '''print(spearman_rank_correlation_coefficient(target_values, lc_res))
    print(spearman_rank_correlation_coefficient(target_values, sp_res))'''


main()
