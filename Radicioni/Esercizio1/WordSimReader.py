import csv


def WordSimReader(filename: str) -> list:
    wordSim= []
    f = open(filename, "rt")
    try:
        reader = csv.reader(f)
        for row in reader:
            if row[0].startswith("#"):
                continue
            else:
                wordSim.append(row)

    finally:
        f.close()

    return wordSim
