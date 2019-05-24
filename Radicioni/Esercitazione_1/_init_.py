from Radicioni.Corpus.SemCor import semcor_extraction
from Radicioni.Esercitazione_1.simplified_lesk import simplified_lesk


def main():
    sentences, extracted = semcor_extraction()

    for i in range(0, len(sentences)):
      sense = simplified_lesk(extracted[i][0][0], sentences[i])
      print(sense, extracted[i].label())

    # print("Sinonimi:", sense.lemmas())
    # accuracy: Sensi dei sostantivi classificati bene/ Tutti i sensi delle parola nel Semcore


main()