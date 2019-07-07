# Dettagli implementativi

- ### Linguaggio di programmazione: python

## Librerie ed utilità usate:

- ### Nltk: Natural Language ToolKit
  **Nltk** è una *suite di librerie* per lo sviluppo di programmi di linguistica computazionale.

  Di essa ci sono state utili le classi di interfaccia alla risorsa *WordNet* e una esaustiva lista di stopwords della lingua inglese.

- ### numpy: Numeric Python
  **numpy** è una libreria che supporta implementazioni di *grandi matrici* e *array multidimensionali* e mette a disposizione una vasta collezione di funzioni matematiche di alto livello per poter operare efficientemente su di esse.

  Di essa abbiamo utilizzato le funzioni per il calcolo della *covarianza*, della *deviazione standard*, della *media* .
  Abbiamo inoltre utilizzato i tipi primitivi *array* e *float64*, non presenti in nessuna versione vanilla di python.

    **PS:** notare che *array* di numpy è diverso da *list* presente in python, in quanto fortemente orientato al calcolo matematico.
    Su di esso possono ad esempio essere chiamate funzioni di utilità come *shape*, *rank* e *full*.

- ### scipy: Scientific Python
  **scipy** è una libreria che implementa strumenti per ottimizzazione numerica, algebra lineare, integrazione e *statistica*.

  Di essa abbiamo utilizzato le funzioni *rankdata*, *pearsonr* e *spearmanr*.

- ### sklearn: Scientific Kit of Learning
  **sklearn** è una libreria che implementa modelli e algoritmi per apprendimento automatico.

  Di essa abbiamo utilizzato la funzione per effettuare *cosine similarity*.

- ### urllib, json
  Per scambiare messaggi *REST* con il server di *BabelNet*, ci sono state utili le librerie **urllib** e **json** di python.

## Moduli python
Ciascun esercizio è diviso concettualmente per **moduli**, seguendo i seguenti criteri:

- `main` è il modulo *principale*, da lanciare al fine di avviare l'esecuzione
- `logic` contiene l'implementazione della *logica* applicativa
- `init`, ove presente, *inizializza* dati necessari allo svolgimento dell'esercizio

Gli altri file contengono metodi di utilità o dati in forma tabulare da elaborare.

# Esercizio 1 - Conceptual similarity with WordNet
Dati in input due termini, il task di conceptual similarity consiste nel fornire un punteggio numerico di similarità che ne indichi la vicinanza semantica.
Nello specifico abbiamo che:
- un punteggio pari a 0 significa che i sensi sono completamente dissimili
- mentre un punteggio pari ad 1 significa identità

Per risolvere il task di conceptual similarity è possibile sfruttare la struttura ad albero di WordNet.

## Input 
L’**input** per questo esercizio è costituito da un **file** che ha nome `WordSim353` all'interno del quale troviamo **353 coppie di termini**.

A ciascuna coppia è attribuito un **valore numerico [0,10]**, che rappresenta la **similarità** fra gli elementi della coppia analizzata.

## Consegna
L'esercizio consiste nell'**implementare tre misure di similarità** basate su WordNet, le quali risultano essere rispettivamente:

- **Wu & Palmer** 
   <p align="center">
        <img src="https://latex.codecogs.com/gif.latex?cs%28s1%2Cs2%29%3D%5Cfrac%7B2*depth%28LCS%29%7D%7Bdepth%28s1%29&plus;depth%28s2%29%7D">
   </p> dove <i>LCS</i> risulta essere il primo antenato comune, detto <i>Lowest Common Subsumer</i>, fra i sensi <i>s1</i> ed <i>s2</i> e <i>depth(x)</i> è una funzione che misura la distanza fra la radice di WordNet e il synset <i>x</i>.

