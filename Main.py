from GameEngine.Mazzo import Mazzo
from GameEngine.Tavolo import Tavolo
from GameEngine.Giocatore import Giocatore
from GameEngine.Punteggio import Punteggio
from GameEngine.Carta import Carta
import os
import time
from Agent.AgenteMonteCarlo import AgenteMonteCarlo

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
    # Prima distribuisci le carte sul tavolo solo all'inizio della partita
    if tavolo.carte == [] and all(len(g.carte_raccolte) == 0 for g in giocatori):  # Controlla se è l'inizio della partita
        print("\n🎴 Distribuisco le carte sul tavolo...")
        for _ in range(4):
            if mazzo.carte:
                carta = mazzo.carte[0]
                tavolo.aggiungi_carta_da_mazzo(carta, mazzo)
       # time.sleep(1)

    # Poi distribuisci ai giocatori
    print("🎴 Distribuisco le carte ai giocatori...")
    for giocatore in giocatori:
        for _ in range(num_carte):
            if mazzo.carte:
                carta = mazzo.carte[0]
                giocatore.aggiungi_mano(carta, mazzo)
   # time.sleep(1)


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


def ordina_carte_per_seme(carte):
    """Ordina le carte per seme e valore"""
    carte_per_seme = {
        'Bastoni': [],
        'Coppe': [],
        'Denari': [],
        'Spade': []
    }

    # Raggruppa le carte per seme
    for carta in carte:
        carte_per_seme[carta.seme].append(carta)

    # Ordina le carte di ogni seme per valore
    for seme in carte_per_seme:
        carte_per_seme[seme].sort(key=lambda x: x.valore)

    return carte_per_seme


def mostra_carte_raccolte(giocatore_num, carte):
    """Mostra le carte raccolte ordinate per seme"""
    print(f"\n🎮 Carte raccolte dal Giocatore {giocatore_num}:")
    print("═" * 45)

    carte_ordinate = ordina_carte_per_seme(carte)
    for seme, carte_seme in carte_ordinate.items():
        if carte_seme:  # Mostra il seme solo se ci sono carte
            print(f"\n{seme}:", end=" ")
            valori = [str(carta.valore) for carta in carte_seme]
            print(", ".join(valori))


def spiega_punteggio(g1_details, g2_details):
    """Spiega come sono stati assegnati i punteggi"""
    print("\n📝 Dettaglio punteggi:")
    print("═" * 45)

    # Carte lungo
    print(f"\n• Carte raccolte:")
    print(f"  Giocatore 1: {g1_details['carte_giocatore']} carte")
    print(f"  Giocatore 2: {g2_details['carte_giocatore']} carte")
    if g1_details['carte_lungo']:
        print("  ➜ Punto carte lungo al Giocatore 1")
    elif g2_details['carte_lungo']:
        print("  ➜ Punto carte lungo al Giocatore 2")
    else:
        print("  ➜ Nessun punto assegnato (parità)")

    # Denari
    print(f"\n• Carte di denari:")
    print(f"  Giocatore 1: {g1_details['denari']} denari")
    print(f"  Giocatore 2: {g2_details['denari']} denari")
    if g1_details['denari'] > g2_details['denari']:
        print("  ➜ Punto denari al Giocatore 1")
    elif g2_details['denari'] > g1_details['denari']:
        print("  ➜ Punto denari al Giocatore 2")
    else:
        print("  ➜ Nessun punto assegnato (parità)")

    # Settebello
    print("\n• Settebello (7 di denari):")
    if g1_details['settebello']:
        print("  ➜ Punto settebello al Giocatore 1")
    elif g2_details['settebello']:
        print("  ➜ Punto settebello al Giocatore 2")
    else:
        print("  ➜ Nessun punto assegnato")

    # Scope
    print("\n• Scope:")
    if g1_details['scope'] > 0 or g2_details['scope'] > 0:
        if g1_details['scope'] > 0:
            print(f"  ➜ {g1_details['scope']} punti al Giocatore 1")
        if g2_details['scope'] > 0:
            print(f"  ➜ {g2_details['scope']} punti al Giocatore 2")
    else:
        print("  ➜ Nessuna scopa realizzata")

    # Primiera
    print("\n• Primiera:")
    print(f"  Giocatore 1: {g1_details['punteggio_primiera']} punti")
    print(f"  Giocatore 2: {g2_details['punteggio_primiera_avv']} punti")
    if g1_details['primiera']:
        print("  ➜ Punto primiera al Giocatore 1")
    elif g2_details['primiera']:
        print("  ➜ Punto primiera al Giocatore 2")
    else:
        print("  ➜ Nessun punto assegnato (parità)")


