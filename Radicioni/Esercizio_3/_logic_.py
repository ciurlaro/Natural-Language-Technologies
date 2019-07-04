import itertools
from collections import defaultdict
from pathlib import Path
from Radicioni.Esercizio_3.sem_eval_mapper import cognome
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import itertools
import pprint
from scipy.stats import pearsonr, spearmanr
from numpy import mean
from partd import numpy
key_cesare = 'd98e5389-2438-4db4-8672-fcdd4ce6d4f9'
key_nicolo = '34461ea6-4c3a-411f-9531-d9e3cae24954'


def select_lines(file_name: str) -> dict:
    """
    Loads data from file `iurlaro_output.txt` into `eval_dict`
    :return: eval_dict: dictionary whose key is a tuple cointaining two words, and whose value is an annotated value
    """

    # lines = cognome().split('-')
    lines = ['201', '300']
    with open(Path.cwd() / "annotated_files" / file_name, encoding='utf-8') as input_file:
        input_reader = input_file.readlines()

        eval_dict = {}
        for i in range(int(lines[0]) - 1, int(lines[1])):
            line = input_reader[i][:-1].split('\t')
            eval_dict[line[0], line[1]] = line[2]

    return eval_dict


def load_data_from_file() -> dict:
    """
    Loads data from file `mini_nasari.tsv` into `nasari_dict`
    :return: nasari_dict: a dictionary whose key is a babel synset id, and whose value is a tuple containing a
             description of the babel synset id and its corresponding nasari vector
    """

    nasari_dict = {}
    with open(Path.cwd() / "mini_nasari" / "mini_nasari.tsv", encoding="utf-8") as nasari_file:
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
    with open(Path.cwd() / "mini_nasari" / "SemEval17_IT_senses2synsets.txt", encoding="utf-8") as sem_eval_s2s_file:
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


def unify_annotations(files: list) -> defaultdict:
    """
    Unites all the annotations from the files of annotations in `annotated_files`
    :param files: list of file names
    :return: dictionary whose key is (person id, couple of annotated words) and whose value is the associated evaluation
    """
    dictionaries_list = []
    output_dict = defaultdict(dict)

    for file_name in files:
        dictionaries_list.append(select_lines(file_name))

    for i in range(0, len(dictionaries_list)):
        for key in dictionaries_list[i].keys():
            # i valuta key con value print(dictionaries_list[i][key])
            output_dict[i, key] = dictionaries_list[i][key]

    return output_dict


def extract_evaluations(file_list):
    """
    Creates a list of lists. Each created list element is a tuple containing a couple (annotated words) and a list of
    each person evaluation
    :param files: list of involved file names
    :return: list of annotation lists
    """
    unified_annotations = unify_annotations(file_list)

    total_evaluations = []
    count = len(unified_annotations.keys()) / len(file_list)
    for key in unified_annotations.keys():
        if count > 0:
            couple_of_words = key[1]
            people_evaluations = []

            for person in range(0, len(file_list)):
                evaluation = float(unified_annotations[person, couple_of_words])
                people_evaluations.append(evaluation)

            total_evaluations.append((couple_of_words, people_evaluations))
            count -= 1
        else:
            break

    return total_evaluations


def sense_identification(file_name):
    """
    Computes the best sense identification for each couple of words in the given file
    :param file_name: file containing the couple of words to be compared
    """
    annotated_dict = select_lines(file_name)
    nasari_dict = load_data_from_file()
    sem_eval_dict = load_data_from_sem_eval()
    update_sem_eval_dict(sem_eval_dict, annotated_dict, nasari_dict)
    for concepts in annotated_dict:
        concept_1, concept_2 = best_senses_identification(concepts[0], concepts[1], sem_eval_dict)
        print("Best senses for", concepts[0], "and", concepts[1], "are:",
              concept_1, "[", get_gloss(concept_1, key_cesare), "]",
              concept_2, "[", get_gloss(concept_2, key_cesare), "]")


def get_results(file_list):
    """
    Computes the mean value of the words evaluations for each couple.
    Computes also and Pearson & Spearman correlation indexes on the entire column of evaluation that each person
    """
    whole_evaluations = extract_evaluations(file_list)
    people_evaluations = defaultdict(list)
    print()
    for couple in whole_evaluations:
        couple_of_words = couple[0]
        evaluations_list = couple[1]
        print("La coppia di parole: ", couple_of_words, "ha un'annotazione media di:", mean(evaluations_list))

        for person in range(0, len(evaluations_list)):
            people_evaluations[person].append(evaluations_list[person])

    print()
    print("INTER-RATER AGREEMENT")
    for elem in itertools.combinations(people_evaluations.keys(), 2):
        pearson = pearsonr(people_evaluations[elem[0]], people_evaluations[elem[1]])
        spearman = spearmanr(people_evaluations[elem[0]], people_evaluations[elem[1]])
        print("(", elem[0], ",", elem[1], ")", "PC: ", pearson[0], "SC: ", spearman[0], "\n")


def get_gloss(id: str, key: str):
    import urllib
    import urllib3
    import json

    service_url = 'https://babelnet.io/v5/getSynset'
    params = {
        'id': id,
        'key': key
    }

    url = service_url + '?' + urllib.parse.urlencode(params)
    # print(url)

    http = urllib3.PoolManager()
    response = http.request('GET', url)
    babel_synset = json.loads(response.data.decode('utf-8'))
    # pprint.pprint(get_gloss(babel_synset))
    # print(babel_synset)
    return ['BABEL SYNSET NOT FOUND'] if 'message' in  babel_synset else babel_synset['glosses'][0]['gloss']
