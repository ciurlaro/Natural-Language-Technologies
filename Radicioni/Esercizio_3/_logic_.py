from collections import defaultdict
from pathlib import Path
from Radicioni.Esercizio_3.sem_eval_mapper import cognome
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def select_lines() -> dict:
    """
    Loads data from file `it.test.data.txt` into `eval_dict`
    :return: eval_dict: dictionary whose key is a tuple cointaining two words, and whose value is an annotated value
    """

    lines = cognome().split('-')
    with open(Path.cwd() / "it.test.data.txt", encoding='utf-8') as input_file:
        input_reader = input_file.readlines()

        eval_dict = {}
        for i in range(int(lines[0]) - 1, int(lines[1])):
            line = input_reader[i][:-1].split('\t')
            eval_dict[line[0], line[1]] = line[2]

    return eval_dict


def load_data_from_file() -> dict:
    """
    Loads data from file `mini_NASARI.tsv` into `nasari_dict`
    :return: nasari_dict: a dictionary whose key is a babel synset id, and whose value is a tuple containing a
             description of the babel synset id and its corresponding nasari vector
    """

    nasari_dict = {}
    with open(Path.cwd() / "mini_nasari" / "mini_NASARI.tsv", encoding="utf-8") as nasari_file:
        for row in nasari_file:
            line = row.split("\t")
            key = line[0].split("__")
            nasari_dict[key[0]] = (key[1], line[1:-1])

    return nasari_dict


def load_data_from_sem_eval() -> defaultdict:
    """
    Loads data from file `SemEval17_IT_senses2synsets.txt` into `s2sdict`
    :return: s2sdict: a dictionary whose key is the semEval term, and whose value is a new defaultdict.
             This latter one has as key a bebel synset id, and as value its nasari vector
    """

    s2sdict = defaultdict(str)
    with open(Path.cwd() / "SemEval17_IT_senses2synsets.txt", encoding="utf-8") as sem_eval_s2s_file:
        for row in sem_eval_s2s_file:
            if row[0] == "#":
                key = row[1:-1]
                s2sdict[key] = defaultdict(str)
            else:
                s2sdict[key][(row.split("\n")[:-1])[0]] = None

    return s2sdict


def update_sem_eval_dict(sem_eval_dict: defaultdict, annotated_dict: dict, nasari_dict: dict):
    """
    Updates sem_eval_dict associating to each babel synset id its nasari vector
    :param sem_eval_dict: dict to update
    :param annotated_dict: annotated dict
    :param nasari_dict: nasari dict
    """
    for concepts in annotated_dict:
        for concept in concepts:
            synset_concepts = sem_eval_dict[concept]

            for sense in synset_concepts:
                if sense in nasari_dict:
                    sem_eval_dict[concept][sense] = nasari_dict[sense]


def best_senses_identification(concept1: str, concept2: str, sem_eval_dict: defaultdict) -> tuple:
    """
    Finds the best senses given two different concepts using data contained in sem_eval_dict and computing
    cosine similarity
    :param sem_eval_dict:
    :param concept1: first concept
    :param concept2: second concept
    :return: tuple of best senses
    """

    max_cos_sim = 0.0
    best_senses = (None, None)

    for bn_1 in sem_eval_dict[concept1]:
        if (sem_eval_dict[concept1][bn_1]) is not None:
            nasari_vector_1 = (sem_eval_dict[concept1][bn_1])[1]
            for bn_2 in sem_eval_dict[concept2]:
                if (sem_eval_dict[concept2][bn_2]) is not None:
                    nasari_vector_2 = (sem_eval_dict[concept2][bn_2])[1]
                    cosine_sim = compute_cosine_similarity(nasari_vector_1, nasari_vector_2)
                    if cosine_sim > max_cos_sim:
                        max_cos_sim = cosine_sim
                        best_senses = (bn_1, bn_2)

    return best_senses


def compute_cosine_similarity(nasari_vector_1, nasari_vector_2) -> np.array:
    """
    Computes cosine similarity between two nasari vectors
    :param nasari_vector_1: first nasari vector
    :param nasari_vector_2: second nasari vector
    :return: cosine_similarity between `nasari_vector_1` and `nasari_vector_2`

    """
    # The usual creation of arrays produces wrong format (as cosine_similarity works on matrices)
    x = np.array(nasari_vector_1)
    y = np.array(nasari_vector_2)

    # Need to reshape these
    x = x.reshape(1, -1)
    y = y.reshape(1, -1)

    # Now we can compute similarities
    return cosine_similarity(x, y)


def get_description(nasari_dict: dict, babel_synset: str) -> dict:
    """
    Gets the description of the babel synset given
    :param nasari_dict: nasari_dict
    :param babel_synset: string of babel synset id
    :return: Description if it exists, "None" otherwise
    """
    return nasari_dict[babel_synset][0] if babel_synset else "None"


