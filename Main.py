from Carta import Carta
from Mazzo import Mazzo
from Tavolo import Tavolo
from Giocatore import Giocatore
from Punteggio import Punteggio
import os
import time


def clear_screen():
    """Pulisce lo schermo del terminale in modo cross-platform."""
    if os.name == 'nt':  # Per Windows
        os.system('cls')
    else:  # Per Unix/Linux/MacOS
        try:
            os.system('clear')
        except:
            print('\n' * 100)  # Fallback se clear non funziona


def print_banner():
    """Stampa il banner del gioco."""
    banner = """
    ╔═══════════════════════════════════════════╗
    ║             GIOCO DELLA SCOPA             ║
    ╚═══════════════════════════════════════════╝
    """
    print(banner)


def print_separator():
    """Stampa un separatore decorativo."""
    print("\n" + "═" * 50 + "\n")


def distribuisci_carte(mazzo, tavolo, giocatori, num_carte):
    """Distribuisce le carte ai giocatori e sul tavolo."""
    # Prima distribuisci le carte sul tavolo
    if tavolo.carte == []:  # Solo se il tavolo è vuoto
        print("\n🎴 Distribuisco le carte sul tavolo...")
        for _ in range(4):
            if mazzo.carte:
                carta = mazzo.carte[0]
                tavolo.aggiungi_carta_da_mazzo(carta, mazzo)
        time.sleep(1)

    # Poi distribuisci ai giocatori
    print("🎴 Distribuisco le carte ai giocatori...")
    for giocatore in giocatori:
        for _ in range(num_carte):
            if mazzo.carte:
                carta = mazzo.carte[0]
                giocatore.aggiungi_mano(carta, mazzo)
    time.sleep(1)


def mostra_stato_gioco(giocatore_num, tavolo, giocatore_attivo, giocatore_inattivo):
    """Mostra lo stato corrente del gioco."""
    clear_screen()
    print("""    ╔═══════════════════════════════════════════╗
    ║             GIOCO DELLA SCOPA             ║
    ╚═══════════════════════════════════════════╝""")

    print(f"\n👤 Turno del Giocatore {giocatore_num}")
    print(f"🎯 Scope: {giocatore_attivo.scope}")
    print(f"📦 Carte raccolte: {len(giocatore_attivo.carte_raccolte)}")
    print("══════════════════════════════════════════════════")

    # Se è il giocatore 1
    if giocatore_num == 1:
        print("🎮 Le tue carte (Giocatore 1):")
        giocatore_attivo.mostra_mano()
        print("\n📍 Carte sul tavolo:")
        tavolo.stampa_carte()
        print("\n🎮 Giocatore 2:")
        print("[Carte nascoste]")
    # Se è il giocatore 2
    else:
        print("🎮 Giocatore 1:")
        print("[Carte nascoste]")
        print("\n📍 Carte sul tavolo:")
        tavolo.stampa_carte()
        print("\n🎮 Le tue carte (Giocatore 2):")
        giocatore_attivo.mostra_mano()

    print("══════════════════════════════════════════════════")


def mostra_punteggio_round(punteggi_g1, punteggi_g2):
    """Mostra i punteggi dettagliati del round"""
    print("\n📊 Punteggi del round:")
    print("\nCategoria       Giocatore 1  Giocatore 2")
    print("═" * 45)
    categorie = ['carte_lungo', 'denari', 'settebello', 'scope', 'primiera', 'totale']
    nomi = {
        'carte_lungo': 'Carte lungo',
        'denari': 'Denari',
        'settebello': 'Settebello',
        'scope': 'Scope',
        'primiera': 'Primiera',
        'totale': 'TOTALE'
    }

    for categoria in categorie:
        nome = nomi[categoria]
        g1 = punteggi_g1[categoria]
        g2 = punteggi_g2[categoria]
        print(f"{nome:<14} {g1:^11} {g2:^11}")


