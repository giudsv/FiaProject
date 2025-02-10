from copy import deepcopy


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
