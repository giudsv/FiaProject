from Carta import Carta
from Mazzo import Mazzo
from Tavolo import Tavolo
from Giocatore import Giocatore
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
    """Mostra lo stato corrente del gioco con la nuova interfaccia."""
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


def main():
    clear_screen()
    print_banner()

    # Inizializzazione del gioco con 2 giocatori fissi
    mazzo = Mazzo()
    tavolo = Tavolo()
    giocatori = [Giocatore(), Giocatore()]
    ultimo_giocatore_presa = None

    # Distribuzione iniziale
    distribuisci_carte(mazzo, tavolo, giocatori, 3)

    # Ciclo di gioco
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
            # Gestisci la presa e aggiorna l'ultimo giocatore che ha fatto presa
            if giocatore_corrente.gioca_mano(tavolo):
                ultimo_giocatore_presa = turno % 2

            input("\nPremi Enter per continuare...")

        turno += 1

    # Fine del gioco
    clear_screen()
    print_banner()
    print("\n🏁 Partita terminata!")
    print("\n📊 Punteggi finali:")
    for i, giocatore in enumerate(giocatori, 1):
        print(f"\nGiocatore {i}:")
        print(f"Scope: {giocatore.scope}")
        print(f"Carte raccolte: {len(giocatore.carte_raccolte)}")

    print_separator()
    input("\nPremi Enter per uscire...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()
        print("\n\n👋 Grazie per aver giocato! Arrivederci!\n")