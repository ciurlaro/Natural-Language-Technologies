from nltk.corpus import wordnet
from nltk.corpus.reader import Synset
from numpy import array, cov, std, float64
import sys, math
from scipy.stats import spearmanr, pearsonr


def get_max_wordnet_depth() -> int:
    # return max(max(len(hyp_path) for hyp_path in synset.hypernym_paths()) for synset in wordnet.all_synsets())
    return 20


def wp_similarity(word_1: str, word_2: str) -> float:

    max_lcs = 0.0
    for s1_words in wordnet.synsets(word_1):
        for s2_words in wordnet.synsets(word_2):
            for lcs in s1_words.lowest_common_hypernyms(s2_words):
                similarity = 2 * lcs.max_depth() / (s1_words.max_depth() + s2_words.max_depth())
                max_lcs = max(max_lcs, similarity)

    return max_lcs


def shortest_path(word_1: str, word_2: str) -> float:

    min_distance = sys.maxsize
    for s1_word in wordnet.synsets(word_1):
        for s2_word in wordnet.synsets(word_2):
            dist_s1_s2 = s1_word.shortest_path_distance(s2_word)
            if dist_s1_s2 is None:
                dist_s1_s2 = 2 * get_max_wordnet_depth()
            min_distance = min(dist_s1_s2, min_distance)

    similarity = 2 * get_max_wordnet_depth() - min_distance
    return similarity


def lc_similarity(word_1: str, word_2: str) -> float:
    max_similarity = 0
    min_distance = sys.maxsize
    for s1_word in wordnet.synsets(word_1):
        for s2_word in wordnet.synsets(word_2):
            dist_s1_s2 = s1_word.shortest_path_distance(s2_word)
            if dist_s1_s2 is not None:
                if dist_s1_s2 > 0:
                    similarity = -(math.log(dist_s1_s2 / (2 * 20)) )
                else:
                    similarity = -(math.log(1 / (2 * 20 + 1)))
            else:
                similarity = 0

            max_similarity = max(max_similarity, similarity)

    # similarity = - math.log( (min_distance + 1) / (2 * get_max_wordnet_depth() + 1))
    return max_similarity



def pearson_correlation_coefficient(word_sim_res: list, obtained_res: list):
    targets = array(word_sim_res).astype(float)
    results = array(obtained_res).astype(float)

    return cov(targets, results)[0][1] / std(targets, dtype=float64) * std(results, dtype=float64)


def spearman_rank_correlation_coefficient(word_sim_res: list, obtained_res: list):
    return spearmanr(word_sim_res, obtained_res)[0]