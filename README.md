# ScopaAI
L’obiettivo principale di questo progetto è sviluppare un agente intelligente capace di giocare a Scopa
il cui obiettivo prioritario è vincere la partita.

Per raggiungere questo risultato, l’IA sarà progettata per:
- Analizzare le situazioni di gioco e valutare le mosse più vantaggiose in ogni turno;
- Massimizzare i punti attraverso una gestione strategica delle prese, delle scope e degli obiettivi
secondari (come il Settebello, i Denari e la Primiera).

Il risultato atteso è un avversario virtuale in grado di competere in modo intelligente ed efficace,
simulando le scelte di un giocatore esperto con l’unico scopo di massimizzare le probabilità di vittoria.

## Risorse
La cartella `src` contiene il codice sorgente organizzato nei seguenti package:
- `Agent`: Questo package implementa l’agente di gioco intelligente utilizzando l'algoritmo di Monte Carlo per
prendere decisioni strategiche durante la partita.

- `Evaluation`: Questo package presenta il file `ValutationGame.py`, il quale consente di far giocare
l’agente contro se stesso per un numero definito di partite. Inoltre, verrà creato un report che verrà poi
utilizzato per fare valutazioni sull’algoritmo.

- `GameEngine`: Questo package contiene tutte le classi responsabili della gestione della logica di gioco.
Qui vengono definite le regole della Scopa, lo stato della partita e le operazioni necessarie per la sua
evoluzione. Il GameEngine funge da base per l’interazione tra gli agenti e il sistema di gioco.

- `MonteCarloTreeSearch`: Questo package include l’implementazione dell’algoritmo di Monte Carlo, utilizzato
per esplorare le possibili mosse e selezionare la migliore attraverso simulazioni. Al suo interno si trovano
due classi principali:
	- `Node`: Classe usata per rappresentare i nodi dell'albero di ricerca, che memorizzano gli stati del gioco
 	ed i valori associati.
	- `MonteCarlo`: Gestisce il processo di ricerca, eseguendo simulazioni per selezionare la mossa ottimale.

Infine la cartella `result` presenta i risultati delle partite che l'agente ha giocato contro se stesso.

## Avviare la demo
Per avviare la demo e giocare contro l'AI basta eseguire da terminale il file `src/Main.py` (i.e. `python3 src/Main.py`) che
si trova nella cartella root.
