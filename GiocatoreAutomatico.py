from Giocatore import Giocatore
from Carta import Carta

class GiocatoreAutomatico(Giocatore):
    def __init__(self, nome="Bot"):
        super().__init__()
        self.nome = nome

    def gioca_mano(self, tavolo):
        """Versione automatizzata di gioca_mano che sceglie la prima carta disponibile e la prima presa possibile"""
        if not self.carte_mano:
            return False

        # Sceglie la prima carta disponibile
        carta_da_giocare = self.carte_mano[0]
        prese_possibili = self.cerca_prese_possibili(carta_da_giocare, tavolo.carte)
        ha_fatto_presa = False

        if prese_possibili:
            # Sceglie sempre la prima presa disponibile
            self.raccogli_carte(carta_da_giocare, prese_possibili[0], tavolo)
            ha_fatto_presa = True
        else:
            tavolo.aggiungi_carta_da_giocatore(carta_da_giocare)

        self.carte_mano.remove(carta_da_giocare)
        return ha_fatto_presa