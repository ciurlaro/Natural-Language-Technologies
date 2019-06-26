#ESERCIZIO 1

Preso un file WordSimSimilarity, composto da una coppia di parole ed un valore corrispondente alla loro similarity, sono state calcolate ed implementate le seguenti metriche rappresentanti le similarity: Wu & Palmer, Shortest path, Leacock and Chodorow.
Successivamente sono stati calcolati gli indici di correlazione Pearson e Spearman, con lo scopo di confrontare i risultati precedentemente ottenuti.
Di seguito sono riportati i valori finali ottenuti:

- Pearson correlation:

WP) 0.29700237615006186

SP) -0.06801134931497702

LC) 0.319721382759658


- Spearman correlation:

WP) 0.3514162690947211

SP) 0.29034784872693087

LC) 0.29033458035854387



#ESERCIZIO 2

Per questo esercizio, a scopo di effettuare Word Sense Disambiguation, è stato implementato l'algoritmo Lesk, in tre varianti.
La prima variante rappresenta l'implementazione dello pseudocodice visto a lezione. In particolare, si calcola la max_overlap tra i possibili sensi di Wordnet per la parola data, e si restituisce il senso che massimizza tale overlap. L'algoritmo prende dunque in input la parola da disambiguare, ed una frase in cui appare (contesto).

La seconda implementazione è simile alla prima, il procedimento generale è lo stesso, ma è stata implementata in maniera aggiuntiva l'eliminazione delle stopwords all'interno delle frasi, cercando di rendere il contesto più pulito possibile.
La terza ed ultima versione, prevede l'amplificazione del contesto a tutto ciò che riguarda, ed è correlato tramite, le relazioi di Hyperonym e Hyponym, applicate alle paorle del contesto. Generando un contesto molto più vasto, proviamo a vedere se le prestazioni, applicando questa modifica, possono migliorare o cambiare in qualche modo.

In un primo momento sono stati disambiguati i termini polisemici contenuti in sentences.txt, con le frasi in cui apparivano, e sono stati sostituiti con la lista di sinonimi (ottenuta tramite la funzione lemmas() ) del senso restituito da Lesk.
Successivamente l'algoritmo è stato utilizzato per disambiguare 50 termini presi in modo random da 50 frasi ottenute dal corpus Semcor.
I risultati, calcolati in termini di accuracy, sono riportati successivmante.

In media la prima implementazione fornisce un risultato di ~0.4, contro una baseline di ~0.6 prendendo le informazioni (parole da disambiguare e frasi) dal corpus Semcor. Questo gap tra baseline e implementazione Lesk è giustificato dal fatto che la baseline è stata calcolata sulla base del primo synset restituito da WordNet, il quale rappresenta il synset statisticamente più probabile.
Per quanto riguarda i risultati ottenuti attraverso la seconda e terza implementazione, non si notano miglioramenti significativi. I risultati sembrano dunque essere pressochè identici.

#ESERCIZIO 3

Per quanto riguarda il terzo ed ultimo esercizio, sono state inizialmente annotate 100 coppie di termini con un valore di similarity compreso tra 0 e 4.
Le coppie sono state fornite dal file it.test.data.txt. Successivamente sono stati calcolati il valore medio e l’inter-rater agreement fra le annotazioni dei tre diversi annotatori. Per il calcolo dell' inter-rater agreement sono stati utilizzati, come misure, gli indici di correlazione di Pearson e Spearman.
I risultati di questa computazione sono riportati in fondo.
Successivamente, a scopo di identificare i corretti sensi di Babel, è stata implementata la cosine similarity sui vettori nasari forniti dal file mini-nasari.tsv. Una volta effettuato il task di sense indentification, sono stati restituiti i corretti sensi, ovvero quelli che rendevano massima la cosine similarity, e la rispettiva glossa.

INTER-RATER AGREEMENT

( 0 , 1 ) PC:  0.7574318415062212 SC:  0.7583300448215048 

( 0 , 2 ) PC:  0.8066287958553586 SC:  0.8388276512272342 

( 1 , 2 ) PC:  0.8174349077649021 SC:  0.8128527487138741 




DA FARE:

getGloss()
