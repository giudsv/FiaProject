from GameEngine.Carta import Carta
import random

class Mazzo:
    def __init__(self):
        self.carte=self.crea_mazzo()
        self.mescola()

    def crea_mazzo(self):
        semi=Carta.Seme
        valori=range (1, 11)
        return [Carta.da_sigla(f"{valore}{seme}") for seme in semi for valore in valori]

    def elimina_carta(self, carta):
        try:
            self.carte.remove(carta)  # Rimuove la carta dalla lista
            #print(f"Carta {carta} rimossa dal mazzo.")
        except ValueError:
            print("La carta non è presente sul tavolo.")

    def mescola(self):
        random.shuffle(self.carte)

    def stampa_mazzo(self):
        for carta in self.carte:
            print(carta)

