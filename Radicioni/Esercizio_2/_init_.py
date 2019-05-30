from Radicioni.Corpus.SemCor import semcor_extraction
from Radicioni.Esercizio_2.simplified_lesk import simplified_lesk
import sklearn.metrics as metrics



def main():
    sentences, extracted = semcor_extraction()

    for i in range(0, len(sentences)):
      sense = simplified_lesk(extracted[i][0][0], sentences[i])
      print(sense, extracted[i].label())

    # print("Sinonimi:", sense.lemmas())
    # accuracy: Sensi dei sostantivi classificati bene/ Tutti i sensi delle parola nel Semcore


def calculate_accuracy():
    # Calculate accuracy
    ground = [str(element['semcor']) for element in dataset]
    predicted_nltk = [str(element['nltk_lesk']) for element in dataset]
    predicted_simplified = [str(element['simplified_lesk']) for element in dataset]
    nltk_accuracy = metrics.accuracy_score(ground, predicted_nltk)
    simplified_accuracy = metrics.accuracy_score(ground, predicted_simplified)



main()