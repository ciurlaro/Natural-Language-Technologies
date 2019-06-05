from Radicioni.Corpus.SemCor import semcor_extraction
from Radicioni.Esercizio_2._logic_ import *
from Radicioni.Esercizio_2.lesk_algorithms import simplified_lesk, removes_stopwords_lesk


if __name__ == '__main__':
    """
    @:var disambiguation_words: list of polysemic terms to disambiguate 
    """
    print(" ---------------------------------------------------------------------------------------------------- \n")
    disambiguation_words = pre_process_sentences()
    replace_synonyms(disambiguation_words)
    print(" ---------------------------------------------------------------------------------------------------- \n")

    """
    @:var semcor_sentences: sentences taken from Semcore corpus
    @:var semcor_extracted: nouns taken from `Semcore_sentences`
    """
    semcor_sentences, semcor_extracted = semcor_extraction()

    target_senses_simplified, obtained_senses_simplified = \
        load_obtained_target_data(semcor_sentences, semcor_extracted, lesk_type='simplified')

    target_senses_stopwords, obtained_senses_stopwords = \
        load_obtained_target_data(semcor_sentences, semcor_extracted, lesk_type='stopwords')

    target_senses_extended, obtained_senses_extended = \
        load_obtained_target_data(semcor_sentences, semcor_extracted, lesk_type='extended')

    print("Simplified Lesk Accuracy:", calculate_accuracy(target_senses_simplified, obtained_senses_simplified))
    print("Stopwords Lesk Accuracy:", calculate_accuracy(target_senses_stopwords, obtained_senses_stopwords))
    print("Extended Lesk Accuracy:", calculate_accuracy(target_senses_extended, obtained_senses_extended))

    """
    @:var baseline_best_senses: list of synsets computed through baseline method
    """
    baseline_best_senses = []
    for i in range(0, len(semcor_sentences)):
        baseline_best_senses.append(str(baseline(semcor_extracted[i][0][0])))
    print("Baseline Accuracy with Simplified Lesk:", calculate_accuracy(baseline_best_senses, target_senses_simplified))
    print("Baseline Accuracy with Stopwords Lesk:", calculate_accuracy(baseline_best_senses, target_senses_stopwords))
    print("Baseline Accuracy with Extended Lesk:", calculate_accuracy(baseline_best_senses, target_senses_extended))
