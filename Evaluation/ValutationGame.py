import os
import time
from datetime import datetime
from copy import deepcopy

from GameEngine.Mazzo import Mazzo
from GameEngine.Tavolo import Tavolo
from GameEngine.Giocatore import Giocatore
from GameEngine.Punteggio import Punteggio
from Agent.AgenteMonteCarlo import AgenteMonteCarlo


def gioca_round_ai(giocatori, punteggi, turno_iniziale):
    mazzo = Mazzo()
    tavolo = Tavolo()
    ultimo_giocatore_presa = None

    # Setup AI agents
    giocatori[0].agente_ia = AgenteMonteCarlo(giocatori[0])
    giocatori[1].agente_ia = AgenteMonteCarlo(giocatori[1])

    # Initial distribution
    for _ in range(4):  # Table cards
        if mazzo.carte:
            carta = mazzo.carte[0]
            tavolo.aggiungi_carta_da_mazzo(carta, mazzo)

    for giocatore in giocatori:  # Player cards
        for _ in range(3):
            if mazzo.carte:
                carta = mazzo.carte[0]
                giocatore.aggiungi_mano(carta, mazzo)

    # Game round loop
    turno = turno_iniziale  # Inizia dal giocatore giusto
    while True:
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

        giocatore_corrente = giocatori[turno % 2]

        if len(giocatore_corrente.carte_mano) > 0:
            carta_da_giocare = giocatore_corrente.agente_ia.scegli_mossa(tavolo)
            prese_possibili = giocatore_corrente.cerca_prese_possibili(carta_da_giocare, tavolo.carte)

            if prese_possibili:
                miglior_presa = max(prese_possibili, key=lambda x: (len(x), sum(c.valore for c in x)))
                giocatore_corrente.raccogli_carte(carta_da_giocare, miglior_presa, tavolo)
                ultimo_giocatore_presa = turno % 2
            else:
                tavolo.aggiungi_carta_da_giocatore(carta_da_giocare)

            giocatore_corrente.carte_mano.remove(carta_da_giocare)

        turno += 1

    punti_g1, dettagli_g1 = punteggi[0].calcola_punteggio_round(giocatori[0], giocatori[1])
    punti_g2, dettagli_g2 = punteggi[1].calcola_punteggio_round(giocatori[1], giocatori[0])

    punteggi[0].aggiungi_punteggio(punti_g1)
    punteggi[1].aggiungi_punteggio(punti_g2)

    return dettagli_g1, dettagli_g2, turno



def crea_report(num_partite, statistiche, tempi, punteggi_partite):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = f"reports/report_{timestamp}.txt"
    os.makedirs("reports", exist_ok=True)

    with open(report_path, "w") as f:
        f.write("=== REPORT VALUTAZIONE AGENTE MONTE CARLO ===\n\n")

        # Tempo di esecuzione
        f.write(f"Tempo totale di esecuzione: {tempi['totale']:.2f} secondi\n")
        f.write(f"Tempo medio per partita: {tempi['medio']:.2f} secondi\n\n")

        # Statistiche generali
        f.write(f"Numero totale partite: {num_partite}\n")
        f.write(f"Vittorie Agente 1: {statistiche['vittorie_g1']}\n")
        f.write(f"Vittorie Agente 2: {statistiche['vittorie_g2']}\n")
        f.write(f"Durata media partita (round): {statistiche['media_round']:.2f}\n")
        f.write(f"Punteggio medio Agente 1: {statistiche['media_punti_g1']:.2f}\n")
        f.write(f"Punteggio medio Agente 2: {statistiche['media_punti_g2']:.2f}\n")
        f.write(f"Scope totali Agente 1: {statistiche['scope_g1']}\n")
        f.write(f"Scope totali Agente 2: {statistiche['scope_g2']}\n\n")

        # Dettagli per ogni partita
        f.write("=== DETTAGLI PARTITE ===\n")
        for i, (punteggio_g1, punteggio_g2, tempo_partita) in enumerate(punteggi_partite, 1):
            f.write(f"Partita {i}:\n")
            f.write(f"Punteggio Agente 1: {punteggio_g1}\n")
            f.write(f"Punteggio Agente 2: {punteggio_g2}\n")
            f.write(f"Tempo partita: {tempo_partita:.2f} secondi\n\n")

    return report_path


def main(num_partite=100):
    start_time_total = time.time()

    statistiche = {
        'vittorie_g1': 0,
        'vittorie_g2': 0,
        'totale_round': 0,
        'totale_punti_g1': 0,
        'totale_punti_g2': 0,
        'scope_g1': 0,
        'scope_g2': 0
    }

    punteggi_partite = []
    tempi_partite = []

    for partita in range(num_partite):
        start_time_game = time.time()

        giocatori = [Giocatore(), Giocatore()]
        punteggi = [Punteggio(), Punteggio()]

        # Alterna chi inizia la partita (0 per Agente 1, 1 per Agente 2)
        turno_iniziale = partita % 2

        round_num = 0

        while True:
            dettagli_g1, dettagli_g2, num_turni = gioca_round_ai(giocatori, punteggi, turno_iniziale)
            round_num += 1

            statistiche['scope_g1'] += dettagli_g1['scope']
            statistiche['scope_g2'] += dettagli_g2['scope']

            if punteggi[0].punteggio_totale >= 11 or punteggi[1].punteggio_totale >= 11:
                statistiche['totale_round'] += round_num
                statistiche['totale_punti_g1'] += punteggi[0].punteggio_totale
                statistiche['totale_punti_g2'] += punteggi[1].punteggio_totale

                tempo_partita = time.time() - start_time_game
                tempi_partite.append(tempo_partita)
                punteggi_partite.append((punteggi[0].punteggio_totale, punteggi[1].punteggio_totale, tempo_partita))

                if punteggi[0].punteggio_totale > punteggi[1].punteggio_totale:
                    statistiche['vittorie_g1'] += 1
                else:
                    statistiche['vittorie_g2'] += 1
                break

            for giocatore in giocatori:
                giocatore.carte_mano = []
                giocatore.carte_raccolte = []
                giocatore.scope = 0


    tempo_totale = time.time() - start_time_total

    statistiche['media_round'] = statistiche['totale_round'] / num_partite
    statistiche['media_punti_g1'] = statistiche['totale_punti_g1'] / num_partite
    statistiche['media_punti_g2'] = statistiche['totale_punti_g2'] / num_partite

    tempi = {
        'totale': tempo_totale,
        'medio': tempo_totale / num_partite
    }

    report_path = crea_report(num_partite, statistiche, tempi, punteggi_partite)
    print(f"Report creato: {report_path}")


if __name__ == "__main__":
    num_partite = int(input("Inserisci il numero di partite da simulare: "))
    main(num_partite)