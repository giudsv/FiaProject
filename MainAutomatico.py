from Carta import Carta
from Mazzo import Mazzo
from Tavolo import Tavolo
from GiocatoreAutomatico import GiocatoreAutomatico
from Punteggio import Punteggio
import time
import json
from datetime import datetime


def salva_risultati(round_num, dettagli_g1, dettagli_g2, punteggi, nome_file=None):
    """Salva i risultati della partita in un file JSON"""
    if nome_file is None:
        nome_file = f"risultati_scopa_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    risultati = {
        "data_partita": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "numero_round": round_num,
        "punteggio_finale": {
            "giocatore1": punteggi[0].punteggio_totale,
            "giocatore2": punteggi[1].punteggio_totale
        },
        "dettagli_round": {
            f"round_{round_num}": {
                "giocatore1": dettagli_g1,
                "giocatore2": dettagli_g2
            }
        }
    }

    with open(nome_file, 'w', encoding='utf-8') as f:
        json.dump(risultati, f, indent=4, ensure_ascii=False)


def gioca_round_automatico(giocatori, punteggi):
    """Versione automatizzata di gioca_round"""
    mazzo = Mazzo()
    tavolo = Tavolo()
    ultimo_giocatore_presa = None

    # Distribuzione iniziale
    for _ in range(4):  # Carte sul tavolo
        if mazzo.carte:
            carta = mazzo.carte[0]
            tavolo.aggiungi_carta_da_mazzo(carta, mazzo)

    while True:
        # Distribuisci 3 carte a ogni giocatore
        if all(len(g.carte_mano) == 0 for g in giocatori):
            if len(mazzo.carte) > 0:
                for giocatore in giocatori:
                    for _ in range(3):
                        if mazzo.carte:
                            carta = mazzo.carte[0]
                            giocatore.aggiungi_mano(carta, mazzo)
            else:
                if ultimo_giocatore_presa is not None and tavolo.carte:
                    for carta in tavolo.carte[:]:
                        giocatori[ultimo_giocatore_presa].carte_raccolte.append(carta)
                        tavolo.elimina_carta(carta)
                break

        # Gioca un turno per ogni giocatore
        for i, giocatore in enumerate(giocatori):
            if len(giocatore.carte_mano) > 0:
                if giocatore.gioca_mano(tavolo):
                    ultimo_giocatore_presa = i

    # Calcola i punteggi
    punti_g1, dettagli_g1 = punteggi[0].calcola_punteggio_round(giocatori[0], giocatori[1])
    punti_g2, dettagli_g2 = punteggi[1].calcola_punteggio_round(giocatori[1], giocatori[0])

    punteggi[0].aggiungi_punteggio(punti_g1)
    punteggi[1].aggiungi_punteggio(punti_g2)

    return dettagli_g1, dettagli_g2


def main_automatico(num_partite=1):
    """Esegue più partite automatiche e salva i risultati"""
    for partita in range(num_partite):
        print(f"\nPartita {partita + 1} di {num_partite}")

        giocatori = [GiocatoreAutomatico("Bot1"), GiocatoreAutomatico("Bot2")]
        punteggi = [Punteggio(), Punteggio()]

        round_num = 1
        while True:
            print(f"Giocando round {round_num}...")
            dettagli_g1, dettagli_g2 = gioca_round_automatico(giocatori, punteggi)

            # Salva i risultati di ogni round
            salva_risultati(
                round_num,
                dettagli_g1,
                dettagli_g2,
                punteggi,
                f"partita_{partita + 1}_round_{round_num}.json"
            )

            if punteggi[0].punteggio_totale >= 11 or punteggi[1].punteggio_totale >= 11:
                vincitore = "Bot1" if punteggi[0].punteggio_totale > punteggi[1].punteggio_totale else "Bot2"
                print(f"Partita {partita + 1} completata! Vince {vincitore}")
                print(f"Punteggio finale: Bot1: {punteggi[0].punteggio_totale}, Bot2: {punteggi[1].punteggio_totale}")
                break

            round_num += 1
            for giocatore in giocatori:
                giocatore.carte_mano = []
                giocatore.carte_raccolte = []
                giocatore.scope = 0


if __name__ == "__main__":
    try:
        num_partite = int(input("Quante partite vuoi simulare? "))
        main_automatico(num_partite)
    except KeyboardInterrupt:
        print("\n\nSimulazione interrotta.")
    except ValueError:
        print("\nPer favore inserisci un numero valido di partite.")