from nltk.corpus import wordnet, stopwords
from nltk.corpus.reader.wordnet import Synset
from nltk.stem import WordNetLemmatizer


def simplified_lesk(word: str, sentence: str) -> Synset:
    """
    Computes the max_overlap to understand what is the best sense
    :param word: word to dissmbiguate
    :param sentence: sentence in which word appears
    :return: Synset that maximizes the overlap
    """
    synsets = wordnet.synsets(word)

    try:
        lemmatizer = WordNetLemmatizer()

        best_sense = wordnet.synsets(word)[0]
        max_overlap = 0
        context = set(lemmatizer.lemmatize(word)for word in sentence.split(" "))

        for sense in synsets:
            signature = set(lemmatizer.lemmatize(word)for word in sense.definition().split(" "))
            for example in sense.examples():
                signature.union(set(lemmatizer.lemmatize(word)for word in example.split(" ")))

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
        lemmatizer = WordNetLemmatizer()

        best_sense = wordnet.synsets(word)[0]
        max_overlap = 0
        context = set(lemmatizer.lemmatize(word)for word in sentence.split(" "))

        for sense in synsets:
            signature = set(lemmatizer.lemmatize(word)for word in sense.definition().split(" "))
            for example in sense.examples():
                signature.union(set(lemmatizer.lemmatize(word)for word in example.split(" ")))

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

    try:
        lemmatizer = WordNetLemmatizer()

        best_sense = wordnet.synsets(word)[0]
        max_overlap = 0
        context = set(lemmatizer.lemmatize(word)for word in sentence.split(" "))

        for sense in synsets:
            signature = set(lemmatizer.lemmatize(word)for word in sense.definition().split(" "))

            for example in sense.examples():
                signature.union(set(lemmatizer.lemmatize(word)for word in example.split(" ")))

            for hypernym in sense.hypernyms():
                signature = signature.union(set(lemmatizer.lemmatize(word)for word in hypernym.definition().split(" ")))

            for hyponym in sense.hyponyms():
                signature = signature.union(set(lemmatizer.lemmatize(word)for word in hyponym.definition().split(" ")))

            signature.difference(stopwords_set)

            overlap = len(signature.intersection(context))
            if overlap > max_overlap:
                max_overlap = overlap
                best_sense = sense

        return best_sense

    except:
        return Synset(None)

