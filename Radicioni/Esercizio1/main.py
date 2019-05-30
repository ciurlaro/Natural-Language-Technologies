from TLN.Radicioni.Esercizio1.WordSimReader import WordSimReader


def main():
    wordSim = WordSimReader("/home/nicolo/PycharmProjects/TLN1/TLN/Radicioni/Esercizio1/WordSim353.csv")
    for row in wordSim:
        print(row)


main()
