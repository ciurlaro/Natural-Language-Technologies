from Radicioni.Corpus.SemCor import semcor_extraction
from Radicioni.Esercizio_2._logic_ import pre_process_sentences, replace_synonyms, calculate_accuracy
from Radicioni.Esercizio_2.simplified_lesk import simplified_lesk

disambiguation_words = pre_process_sentences()
replace_synonyms(disambiguation_words)

print(" ---------------------------------------------------------------------------------------------------- ")

semcor_sentences, semcor_extracted = semcor_extraction()
best_senses = []
semcor_senses = []

for i in range(0, len(semcor_sentences)):
  best_senses.append(str(simplified_lesk(semcor_extracted[i][0][0], semcor_sentences[i])))
  semcor_senses.append(str(semcor_extracted[i].label().synset()))

print(calculate_accuracy(best_senses, semcor_senses))
