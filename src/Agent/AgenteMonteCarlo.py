from MonteCarloTreeSearch import MonteCarlo, Node
from Agent.GameState import ScopaGameState

class AgenteMonteCarlo:
    def __init__(self, giocatore):
        """Inizializza l'agente Monte Carlo per il giocatore"""
        self.giocatore = giocatore

    def scegli_mossa(self, tavolo):
        """
        Sceglie la mossa migliore utilizzando il metodo Monte Carlo Tree Search (MCTS).

        :param tavolo: Lo stato attuale del tavolo di gioco
        :return: La carta da giocare
        """
        stato_iniziale = ScopaGameState(
            self.giocatore,
            tavolo,
            self.giocatore.carte_mano,
            self.giocatore.carte_raccolte,
            []
        )

        root_node = Node(stato_iniziale)
        root_node.player_number = 1
        root_node.discovery_factor = 0.4  # Aumentato per favorire l'esplorazione
        mcts = MonteCarlo(root_node)

        mcts.child_finder = self.child_finder
        mcts.node_evaluator = self.node_evaluator

        # Aumentato il numero di simulazioni per migliorare l'affidabilità
        mcts.simulate(1000)

        # Scegli il nodo migliore in base alla simulazione
        best_node = mcts.make_choice()
        return best_node.state.last_move[0]  # Restituisce la carta da giocare

    def child_finder(self, node, montecarlo):
        """
        Funzione che esplora i possibili nodi figli a partire dal nodo corrente.
        """
        possible_moves = node.state.get_possible_moves()
        for mossa in possible_moves:
            nuovo_stato = node.state.move(mossa)
            child = Node(nuovo_stato)
            child.player_number = 3 - node.player_number

            # Valutazione euristica per policy value
            policy_value = self._calculate_policy_value(nuovo_stato, mossa)
            child.policy_value = policy_value

            # Discovery factor dinamico
            child.discovery_factor = self._calculate_discovery_factor(nuovo_stato)

            node.add_child(child)

    def node_evaluator(self, node, montecarlo):
        """
        Funzione per valutare il valore di un nodo.
        """
        return node.state.evaluate_state()

    def _calculate_policy_value(self, state, mossa):
        """
        Calcola il valore della policy per una mossa.

        :param state: Lo stato corrente del gioco
        :param mossa: La mossa da valutare
        :return: Il valore della policy per quella mossa
        """
        carta, prese = mossa
        base_value = 0.3

        if prese:
            # Bonus per prese
            base_value += 0.2
            # Bonus per denari
            if any(c.seme == 'Denari' for c in prese):
                base_value += 0.15
            # Bonus per settebello
            if any(c.seme == 'Denari' and c.valore == 7 for c in prese):
                base_value += 0.25

        return min(base_value, 1.0)  # Limita il valore tra 0 e 1

    def _calculate_discovery_factor(self, state):
        """
        Calcola il fattore di scoperta dinamico per guidare l'esplorazione nel MCTS.

        :param state: Lo stato corrente del gioco
        :return: Il fattore di scoperta
        """
        base_factor = 0.4

        # Aumenta per stati promettenti
        if state.giocatore.scope > 0:
            base_factor += 0.15

        # Aumenta se ha molti denari
        denari = sum(1 for c in state.carte_raccolte_giocatore if c.seme == 'Denari')
        if denari >= 5:
            base_factor += 0.1

        # Aumenta nelle fasi iniziali del gioco (più carte in mano)
        if len(state.carte_mano) >= 2:
            base_factor += 0.1

        return min(base_factor, 0.8)  # Limita il fattore di scoperta tra 0 e 0.8