- **Shortest Path**
   <p align="center">
        <img src="https://latex.codecogs.com/gif.latex?sim_%7Bpath%7D%28s1%2Cs2%29%3D2*depthMax%20-%20len%28s1%2Cs2%29">
   </p> dove <i>depthMax</i>, data una specifica versione di WordNet, risulta essere un valore fissato (nel nostro caso, con la versione 3.0 di WordNet, pari a 40).

- **Leakcock & Chodorow**
<p align="center">
     <img src="https://latex.codecogs.com/gif.latex?sim_%7BLC%7D%28s1%2Cs2%29%3D-log%5Cfrac%7Blen%28s1%2Cs2%29%7D%7B2*depthMax%7D">
</p>

<hr>    
    
- **Indici di correlazione**
     
     Per ciascuna di tali misure di similarità, effettuiamo anche il calcolo degli **indici di correlazione di**:

     - **Spearman**: 
     <p align="center">
     <img src="https://latex.codecogs.com/gif.latex?r_s%3D%5Crho_%7Brg_X%2Crg_Y%7D%3D%5Cfrac%7Bcov%28rg_X%2Crg_Y%29%7D%7B%5Csigma_%7Brg_X%7D%5Csigma_%7Brg_Y%7D%7D">
    </p>
    
     - **Pearson**:
     <p align="center">
     <img src="https://latex.codecogs.com/gif.latex?%5Crho_%7BX%2CY%7D%3D%5Cfrac%7Bcov%28X%2CY%29%7D%7B%5Csigma_%7BX%7D%5Csigma_%7BY%7D%7D">
     </p>

    fra i risultati ottenuti e quelli ‘target’ presenti nel ﬁle annotato.
    

## Risultati ottenuti 
Di seguito sono riportati i valori finali ottenuti:

|  | Indice di correlazione di Pearson | Indice di correlazione di Spearman |
| ------------- | ------------- | ------------- |
| **Wu & Palmer**          |  0.29700237615006186  | 0.3514162690947211  |
| **Shortest Path**       | -0.06801134931497702  | 0.29034784872693087  |
| **Leakcock & Chodorow**  | 0.319721382759658  | 0.29033458035854387  |


# Esercizio 2 - Word Sense Disambiguation
*"Word sense disambiguation (WSD) is an open problem of natural language processing, which comprises the process of identifying which sense of a word (i.e. meaning) is used in any given sentence, when the word has a number of distinct senses (polysemy)."*

## Input 
L’**input** per questo esercizio è costituito da un **file** di testo che ha nome `sentences.txt` all'interno del quale troviamo **14 frasi** contenenti rispettivamente dei termini polisemici i quali sono identificabili per via del fatto di essere compresi tra due coppie di **.

## Consegna
1. Implementare l’**algoritmo di Lesk**
2. **Disambiguare i termini polisemici** all’interno delle frasi del ﬁle `sentences.txt`; oltre a restituire i synset ID del senso (appropriato per il contesto), il programma deve riscrivere ciascuna frase in input sostituendo il termine polisemico con l’elenco dei sinonimi eventualmente presenti nel synset
3. Estrarre 50 frasi dal corpus *SemCor*, corpus annotato con i synset di *WN*, e disambiguare almeno un sostantivo per frase. **Calcolare l’accuratezza del sistema implementato sulla base dei sensi annotati in SemCor**


## Algoritmo di Lesk
Tale algoritmo rappresenta di gran lunga uno degli algoritmi di sense disambiguation più studiati.

**Pseudocodice** dell'algoritmo su cui sono basate le implementazioni all'interno dell'esercitazione:
<p align="center">
 <img src="https://user-images.githubusercontent.com/37592014/60672048-c03b0880-9e74-11e9-8769-27215887fb7b.PNG" width="60%" height="30%">
</p>

L'algoritmo di Lesk è stato implementato in tre varianti:
1. **Implementazione dello pseudocodice** presentato nell'immagine qui sopra. 

2. Implementazione analoga alla prima, attua lo stesso procedimento generale, alla quale è stata aggiunta l'**eliminazione delle stopwords** allo scopo di rendere il contesto quanto meno rumoroso possibile.