def mostra_punteggio_totale(punteggio_g1, punteggio_g2):
    """Mostra il punteggio totale della partita"""
    print("\n🏆 PUNTEGGIO TOTALE PARTITA:")
    print(f"Giocatore 1: {punteggio_g1.punteggio_totale}")
    print(f"Giocatore 2: {punteggio_g2.punteggio_totale}")


def gioca_round(giocatori, punteggi):
    """Gestisce un singolo round di gioco"""
    mazzo = Mazzo()
    tavolo = Tavolo()
    ultimo_giocatore_presa = None

    # Distribuzione iniziale
    distribuisci_carte(mazzo, tavolo, giocatori, 3)

    # Ciclo di gioco del round
    turno = 0
    while True:
        # Controlla se è necessario ridistribuire le carte
        if all(len(g.carte_mano) == 0 for g in giocatori):
            if len(mazzo.carte) > 0:
                print("\n🎴 Distribuisco nuove carte...")
                distribuisci_carte(mazzo, tavolo, giocatori, 3)
                time.sleep(1)
            else:
                # Assegna le carte rimanenti all'ultimo giocatore che ha fatto presa
                if ultimo_giocatore_presa is not None and tavolo.carte:
                    print(f"\nLe carte rimanenti vanno al Giocatore {ultimo_giocatore_presa + 1}")
                    for carta in tavolo.carte[:]:
                        giocatori[ultimo_giocatore_presa].carte_raccolte.append(carta)
                        tavolo.elimina_carta(carta)
                break

        giocatore_corrente = giocatori[turno % 2]
        giocatore_inattivo = giocatori[(turno + 1) % 2]
        giocatore_num = (turno % 2) + 1

        # Mostra lo stato del gioco
        mostra_stato_gioco(giocatore_num, tavolo, giocatore_corrente, giocatore_inattivo)

        # Gestione del turno
        if len(giocatore_corrente.carte_mano) > 0:
            if giocatore_corrente.gioca_mano(tavolo):
                ultimo_giocatore_presa = turno % 2

            input("\nPremi Enter per continuare...")

        turno += 1

    # Calcolo punteggi del round
    punti_g1, dettagli_g1 = punteggi[0].calcola_punteggio_round(giocatori[0], giocatori[1])
    punti_g2, dettagli_g2 = punteggi[1].calcola_punteggio_round(giocatori[1], giocatori[0])

    # Aggiorna i punteggi totali
    punteggi[0].aggiungi_punteggio(punti_g1)
    punteggi[1].aggiungi_punteggio(punti_g2)

    return dettagli_g1, dettagli_g2


def main():
    clear_screen()
    print_banner()

    # Inizializzazione dei giocatori e punteggi
    giocatori = [Giocatore(), Giocatore()]
    punteggi = [Punteggio(), Punteggio()]

    round_num = 1
    while True:
        print(f"\n🎮 Round {round_num}")
        print_separator()

        # Gioca il round
        dettagli_g1, dettagli_g2 = gioca_round(giocatori, punteggi)

        # Mostra i punteggi del round
        clear_screen()
        print_banner()
        print(f"\n🎯 Fine del Round {round_num}!")
        mostra_punteggio_round(dettagli_g1, dettagli_g2)
        mostra_punteggio_totale(punteggi[0], punteggi[1])

        # Controlla se qualcuno ha raggiunto o superato 11 punti
        if punteggi[0].punteggio_totale >= 11 or punteggi[1].punteggio_totale >= 11:
            print("\n🏆 PARTITA CONCLUSA! 🏆")
            # Se entrambi hanno superato 11 punti, vince chi ha il punteggio più alto
            if punteggi[0].punteggio_totale > punteggi[1].punteggio_totale:
                print("Vince il Giocatore 1!")
            else:
                print("Vince il Giocatore 2!")
            break

        # Prepara il prossimo round
        round_num += 1
        for giocatore in giocatori:
            giocatore.carte_mano = []
            giocatore.carte_raccolte = []
            giocatore.scope = 0

        input("\nPremi Enter per iniziare il prossimo round...")

    print_separator()
    input("\nPremi Enter per uscire...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()
        print("\n\n👋 Grazie per aver giocato! Arrivederci!\n")