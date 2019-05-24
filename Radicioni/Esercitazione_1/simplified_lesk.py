from nltk.corpus import wordnet
from nltk.corpus.reader.wordnet import Synset

# 1 - Pos tagging
# 2 - Features extraction (class of features: bag-of-word/ collocational)

# Collocational approach
# Collocation: parola o frase in una specifica posizione in relazione alla parola target
# Ad ogni parola del contesto associa una collocation ed il Pos Tag


# Bag of word approach
# Corpus, Parola target
# 1) Prendi dal Corpus le frasi in cui compare la parola target
# 2) Estrai le x più frequenti parole
# 3) Verifichi la presenza delle parole estratte nel contesto (1 presente/0 no)


def simplified_lesk(word: str, sentence: str) -> Synset:
    #sense.definition()
    synsets = wordnet.synsets(word)
    best_sense = wordnet.synsets(word)[0]
    max_overlap = 0
    context = set(sentence.split(" "))

    for sense in synsets:
        signature = set(sense.definition().split(" "))      # examples
        overlap = len(signature - (signature - context))
        if overlap > max_overlap:
            max_overlap = overlap
            best_sense = sense

    return best_sense

