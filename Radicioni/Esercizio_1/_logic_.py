from nltk.corpus import wordnet
from nltk.corpus.reader import Synset


def get_max_wordnet_depth() -> int:
    # return max(max(len(hyp_path) for hyp_path in synset.hypernym_paths()) for synset in wordnet.all_synsets())
    return 20


def wp_similarity(word_1: str, word_2: str) -> float:

    max_lcs = 0.0
    for s1_words in wordnet.synsets(word_1):
        for s2_words in wordnet.synsets(word_2):
            for lcs in s1_words.lowest_common_hypernyms(s2_words):
                similarity = 2*lcs.max_depth()/(s1_words.max_depth() + s2_words.max_depth())
                max_lcs = max(max_lcs, similarity)

    return max_lcs


def shortest_path(word_1: str, word_2: str) -> float:

    max_similarity = 0.0
    for s1_word in wordnet.synsets(word_1):
        for s2_word in wordnet.synsets(word_2):
            dist_s1_s2 = s1_word.shortest_path_distance(s2_word)
            if dist_s1_s2 is None: break
            similarity = 2*get_max_wordnet_depth() - dist_s1_s2
            max_similarity = max(max_similarity, similarity)

    return max_similarity