3. Implementazione con **estensione del contesto**; aggiunge al contesto *iperonimi* ed *iponimi* dei termini in esso presenti.
Lo scopo è quello di *analizzare la variazione di prestazioni* alla generazione di un contesto più vasto.


## Risultati ottenuti 
Riportiamo i risultati calcolati in termini di accuracy.

|  | Prima versione Lesk | Seconda versione Lesk | Terza versione Lesk |
| ------------- | ------------- | ------------- | ------------- |
| **Accuracy**         |  0.4  | ~0.4  | ~0.4 |  
| **Baseline**        |  0.6  | 0.6  | 0.6 | 

Questo *gap tra baseline e implementazione Lesk* è giustificato dal fatto che la baseline è stata calcolata sulla base del primo synset restituito da WordNet, il quale rappresenta il synset statisticamente più probabile.

Per quanto riguarda i risultati ottenuti attraverso la seconda e terza versione dell'algoritmo, *non si notano miglioramenti significativi*. I risultati sono infatti pressochè identici.

# Esercizio 3 - Annotazione di Corpora e Sense Identiﬁcation 

## Consegna
1. **Annotare** le coppie presenti nel file `it.test.data.txt` con un valore di *similarity* compreso tra 0 e 4
2. **Calcolare valore medio ed inter-rater agreement** fra le annotazioni dei tre diversi annotatori
  Per il calcolo dell' *inter-rater agreement* sono stati utilizzati, come misure, gli *indici di correlazione di Pearson e Spearman*.


| **Inter-Rater Agreement, Pearson**  | Ferretti | Gabbia | Iurlaro |
| ------------- | ------------- | ------------- | ------------- |
| **Ferretti**         |  -  | 0.8174349077649021  | 0.7574318415062212 |  
| **Gabbia**        |  0.8174349077649021  | -  | 0.8066287958553586 | 
| **Iurlaro**        |  0.7574318415062212  |  0.8066287958553586  | - | 

| **Inter-Rater Agreement, Spearman**  | Ferretti | Gabbia | Iurlaro |
| ------------- | ------------- | ------------- | ------------- |
| **Ferretti**         |  -  | 0.8128527487138741  | 0.7583300448215048 |  
| **Gabbia**        |  0.8128527487138741  | -  | 0.8388276512272342 | 
| **Iurlaro**        |  0.7583300448215048  |  0.8388276512272342 | - | 

3. **Effettuare sense identification**, ovvero *identificare i sensi che massimizzano il punteggio di similarità* fra 2 termini, per ogni coppia.
<p align="center">
 <img src="https://latex.codecogs.com/gif.latex?c_{1},&space;c_{2}&space;\longleftarrow&space;\underset{c_{1}&space;\in&space;s\left(w_{1}\right),&space;c_{2}&space;\in&space;s\left(w_{2}\right)}{\arg&space;\max&space;}\left[\operatorname{sim}\left(c_{1},&space;c_{2}\right)\right]" title="c_{1}, c_{2} \longleftarrow \underset{c_{1} \in s\left(w_{1}\right), c_{2} \in s\left(w_{2}\right)}{\arg \max }\left[\operatorname{sim}\left(c_{1}, c_{2}\right)\right]" />
</p> 

- A tale scopo è stata applicata la misura di **cosine similarity** tra i *vettori nasari* forniti dal file `mini-nasari.tsv`. 
  <p align="center">
  <img src="https://latex.codecogs.com/gif.latex?cos\_similarity(A,B)=\frac{A&space;\cdot&space;B}{\|A\|\|B\|}" title="cos\_similarity(A,B)=\frac{A \cdot B}{\|A\|\|B\|}" />
  </p>
  
4. **Valutare** l'appropriatezza della coppia dei sensi identificati, stabilendo se i sensi in questione sono quelli idealmente selezionati al momento dell’annotazione.
