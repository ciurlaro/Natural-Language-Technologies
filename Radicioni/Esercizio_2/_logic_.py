import re
from sklearn.metrics import accuracy_score
from Radicioni.Esercizio_2._init_ import simplified_lesk_sentences
from Radicioni.Esercizio_2.simplified_lesk import simplified_lesk


def pre_process_sentences():
    disambiguation_words = []
    for i in range(0, len(simplified_lesk_sentences)):
        for elem in simplified_lesk_sentences[i].split():
            if elem.startswith("**"):
                polysemic_term = re.sub(r'[^\w\s]', '', elem)
                simplified_lesk_sentences[i] = simplified_lesk_sentences[i].replace(elem, polysemic_term)
                disambiguation_words.append(polysemic_term)
    return disambiguation_words


def replace_synonyms(disambiguation_words):
    for i in range(0, len(simplified_lesk_sentences)):
        synset = simplified_lesk(disambiguation_words[i], simplified_lesk_sentences[i])  # Lesk
        print("Best sense founded for this sentence: ", synset)
        simplified_lesk_sentences[i] = simplified_lesk_sentences[i].replace(disambiguation_words[i], str(synset.lemmas()))
        print(simplified_lesk_sentences[i])


def calculate_accuracy(best_senses, semcor_senses):
    simplified_accuracy = accuracy_score(best_senses, semcor_senses)
    return simplified_accuracy
