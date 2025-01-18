from Carta import Carta
from Tavolo import Tavolo
from Mazzo import Mazzo

class Giocatore:
    def __init__(self):
        self.carte_mano = []
        self.carte_raccolte = []

    def aggiungi_mano(self,Carta, Mazzo):
        self.carte_mano.append(Carta)
        Mazzo.elimina_carta(Carta)
        print(f"Carta {Carta} in mano al giocatore.")

    def gioca_mano(self, Tavolo):
        self.carte_mano.append(Carta)