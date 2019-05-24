import random
from nltk.corpus import semcor
from nltk.corpus.reader.wordnet import Lemma


def semcor_extraction() -> tuple:
    sentences = []
    extracted = []

    for i in range(0, 10):
        elem = list(filter(lambda sentence_tree:
                           isinstance(sentence_tree.label(), Lemma) and
                           sentence_tree[0].label() == "NN", semcor.tagged_sents(tag='both')[i]))

        if elem:
            extracted.append(random.choice(elem))
            sentences.append(" ".join(semcor.sents()[i]))

    return sentences, extracted
