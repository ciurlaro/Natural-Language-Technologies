from collections import defaultdict
from pathlib import Path
from Radicioni.Esercizio_3.sem_eval_mapper import cognome
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def select_lines() -> dict:
    """

    :return:
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

    :return:
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

    :return:
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


def best_sense_identification(concept1: str, concept2: str, sem_eval_dict: defaultdict) -> tuple:
    """

    :param sem_eval_dict:
    :param concept1:
    :param concept2:
    :return:
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


def compute_cosine_similarity(nasari_vector_1, nasari_vector_2):
    """

    :param nasari_vector_1:
    :param nasari_vector_2:
    :return:
    """
    # The usual creation of arrays produces wrong format (as cosine_similarity works on matrices)
    x = np.array(nasari_vector_1)
    y = np.array(nasari_vector_2)

    # Need to reshape these
    x = x.reshape(1, -1)
    y = y.reshape(1, -1)

    # Now we can compute similarities
    return cosine_similarity(x, y)


def get_description(dict, babel_synset):
    return dict[babel_synset][0] if babel_synset else "None"


