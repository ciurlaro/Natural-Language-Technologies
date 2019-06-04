from nltk.corpus import wordnet, stopwords
from nltk.corpus.reader.wordnet import Synset


def simplified_lesk(word: str, sentence: str) -> Synset:
    """
    Computes the max_overlap to understand what is the best sense
    :param word: word to dissmbiguate
    :param sentence: sentence in which word appears
    :return: Synset that maximizes the overlap
    """
    synsets = wordnet.synsets(word)

    try:
        best_sense = wordnet.synsets(word)[0]

        max_overlap = 0
        context = set(sentence.split(" "))

        for sense in synsets:
            signature = set(sense.definition().split(" "))
            for sentence in sense.examples():
                signature.union(sentence.split(" "))

            overlap = len(signature.intersection(context))

            if overlap > max_overlap:
                max_overlap = overlap
                best_sense = sense

        return best_sense

    except:
        return Synset(None)


def removes_stopwords_lesk(word: str, sentence: str) -> Synset:
    """
    Computes the max_overlap to understand what is the best sense, eliminating the stopwords
    :param word: word to dissmbiguate
    :param sentence: sentence in which word appears
    :return: Synset that maximizes the overlap
    """
    stopwords_set = set(stopwords.words('english'))
    synsets = wordnet.synsets(word)

    try:
        best_sense = wordnet.synsets(word)[0]

        max_overlap = 0
        context = set(sentence.split(" "))

        for sense in synsets:
            signature = set(sense.definition().split(" "))
            for sentence in sense.examples():
                signature.union(sentence.split(" "))

            signature.difference(stopwords_set)
            overlap = len(signature.intersection(context))

            if overlap > max_overlap:
                max_overlap = overlap
                best_sense = sense

        return best_sense

    except:
        return Synset(None)


def extended_context_lesk(word: str, sentence: str) -> Synset:
    """
    Computes the max_overlap to understand what is the best sense, using hypernyms and hyponyms
    :param word: the word to be disambiguated
    :param sentence: input sentence which contains param 'word'
    :return: best_sense, which is a Wordnet Synset, for param 'word'
    """
    stopwords_set = set(stopwords.words('english'))

    synsets = wordnet.synsets(word)
    context = set(sentence.split())

    max_overlap = 0
    best_sense = synsets[0]

    for sense in synsets:
        # get the synset meaning
        signature = set(sense.definition().split(" "))

        for hypernym in sense.hypernyms():
            signature = signature.union(hypernym.definition().split(" "))
        for hyponym in sense.hyponyms():
            signature = signature.union(hyponym.definition().split(" "))

        signature.difference(stopwords_set)

        # compute the overlap between synset signature and synset context
        overlap = len(signature.intersection(context))

        if overlap > max_overlap:
            max_overlap = overlap
            best_sense = sense

    return best_sense
