class Punteggio:
    def __init__(self):
        self.punteggio_totale = 0

    def calcola_carte_lungo(self, num_carte, num_carte_avversario):
        """Calcola punto per chi ha più carte"""
        if num_carte > num_carte_avversario:
            return 1
        return 0

    def calcola_denari(self, carte_raccolte):
        """Conta il numero di carte denari"""
        return sum(1 for carta in carte_raccolte if carta.seme == 'Denari')

    def ha_settebello(self, carte_raccolte):
        """Verifica se il giocatore ha il settebello"""
        return any(carta.seme == 'Denari' and carta.valore == 7 for carta in carte_raccolte)

    def calcola_valore_primiera(self, valore):
        """Calcola il valore della carta per la primiera"""
        valori_primiera = {
            7: 21,
            6: 18,
            1: 16,
            5: 15,
            4: 14,
            3: 13,
            2: 12,
            8: 10,
            9: 10,
            10: 10
        }
        return valori_primiera.get(valore, 0)

    def calcola_primiera(self, carte_raccolte):
        """Calcola il punteggio della primiera"""
        # Raggruppa le carte per seme
        carte_per_seme = {
            'Coppe': [],
            'Bastoni': [],
            'Denari': [],
            'Spade': []
        }

        for carta in carte_raccolte:
            carte_per_seme[carta.seme].append(carta)

        # Trova il valore massimo per ogni seme
        punteggi_per_seme = {}
        for seme, carte in carte_per_seme.items():
            if carte:  # Se ci sono carte per questo seme
                max_valore = max(
                    self.calcola_valore_primiera(carta.valore)
                    for carta in carte
                )
                punteggi_per_seme[seme] = max_valore
            else:
                # Aggiungiamo 0 per i semi mancanti
                punteggi_per_seme[seme] = 0

        return sum(punteggi_per_seme.values()), punteggi_per_seme

    def calcola_punteggio_round(self, giocatore, giocatore_avversario):
        """Calcola il punteggio totale per un round"""
        # Punto per carte lungo
        carte_giocatore = len(giocatore.carte_raccolte)
        carte_avversario = len(giocatore_avversario.carte_raccolte)
        carte_lungo = self.calcola_carte_lungo(carte_giocatore, carte_avversario)

        # Punto per denari
        denari_giocatore = self.calcola_denari(giocatore.carte_raccolte)
        denari_avversario = self.calcola_denari(giocatore_avversario.carte_raccolte)
        punto_denari = 1 if denari_giocatore > denari_avversario else 0

        # Punto per settebello
        punto_settebello = 1 if self.ha_settebello(giocatore.carte_raccolte) else 0

        # Punti per scope
        punti_scope = giocatore.scope

        # Punto per primiera
        punteggio_primiera, dettagli_primiera = self.calcola_primiera(giocatore.carte_raccolte)
        punteggio_primiera_avv, dettagli_primiera_avv = self.calcola_primiera(giocatore_avversario.carte_raccolte)
        # Modifica: assegna punto primiera solo se il punteggio è strettamente maggiore
        punto_primiera = 1 if punteggio_primiera > punteggio_primiera_avv else 0

        # Somma tutti i punti
        punteggio_round = (
                carte_lungo +
                punto_denari +
                punto_settebello +
                punti_scope +
                punto_primiera
        )

        return punteggio_round, {
            'carte_lungo': carte_lungo,
            'carte_giocatore': carte_giocatore,
            'carte_avversario': carte_avversario,
            'denari': denari_giocatore,
            'denari_avversario': denari_avversario,
            'settebello': punto_settebello,
            'scope': punti_scope,
            'primiera': punto_primiera,
            'punteggio_primiera': punteggio_primiera,
            'punteggio_primiera_avv': punteggio_primiera_avv,
            'dettagli_primiera': dettagli_primiera,
            'dettagli_primiera_avv': dettagli_primiera_avv,
            'totale': punteggio_round
        }

    def aggiungi_punteggio(self, punti):
        """Aggiunge punti al punteggio totale"""
        self.punteggio_totale += punti