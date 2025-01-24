from Carta import Carta
import random
from typing import List, Optional

class AgenteMonteCarlo:
    def __init__(self, giocatore):
        self.giocatore = giocatore
        self.simulazioni = 100  # Numero di simulazioni Monte Carlo

    def scegli_mossa(self, tavolo):
        """
        Sceglie la mossa migliore usando simulazioni Monte Carlo
        e le euristiche definite
        """
        # Ottieni le mosse possibili
        mosse_possibili = self.giocatore.carte_mano

        if not mosse_possibili:
            return None

        # Se c'è solo una carta, giocala
        if len(mosse_possibili) == 1:
            return mosse_possibili[0]

        # Valuta ogni carta con simulazioni Monte Carlo
        valutazioni = {}
        for carta in mosse_possibili:
            punteggio_medio = self.valuta_carta(carta, tavolo)
            valutazioni[carta] = punteggio_medio

        # Scegli la carta con punteggio migliore
        return max(valutazioni, key=valutazioni.get)

    def valuta_carta(self, carta, tavolo):
        """
        Valuta una carta attraverso simulazioni Monte Carlo
        """
        punteggi_totali = 0

        for _ in range(self.simulazioni):
            # Crea una copia del tavolo per la simulazione
            tavolo_simulato = tavolo.__class__()
            tavolo_simulato.carte = tavolo.carte.copy()

            # Trova le prese possibili
            prese_possibili = self.giocatore.cerca_prese_possibili(carta, tavolo_simulato.carte)

            # Valuta le prese
            if prese_possibili:
                # Scegli la miglior combinazione (più carte o carte di valore)
                miglior_presa = max(prese_possibili, key=lambda x: (len(x), sum(c.valore for c in x)))
                punteggio_presa = len(miglior_presa) + sum(c.valore for c in miglior_presa)
                punteggi_totali += punteggio_presa

                # Bonus per scopa
                if len(tavolo_simulato.carte) - len(miglior_presa) == 0:
                    punteggi_totali += 5  # Bonus per scopa

        # Calcola il punteggio medio
        return punteggi_totali / self.simulazioni

