import re
from TLN.Radicioni.Esercizio2.Lesk import simplified_Lesk
from TLN.Radicioni.Esercizio2.SemcorExtraction import semcor_extraction


def main():

    sentences = ["**Arms** bend at the elbow.",
                 "Germany sells **arms** to Saudi Arabia.",
                 "The **key** broke in the lock.",
                 "The **key** problem was not one of quality but of quantity. ",
                 "Work out the **solution** in your head.",
                 "Heat the **solution** to 75° Celsius. ",
                 "The house was burnt to **ashes** while the owner returned.",
                 "This table is made of **ash** wood.",
                 "The **lunch** with her boss took longer than she expected.",
                 "She packed her **lunch** in her purse.",
                 "The **classification** of the genetic data took two years.",
                 "The journal Science published the **classification** this month.",
                 "His cottage is near a small **wood**.",
                 "The statue was made out of a block of **wood**."]
    words = []

    for i in range(0, len(sentences)):
        for elem in sentences[i].split():
            if elem.startswith("**"):
                polysemic_term = re.sub(r'[^\w\s]', '', elem)
                sentences[i] = sentences[i].replace(elem, polysemic_term)
                words.append(polysemic_term)

    for i in range(0, len(sentences)):
        synset = simplified_Lesk(words[i], sentences[i])                     # Lesk
        print("Best sense founded for this sentence: ", synset)
        sentences[i] = sentences[i].replace(words[i], str(synset.lemmas()))  # lemmas()= synonyms of the chosen synset
        print(sentences[i])

    print()
    print("-----------------------------------------------------------------------------------------------------------")
    print()
                                                                             # semcor
    semCor_sentences, semCor_extracted, semcor_synset = semcor_extraction()

    for i in range(0, len(sentences)):
      sense = simplified_Lesk(semCor_extracted[i][0][0], sentences[i])
      print(sense, semcor_synset[i])

    # accuracy: Sensi dei sostantivi classificati bene/ Tutti i sensi delle parola nel Semcore



main()
