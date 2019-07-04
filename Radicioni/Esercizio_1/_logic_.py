from nltk.corpus import wordnet
from numpy import array, cov, std, float64
import sys, math
from scipy.stats import rankdata


def get_max_wordnet_depth(fast_computing: bool = True) -> int:
    """
    Get Wordnet's maximum taxonomy depth.
    The method returns a static value, which is always 20.
    :param fast_computing: returns 20
    :return: Wordnet's maximum taxonomy depth value
    """
    return 20 if fast_computing \
        else max(max(len(hyp_path) for hyp_path in synset.hypernym_paths()) for synset in wordnet.all_synsets())


def wp_similarity(word_1: str, word_2: str) -> float:
    """
    Compute Wu & Palmer similarity score, given word_1 and word_2
    :param word_1: first word needed to compute the coefficient
    :param word_2: second word needed to compute the coefficient
    :return: Wu & Palmer similarity score, always ∈ [0, 1]
    """
    max_lcs = 0.0
    for s1_words in wordnet.synsets(word_1):
        for s2_words in wordnet.synsets(word_2):
            for lcs in s1_words.lowest_common_hypernyms(s2_words):
                similarity = 2 * lcs.max_depth() / (s1_words.max_depth() + s2_words.max_depth())
                max_lcs = max(max_lcs, similarity)
    return max_lcs


def lc_similarity(word_1: str, word_2: str, normalized: bool = True) -> float:
    """
    Compute Leacock & Chodorov similarity score, given word_1 and word_2
    :param word_1: first word needed to compute the coefficient
    :param word_2: second word needed to compute the coefficient
    :param normalized: normalizes in [0, 1] the score, if True
    :return: Leacock & Chodorov similarity score
    """
    max_similarity = 0
    for s1_word in wordnet.synsets(word_1):
        for s2_word in wordnet.synsets(word_2):
            dist_s1_s2 = s1_word.shortest_path_distance(s2_word)
            if dist_s1_s2 is not None:
                if dist_s1_s2 > 0:
                    similarity = -(math.log(dist_s1_s2 / (2 * get_max_wordnet_depth())))
                else:
                    similarity = -(math.log(1 / (2 * get_max_wordnet_depth() + 1)))
            else:
                similarity = 0

            max_similarity = max(max_similarity, similarity)

    return max_similarity / math.log(2 * get_max_wordnet_depth() + 1) if normalized else max_similarity


def sp_similarity(word_1: str, word_2: str, normalized: bool = True) -> float:
    """
    Compute shortest path similarity score, given word_1 and word_2
    :param word_1: first word needed to compute the coefficient
    :param word_2: second word needed to compute the coefficient
    :param normalized: normalizes in [0, 1] the score, if True
    :return: shortest path similarity score
    """
    min_distance = sys.maxsize
    for s1_word in wordnet.synsets(word_1):
        for s2_word in wordnet.synsets(word_2):
            dist_s1_s2 = s1_word.shortest_path_distance(s2_word)
            if dist_s1_s2 is None:
                dist_s1_s2 = 2 * get_max_wordnet_depth()
            min_distance = min(dist_s1_s2, min_distance)

    similarity = 2 * get_max_wordnet_depth() - min_distance
    return similarity / (2 * get_max_wordnet_depth()) if normalized else similarity


def pearson_correlation_coefficient(target_values: list, obtained_values: list) -> float:
    """
    Compute the Pearson correlation coefficient between target and obtained values
    :param target_values: list of expected values
    :param obtained_values: list of obtained values
    :return: Pearson correlation coefficient between target and obtained values
    """
    targets = array(target_values).astype(float)
    results = array(obtained_values).astype(float)

    return cov(targets, results)[0][1] / (std(targets, dtype=float64) * std(results, dtype=float64))


def spearman_rank_correlation_coefficient(target_values: list, obtained_values: list) -> float:
    """
    Compute the Spearman rank correlation coefficient between target and obtained values
    :param target_values: list of expected values
    :param obtained_values: list of obtained values
    :return: Spearman rank correlation coefficient between target and obtained values
    """
    targets = array(rankdata(target_values)).astype(float)
    results = array(rankdata(obtained_values)).astype(float)

    return cov(targets, results)[0][1] / (std(targets, dtype=float64) * std(results, dtype=float64))