def mostra_punteggio_round(punteggi_g1, punteggi_g2, giocatori):
    """Mostra i punteggi dettagliati del round e le carte raccolte"""
    print("\n📊 Punteggi del round:")
    print("\nCategoria       Giocatore 1  Giocatore 2")
    print("═" * 45)

    # Definizione delle categorie e loro nomi per la visualizzazione
    categorie = [
        ('carte_lungo', 'Carte lungo'),
        ('denari', 'Denari'),
        ('settebello', 'Settebello'),
        ('scope', 'Scope'),
        ('primiera', 'Primiera'),
        ('totale', 'TOTALE')
    ]

    # Stampa ogni categoria con il suo punteggio
    for chiave, nome in categorie:
        # Per ogni categoria, mostriamo 1 se il punto è stato assegnato, 0 altrimenti
        if chiave == 'scope':
            g1 = punteggi_g1[chiave]  # Per le scope, mostriamo il numero effettivo
            g2 = punteggi_g2[chiave]
        elif chiave == 'totale':
            g1 = punteggi_g1[chiave]  # Per il totale, mostriamo la somma
            g2 = punteggi_g2[chiave]
        else:
            # Per tutte le altre categorie, mostriamo 1 o 0
            g1 = 1 if punteggi_g1[chiave] else 0
            g2 = 1 if punteggi_g2[chiave] else 0

        # Formatta l'output con spaziatura fissa
        print(f"{nome:<14} {g1:^11} {g2:^11}")

    # Mostra le carte raccolte
    mostra_carte_raccolte(1, giocatori[0].carte_raccolte)
    mostra_carte_raccolte(2, giocatori[1].carte_raccolte)

    # Spiega l'assegnazione dei punteggi in dettaglio
    spiega_punteggio(punteggi_g1, punteggi_g2)


def mostra_punteggio_totale(punteggio_g1, punteggio_g2):
    """Mostra il punteggio totale della partita"""
    print("\n🏆 PUNTEGGIO TOTALE PARTITA:")
    print("═" * 45)
    print(f"Giocatore 1: {punteggio_g1.punteggio_totale} punti")
    print(f"Giocatore 2: {punteggio_g2.punteggio_totale} punti")


def gioca_round(giocatori, punteggi):
    """Gestisce un singolo round di gioco"""
    mazzo = Mazzo()
    tavolo = Tavolo()
    ultimo_giocatore_presa = None
    primo_giro = True  # Flag per tracciare se siamo al primo giro

    # Aggiungi l'AgenteMonteCarlo al secondo giocatore
    giocatori[1].agente_ia = AgenteMonteCarlo(giocatori[1])

    # Distribuzione iniziale
    distribuisci_carte(mazzo, tavolo, giocatori, 3)

    # Ciclo di gioco del round
    turno = 0
    while True:
        # Controlla se è necessario ridistribuire le carte
        if all(len(g.carte_mano) == 0 for g in giocatori):
            if len(mazzo.carte) > 0:
                print("\n🎴 Distribuisco nuove carte...")
                # Distribuisci solo ai giocatori, non sul tavolo
                for giocatore in giocatori:
                    for _ in range(3):
                        if mazzo.carte:
                            carta = mazzo.carte[0]
                            giocatore.aggiungi_mano(carta, mazzo)
               # time.sleep(1)
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
            # Per il giocatore 1, mantieni il comportamento originale
            if turno % 2 == 0:
                ha_fatto_presa = giocatore_corrente.gioca_mano(tavolo)
            else:
                # Per il giocatore 2 (IA), usa l'AgenteMonteCarlo
                carta_da_giocare = giocatore_corrente.agente_ia.scegli_mossa(tavolo)
                prese_possibili = giocatore_corrente.cerca_prese_possibili(carta_da_giocare, tavolo.carte)

                if prese_possibili:
                    # Scegli automaticamente la miglior presa
                    miglior_presa = max(prese_possibili, key=lambda x: (len(x), sum(c.valore for c in x)))
                    giocatore_corrente.raccogli_carte(carta_da_giocare, miglior_presa, tavolo)

                    # Stampa le mosse dell'IA per il giocatore 1
                    print(f"\n🤖 IA ha giocato {carta_da_giocare}")
                    print(f"🤖 Carte prese: {' + '.join(str(carta) for carta in miglior_presa)}")

                    ha_fatto_presa = True
                else:
                    tavolo.aggiungi_carta_da_giocatore(carta_da_giocare)
                    print(f"\n🤖 IA ha lasciato {carta_da_giocare} sul tavolo")
                    ha_fatto_presa = False

                giocatore_corrente.carte_mano.remove(carta_da_giocare)

                # Pausa per permettere al giocatore 1 di leggere le mosse dell'IA
                input("\nPremi Enter per continuare...")

            if ha_fatto_presa:
                ultimo_giocatore_presa = turno % 2

        turno += 1

    # Resto del codice rimane invariato
    punti_g1, dettagli_g1 = punteggi[0].calcola_punteggio_round(giocatori[0], giocatori[1])
    punti_g2, dettagli_g2 = punteggi[1].calcola_punteggio_round(giocatori[1], giocatori[0])

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
        mostra_punteggio_round(dettagli_g1, dettagli_g2, giocatori)
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


