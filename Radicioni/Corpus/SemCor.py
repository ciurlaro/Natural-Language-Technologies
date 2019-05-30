import random
from nltk.corpus import semcor
from nltk.corpus.reader.wordnet import Lemma
from Radicioni.Esercizio_2._init_ import sentence_number


def semcor_extraction() -> tuple:
    sentences = []
    extracted = []

    for i in range(0, sentence_number):
        elem = list(filter(lambda sentence_tree:
                           isinstance(sentence_tree.label(), Lemma) and
                           sentence_tree[0].label() == "NN", semcor.tagged_sents(tag='both')[i]))

        if elem:
            extracted.append(random.choice(elem))
            sentences.append(" ".join(semcor.sents()[i]))

    return sentences, extracted
