from Carta import Carta
from Mazzo import Mazzo
from Tavolo import Tavolo
from Giocatore import Giocatore

def main():
    # Creiamo un mazzo
    mazzo = Mazzo()

    # Stampa il mazzo iniziale
    print("Mazzo iniziale:")
    mazzo.stampa_mazzo()

    # Crea un tavolo e un giocatore
    tavolo = Tavolo()
    giocatore = Giocatore()

    # Aggiungi le prime 4 carte al tavolo
    print("\nAggiungo le prime 4 carte al tavolo:")
    for carta in mazzo.carte[:4]:  # Aggiungi solo le prime 4 carte
        tavolo.aggiungi_carta(carta, mazzo)

    # Stampa le carte sul tavolo
    print("\nCarte sul tavolo dopo l'aggiunta:")
    tavolo.stampa_carte()

    # Aggiungi una carta alla mano del giocatore
    print("\nAggiungo la prima carta alla mano del giocatore:")
    giocatore.aggiungi_mano(mazzo.carte[0], mazzo)

    # Stampa le carte in mano al giocatore
    print("\nCarte in mano al giocatore:")
    for carta in giocatore.carte_mano:
        print(carta)

    # Stampa il mazzo dopo che sono state distribuite alcune carte
    print("\nMazzo dopo la distribuzione:")
    mazzo.stampa_mazzo()

    # Rimuovi una carta dal tavolo
    print("\nRimuovo una carta dal tavolo (ad esempio la prima carta):")
    tavolo.elimina_carta(tavolo.carte[0])

    # Stampa le carte sul tavolo dopo la rimozione
    print("\nCarte sul tavolo dopo la rimozione:")
    tavolo.stampa_carte()

    # Rimuovi una carta dal mazzo (ad esempio la seconda carta)
    print("\nRimuovo una carta dal mazzo (ad esempio la seconda carta):")
    mazzo.elimina_carta(mazzo.carte[1])

    # Stampa il mazzo dopo la rimozione
    print("\nMazzo dopo la rimozione di una carta:")
    mazzo.stampa_mazzo()

if __name__ == "__main__":
    main()
