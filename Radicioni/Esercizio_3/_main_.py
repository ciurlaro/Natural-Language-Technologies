from Radicioni.Esercizio_3._logic_ import *


if __name__ == '__main__':
    """
    @:var annotated_dict: annotated dictionary
    @:var nasari_dict: nasari dictionary
    @:var sem_eval_dict: sem_eval dictionary
    """
    annotated_dict = select_lines()
    nasari_dict = load_data_from_file()
    sem_eval_dict = load_data_from_sem_eval()

    update_sem_eval_dict(sem_eval_dict, annotated_dict, nasari_dict)

    for concepts in annotated_dict:
        concept_1, concept_2 = best_senses_identification(concepts[0], concepts[1], sem_eval_dict)
        print("Best senses for", concepts[0],  "and", concepts[1], "are:",
                                  concept_1, "[" , get_description(nasari_dict, concept_1), "]",
                                  concept_2 ,"[" , get_description(nasari_dict, concept_2), "]")
