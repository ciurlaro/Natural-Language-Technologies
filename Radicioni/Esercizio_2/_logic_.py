import re

from nltk.corpus import wordnet
from nltk.corpus.reader import Synset
from sklearn.metrics import accuracy_score
from Radicioni.Esercizio_2._init_ import Lesk_sentences
from Radicioni.Esercizio_2.lesk_algorithms import simplified_lesk


def pre_process_sentences() -> list:
    """
    Takes `Lesk sentences` list and isolates from it the polysemic words contained in each sentence
    :return: a list of polysemic words
    """
    disambiguation_words = []
    for i in range(0, len(Lesk_sentences)):
        for elem in Lesk_sentences[i].split():
            if elem.startswith("**"):
                polysemic_term = re.sub(r'[^\w\s]', '', elem)
                Lesk_sentences[i] = Lesk_sentences[i].replace(elem, polysemic_term)
                disambiguation_words.append(polysemic_term)
    return disambiguation_words


def replace_synonyms(disambiguation_words: list, verbose=True):
    """
    Takes the disambiguation words list and substitutes them in each `Lesk sentences` list sentence  with a list of
    synonyms, taken from the Simplified Lesk returned Synset
    :param disambiguation_words: a list of polysemic words
    :param verbose: specifies if prints are needed
    :return:
    """
    for i in range(0, len(Lesk_sentences)):
        synset = simplified_lesk(disambiguation_words[i], Lesk_sentences[i])
        if verbose: print("Best sense, given this sentence: ", synset)
        Lesk_sentences[i] = Lesk_sentences[i].replace(disambiguation_words[i],
                                                      str(synset.lemmas()))
        if verbose: print(Lesk_sentences[i])


def load_obtained_target_data(semcor_sentences: list, semcor_extracted:list):
    """
    Fills target and obtined senses lists
    :param semcor_sentences: sentences taken from semcore corpus
    :param semcor_extracted: nouns taken from `semcore_sentences`
    :return: Tuple containing synsets taken from semcore words and synsets obtainet through Lesk algorithm
    """
    target_senses, obtained_senses = [], []
    for i in range(0, len(semcor_sentences)):
        obtained_senses.append(str(simplified_lesk(semcor_extracted[i][0][0], semcor_sentences[i])))
        target_senses.append(str(semcor_extracted[i].label().synset()))

    return target_senses, obtained_senses


def calculate_accuracy(obtained_senses, target_senses) -> float:
    """
    Computes the accuracy between obtained and computed data
    :param obtained_senses: list of senses computed
    :param target_senses: list of expected senses taken from semcore
    :return: accuracy value
    """
    simplified_accuracy = accuracy_score(obtained_senses, target_senses)
    return simplified_accuracy


def baseline(word: str) -> Synset:
    """
    Computes the baseline disambiguation sense (frequency based)
    :param word: word to disambiguate
    :return: most frequent synset in wordnet of `word`
    """
    try:
        return wordnet.synsets(word)[0]
    except:
        return Synset(None)
