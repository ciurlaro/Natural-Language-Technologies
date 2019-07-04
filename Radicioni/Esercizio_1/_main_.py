from pathlib import Path
from Radicioni.Esercizio_1.WordSimReader import word_sim_reader
from Radicioni.Esercizio_1._logic_ import *


if __name__ == '__main__':
    word_sim = word_sim_reader(Path.cwd() / "WordSim353.csv")

    """
    @:var target_values: list of gold standard scores 
    @:var wp_res: list of Wu & Palmer similarity scores obtained
    @:var lc_res: list of Leacock & Chodorov similarity scores obtained
    @:var sp_res: list of shortest path similarity scores obtained
    """
    target_values, wp_res, lc_res, sp_res = [], [], [], []

    for row in word_sim:
        wp_res.append(wp_similarity(row[0], row[1]))
        lc_res.append(lc_similarity(row[0], row[1]))
        sp_res.append(sp_similarity(row[0], row[1]))
        target_values.append(float(row[2]) / 10)
    print('Pearson Correlation: ')
    print("WP: ", pearson_correlation_coefficient(target_values, wp_res))
    print("LC: ", pearson_correlation_coefficient(target_values, lc_res))
    print("SP: ", pearson_correlation_coefficient(target_values, sp_res))

    print('Spearman Correlation: ')
    print("WP: ", spearman_rank_correlation_coefficient(target_values, wp_res))
    print("LC: ", spearman_rank_correlation_coefficient(target_values, lc_res))
    print("SP: ", spearman_rank_correlation_coefficient(target_values, sp_res))

