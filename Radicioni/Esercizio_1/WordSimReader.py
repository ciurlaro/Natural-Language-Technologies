import csv


def word_sim_reader(filename: str) -> list:
    """
    Read the given input file and return a list of its rows
    :param filename:
    :return:
    """
    word_sim = []
    f = open(filename, "rt")
    try:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            word_sim.append(row)

    finally:
        f.close()

    return word_sim
