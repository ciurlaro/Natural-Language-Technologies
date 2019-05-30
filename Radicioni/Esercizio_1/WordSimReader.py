import csv


def word_sim_reader(filename: str) -> list:
    word_sim= []
    f = open(filename, "rt")
    try:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            word_sim.append(row)

    finally:
        f.close()

    return word_sim
