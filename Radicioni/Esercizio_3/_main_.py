from Radicioni.Esercizio_3._logic_ import *
import pprint


def main():
    annotated_dict = select_lines()
    nasari_dict = load_data_from_file()
    sem_eval_dict = load_data_from_sem_eval()

    # pprint.pprint(nasari_dict)

    for concepts in annotated_dict:
        for concept in concepts:
            synset_concepts = sem_eval_dict[concept]

            for sense in synset_concepts:
                if sense in nasari_dict:
                    sem_eval_dict[concept][sense] = nasari_dict[sense]

    '''Manca il synset bn:00012827n all'interno del file. Cosa facciamo?'''

    for concepts in annotated_dict:
        concept_1, concept_2 = best_sense_identification(concepts[0], concepts[1], sem_eval_dict)
        print("Best senses for", concepts[0],  "and", concepts[1], "are:",
                                  concept_1, "(" , get_description(nasari_dict, concept_1), ")",
                                  concept_2 ,"(" , get_description(nasari_dict, concept_2), ")")



main()
