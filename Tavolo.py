
from Carta import Carta
from Mazzo import Mazzo

class Tavolo:

    def __init__(self):
        self.carte = []

    def aggiungi_carta_da_mazzo(self, Carta, Mazzo):
        self.carte.append(Carta)
        Mazzo.elimina_carta(Carta)

    def aggiungi_carta_da_giocatore(self, Carta):
        self.carte.append(Carta)

    def elimina_carta(self, carta):
        try:
            self.carte.remove(carta)  # Rimuove la carta dalla lista
            #print(f"Carta {carta} rimossa dal tavolo.")
        except ValueError:
            print("La carta non è presente sul tavolo.")



    def stampa_carte(self):
        for carta in self.carte:
            print(carta)



