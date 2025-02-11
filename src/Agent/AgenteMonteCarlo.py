from MonteCarloTreeSearch import MonteCarlo, Node
from Agent.GameState import ScopaGameState


class AgenteMonteCarlo:
    def __init__(self, giocatore):
        """
        Inizializza l'agente Monte Carlo per il giocatore.

        :param giocatore: L'istanza del giocatore a cui appartiene l'agente
        """
        self.giocatore = giocatore

    def scegli_mossa(self, tavolo):
        """
        Sceglie la mossa migliore utilizzando il metodo Monte Carlo Tree Search (MCTS).

        :param tavolo: Lo stato attuale del tavolo di gioco
        :return: La carta da giocare scelta dall'agente
        """
        # Creazione dello stato di gioco iniziale per l'MCTS
        stato_iniziale = ScopaGameState(
            self.giocatore,
            tavolo,
            self.giocatore.carte_mano,
            self.giocatore.carte_raccolte,
            []
        )

        # Creazione del nodo radice per l'MCTS
        root_node = Node(stato_iniziale)
        root_node.player_number = 1  # Identifica il numero del giocatore
        root_node.discovery_factor = 0.4  # Controlla il livello di esplorazione dell'algoritmo

        # Inizializzazione dell'algoritmo MCTS
        mcts = MonteCarlo(root_node)

        # Imposta le funzioni personalizzate per trovare i figli e valutare i nodi
        mcts.child_finder = self.child_finder
        mcts.node_evaluator = self.node_evaluator

        # Aumentiamo il numero di simulazioni per ottenere scelte più affidabili
        mcts.simulate(1000)

        # Seleziona il miglior nodo risultante dalle simulazioni
        best_node = mcts.make_choice()

        # Restituisce la carta selezionata come miglior mossa
        return best_node.state.last_move[0]

    def child_finder(self, node, montecarlo):
        """
        Genera tutti i possibili stati successivi (figli) a partire dal nodo corrente.

        :param node: Nodo corrente dell'albero di ricerca
        :param montecarlo: Istanza dell'algoritmo MCTS
        """
        possible_moves = node.state.get_possible_moves()
        for mossa in possible_moves:
            nuovo_stato = node.state.move(mossa)
            child = Node(nuovo_stato)
            child.player_number = 3 - node.player_number  # Alterna il giocatore

            # Valutazione della mossa tramite una funzione di policy
            policy_value = self._calculate_policy_value(nuovo_stato, mossa)
            child.policy_value = policy_value

            # Calcolo dinamico del discovery factor per la strategia di esplorazione
            child.discovery_factor = self._calculate_discovery_factor(nuovo_stato)

            # Aggiunge il nodo figlio all'albero di ricerca
            node.add_child(child)

    def node_evaluator(self, node, montecarlo):
        """
        Valuta il valore di un nodo in base alla situazione di gioco.

        :param node: Nodo da valutare
        :param montecarlo: Istanza dell'algoritmo MCTS
        :return: Valutazione dello stato
        """
        return node.state.evaluate_state()

    def _calculate_policy_value(self, state, mossa):
        """
        Calcola il valore della policy per una mossa, favorendo quelle strategicamente vantaggiose.

        :param state: Stato corrente del gioco
        :param mossa: Mossa da valutare
        :return: Valore della policy per la mossa (tra 0 e 1)
        """
        carta, prese = mossa
        base_value = 0.3  # Valore base di ogni mossa

        if prese:
            base_value += 0.2  # Bonus per prese effettuate

            # Bonus per la raccolta di carte di seme Denari
            if any(c.seme == 'Denari' for c in prese):
                base_value += 0.15

            # Bonus aggiuntivo per la presa del settebello (7 di Denari)
            if any(c.seme == 'Denari' and c.valore == 7 for c in prese):
                base_value += 0.25

        return min(base_value, 1.0)  # Limita il valore massimo a 1

    def _calculate_discovery_factor(self, state):
        """
        Calcola il fattore di esplorazione per il nodo attuale, basato sulla situazione di gioco.

        :param state: Stato corrente del gioco
        :return: Fattore di esplorazione (tra 0 e 0.8)
        """
        base_factor = 0.4  # Valore iniziale di esplorazione

        # Incremento se il giocatore ha fatto almeno una Scopa
        if state.giocatore.scope > 0:
            base_factor += 0.15

        # Incremento se il giocatore ha raccolto molte carte di seme Denari
        denari = sum(1 for c in state.carte_raccolte_giocatore if c.seme == 'Denari')
        if denari >= 5:
            base_factor += 0.1

        # Incremento se siamo all'inizio del gioco (molte carte in mano)
        if len(state.carte_mano) >= 2:
            base_factor += 0.1

        return min(base_factor, 0.8)  # Limita il valore massimo a 0.8
