from Radicioni.Corpus.SemCor import semcor_extraction
from Radicioni.Esercizio_2._logic_ import *
from Radicioni.Esercizio_2.lesk_algorithms import simplified_lesk, removes_stopwords_lesk


if __name__ == '__main__':
    """
    @:var disambiguation_words: list of polysemic terms to disambiguate 
    """
    disambiguation_words = pre_process_sentences()
    replace_synonyms(disambiguation_words)
    print(" ---------------------------------------------------------------------------------------------------- ")

    """
    @:var semcor_sentences: sentences taken from semcore corpus
    @:var semcor_extracted: nouns taken from `semcore_sentences`
    """
    semcor_sentences, semcor_extracted = semcor_extraction()
    target_senses, obtained_senses = load_obtained_target_data(semcor_sentences, semcor_extracted)
    print("Simplified Lesk Accuracy:", calculate_accuracy(obtained_senses, target_senses))

    """
    @:var baseline_best_senses: list of synsets computed through baseline method
    """
    baseline_best_senses = []
    for i in range(0, len(semcor_sentences)):
        baseline_best_senses.append(str(baseline(semcor_extracted[i][0][0])))
    print("Baseline Accuracy:", calculate_accuracy(baseline_best_senses, target_senses))
