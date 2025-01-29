from copy import deepcopy




from MonteCarloTreeSearch import MonteCarlo, Node

class ScopaGameState:
    def __init__(self, giocatore, tavolo, carte_mano, carte_raccolte_giocatore, carte_raccolte_avversario):
        """
        Inizializza lo stato di gioco per la partita di Scopa.

        :param giocatore: Il giocatore corrente
        :param tavolo: Lo stato del tavolo (carte visibili)
        :param carte_mano: Le carte in mano al giocatore
        :param carte_raccolte_giocatore: Le carte già raccolte dal giocatore
        :param carte_raccolte_avversario: Le carte già raccolte dall'avversario
        """
        self.giocatore = giocatore
        self.tavolo = deepcopy(tavolo)  # Copia profonda del tavolo per evitare modifiche indesiderate
        self.carte_mano = deepcopy(carte_mano)  # Copia profonda delle carte in mano
        self.carte_raccolte_giocatore = deepcopy(carte_raccolte_giocatore)  # Copia delle carte raccolte dal giocatore
        self.carte_raccolte_avversario = deepcopy(
            carte_raccolte_avversario)  # Copia delle carte raccolte dall'avversario
        self.last_move = None  # Inizializza l'ultima mossa come None

    def get_possible_moves(self):
        """Restituisce tutte le mosse possibili ordinate per priorità"""
        mosse = []

        # Cicla su tutte le carte in mano per determinare le mosse possibili
        for carta in self.carte_mano:
            # Cerca le prese possibili per ogni carta
            prese_possibili = self.giocatore.cerca_prese_possibili(carta, self.tavolo.carte)

            if prese_possibili:
                # Ordina le prese possibili per valore strategico
                prese_ordinate = sorted(prese_possibili,
                                        key=lambda x: self._valuta_presa(carta, x),
                                        reverse=True)
                for presa in prese_ordinate:
                    # Aggiunge la mossa (carta, presa) alla lista delle mosse
                    mosse.append((carta, presa))
            else:
                # Se non ci sono prese, la mossa sarà uno scarto (carta, lista vuota)
                mosse.append((carta, []))

        # Ordina tutte le mosse in base alla valutazione della mossa
        return sorted(mosse, key=lambda x: self._valuta_mossa(x), reverse=True)

    def _valuta_presa(self, carta, presa):
        """Valuta il valore strategico di una presa"""
        score = 0

        # Valuta il settebello (sette di denari)
        if any(c.seme == 'Denari' and c.valore == 7 for c in presa):
            score += 50

        # Valuta i denari raccolti
        denari = sum(1 for c in presa if c.seme == 'Denari')
        score += denari * 20

        # Valuta la possibilità di scopa (tutte le carte sul tavolo sono prese)
        if len(self.tavolo.carte) == len(presa):
            score += 40

        # Valuta carte alte per la primiera
        for c in presa:
            if c.valore in [7, 6, 1]:
                score += 15

        # Bonus per prese multiple
        score += len(presa) * 10

        return score

    def _valuta_scarto(self, carta):
        """Valuta la priorità di scarto di una carta"""
        score = 0

        # Penalizza lo scarto di carte strategiche
        if carta.seme == 'Denari':
            score -= 30
        if carta.valore == 7:
            score -= 25
        if carta.valore in [6, 1]:
            score -= 15

        # Favorisce lo scarto di carte basse non denari
        if carta.valore <= 4 and carta.seme != 'Denari':
            score += 10

        return score

    def _valuta_mossa(self, mossa):
        """Valuta il valore complessivo di una mossa"""
        carta, presa = mossa
        if presa:  # Se è una presa
            return self._valuta_presa(carta, presa)
        else:  # Se è uno scarto
            return self._valuta_scarto(carta)

    def move(self, mossa):
        """Applica una mossa e restituisce un nuovo stato"""
        carta, presa = mossa  # Ora questa riga funzionerà correttamente
        nuovo_stato = deepcopy(self)  # Crea una copia dello stato attuale

        # Rimuovi la carta dalla mano
        nuovo_stato.carte_mano.remove(carta)

        if presa:
            # Raccogli le carte prese
            for carta_presa in presa:
                nuovo_stato.tavolo.carte.remove(carta_presa)
                nuovo_stato.carte_raccolte_giocatore.append(carta_presa)
            # Aggiungi la carta giocata alle carte raccolte dal giocatore
            nuovo_stato.carte_raccolte_giocatore.append(carta)

            # Verifica se è stata fatta una scopa
            if len(nuovo_stato.tavolo.carte) == 0 and len(nuovo_stato.carte_mano) > 0:
                nuovo_stato.giocatore.scope += 1
        else:
            # Se non ci sono prese, la carta va sul tavolo
            nuovo_stato.tavolo.carte.append(carta)

        nuovo_stato.last_move = mossa  # Memorizza l'ultima mossa
        return nuovo_stato

    def evaluate_state(self):
        """Valuta lo stato corrente con pesi ottimizzati"""
        punteggio = 0

        # Scope (peso aumentato)
        punteggio += self.giocatore.scope * 15

        # Denari (peso aumentato e progressivo)
        denari = sum(1 for carta in self.carte_raccolte_giocatore if carta.seme == 'Denari')
        punteggio += denari * (8 if denari >= 5 else 5)

        # Settebello (peso aumentato)
        if any(carta.seme == 'Denari' and carta.valore == 7
               for carta in self.carte_raccolte_giocatore):
            punteggio += 20

        # Carte per primiera (nuovo sistema di punteggio)
        primiera_values = {7: 21, 6: 18, 1: 16, 5: 15, 4: 14}
        for seme in ['Bastoni', 'Coppe', 'Denari', 'Spade']:
            carte_seme = [c for c in self.carte_raccolte_giocatore if c.seme == seme]
            if carte_seme:
                max_value = max(primiera_values.get(c.valore, 0) for c in carte_seme)
                punteggio += max_value * 0.5

        # Bonus per controllo del tavolo (meno carte sul tavolo = meglio)
        if len(self.tavolo.carte) < 3:
            punteggio += 5

        return min(max(punteggio / 150, -1), 1)  # Punteggio tra -1 e 1


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

        def child_finder(node, montecarlo):
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

        def node_evaluator(node, montecarlo):
            """
            Funzione per valutare il valore di un nodo.
            """
            return node.state.evaluate_state()

        mcts.child_finder = child_finder
        mcts.node_evaluator = node_evaluator

        # Aumentato il numero di simulazioni per migliorare l'affidabilità
        mcts.simulate(1000)

        # Scegli il nodo migliore in base alla simulazione
        best_node = mcts.make_choice()
        return best_node.state.last_move[0]  # Restituisce la carta da giocare

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
