import re
from nltk.corpus import wordnet
from nltk.corpus.reader import Synset
from sklearn.metrics import accuracy_score
from Radicioni.Esercizio_2._init_ import Lesk_sentences
from Radicioni.Esercizio_2.lesk_algorithms import simplified_lesk, removes_stopwords_lesk, extended_context_lesk


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
        if verbose:
            print("Current sentence:", "'" + Lesk_sentences[i] + "'")
            print("Best sense found:", synset)
            print("Best sense definition:", synset.definition())
        Lesk_sentences[i] = Lesk_sentences[i].replace(disambiguation_words[i],
                                                      str(synset.lemmas()))
        if verbose: print("Rewriting current sentence with synonyms:", "'" + Lesk_sentences[i] + "'\n")


def load_obtained_target_data(semcor_sentences: list, semcor_extracted :list, lesk_type: str = 'simplified'):
    """
    Fills target and obtined senses lists
    :param semcor_sentences: sentences taken from Semcore corpus
    :param semcor_extracted: nouns taken from `Semcore_sentences`
    :param lesk_type: type of lesk algorithm to be used. Possible values are 'simplified', 'stopwords' and 'extended'.
    :return: Tuple containing synsets taken from Semcore words and synsets obtainet through Lesk algorithm
    """

    precondition_values = ['simplified', 'stopwords', 'extended']
    if lesk_type not in precondition_values:
        raise ValueError('Possible values are "'"simplified"'", "'"stopwords"'" and "'"extended"'"')
    else:
        target_senses, obtained_senses = [], []
        for i in range(0, len(semcor_sentences)):
            if lesk_type == 'simplified':
                best_sense = str(simplified_lesk(semcor_extracted[i][0][0], semcor_sentences[i]))
            elif lesk_type == 'stopwords':
                best_sense = str(removes_stopwords_lesk(semcor_extracted[i][0][0], semcor_sentences[i]))
            else:
                best_sense = str(extended_context_lesk(semcor_extracted[i][0][0], semcor_sentences[i]))

            obtained_senses.append(best_sense)
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
