import os
import time

class Giocatore:
    def __init__(self):
        self.carte_mano = []
        self.carte_raccolte = []
        self.scope = 0

    def clear_screen(self):
        """Pulisce lo schermo del terminale."""
        if os.name == 'nt':  # Per Windows
            os.system('cls')
        else:  # Per Unix/Linux/MacOS
            try:
                os.system('clear')
            except:
                print('\n' * 100)  # Fallback se clear non funziona

    def print_separator(self):
        """Stampa un separatore decorativo."""
        print("\n" + "═" * 50 + "\n")

    def aggiungi_mano(self, Carta, Mazzo):
        self.carte_mano.append(Carta)
        Mazzo.elimina_carta(Carta)

    def trova_combinazioni(self, numero, carte_tavolo, combinazione_corrente, tutte_combinazioni):
        """Trova tutte le combinazioni di carte che sommano a un numero specifico"""
        if numero == 0:
            tutte_combinazioni.append(combinazione_corrente[:])
            return
        if numero < 0:
            return
        for i in range(len(carte_tavolo)):
            self.trova_combinazioni(
                numero - carte_tavolo[i].valore,
                carte_tavolo[i + 1:],
                combinazione_corrente + [carte_tavolo[i]],
                tutte_combinazioni
            )

    def cerca_prese_possibili(self, carta_giocata, carte_tavolo):
        """Cerca tutte le possibili prese con una carta"""
        prese_possibili = []

        # Cerca le prese dirette (stesso valore)
        prese_dirette = [carta for carta in carte_tavolo if carta.valore == carta_giocata.valore]

        # Aggiungi ogni presa diretta come una combinazione separata
        for carta in prese_dirette:
            prese_possibili.append([carta])

        # Cerca le combinazioni di somme solo se non ci sono prese dirette
        if not prese_dirette:
            tutte_combinazioni = []
            self.trova_combinazioni(carta_giocata.valore, carte_tavolo, [], tutte_combinazioni)

            # Filtra le combinazioni per evitare duplicati
            for combo in tutte_combinazioni:
                if combo not in prese_possibili and len(combo) > 1:
                    prese_possibili.append(combo)

        return prese_possibili

    def mostra_combinazioni(self, carta_giocata, combinazioni):
        """Mostra tutte le combinazioni possibili in modo chiaro"""
        self.clear_screen()
        print(f"\n🎴 Hai giocato: {carta_giocata}")
        self.print_separator()
        print("📍 Combinazioni disponibili:")

        for i, combinazione in enumerate(combinazioni, 1):
            if len(combinazione) == 1:
                print(f"\n{i}: Prendi la singola carta: {combinazione[0]}")
            else:
                carte_str = " + ".join(str(carta) for carta in combinazione)
                somma = sum(carta.valore for carta in combinazione)
                print(f"\n{i}: Prendi la combinazione ({somma}):")
                print(f"   {carte_str}")

        self.print_separator()

    def get_valid_choice(self, max_choice):
        """Ottiene una scelta valida dall'utente"""
        while True:
            try:
                choice = input("🎮 Scegli quale combinazione prendere: ")
                choice = int(choice)
                if 1 <= choice <= max_choice:
                    return choice
                print(f"\n⚠️  Scelta non valida. Inserisci un numero tra 1 e {max_choice}")
            except ValueError:
                print("\n⚠️  Input non valido. Inserisci un numero.")

    def raccogli_carte(self, carta_giocata, carte_prese, tavolo):
        """Raccoglie le carte dal tavolo"""
        # Prima rimuoviamo le carte dal tavolo
        for carta in carte_prese:
            tavolo.elimina_carta(carta)
            self.carte_raccolte.append(carta)

        # Poi aggiungiamo la carta giocata alle carte raccolte
        self.carte_raccolte.append(carta_giocata)

        # La scopa viene assegnata solo se il tavolo è vuoto e non è l'ultima mano
        if len(tavolo.carte) == 0 and len(self.carte_mano) > 0:
            self.scope += 1
            print("\n🌟 SCOPA! 🌟")
            time.sleep(1.5)

    def gioca_mano(self, tavolo):
        """Permette al giocatore di scegliere una carta e gestisce la raccolta"""
        if not self.carte_mano:
            return False

        # Se è presente un agente IA, usa l'IA per giocare
        if hasattr(self, 'agente_ia'):
            carta_da_giocare = self.agente_ia.scegli_mossa(tavolo)
            prese_possibili = self.cerca_prese_possibili(carta_da_giocare, tavolo.carte)

            if prese_possibili:
                # Scegli automaticamente la miglior presa
                miglior_presa = max(prese_possibili, key=lambda x: (len(x), sum(c.valore for c in x)))
                self.raccogli_carte(carta_da_giocare, miglior_presa, tavolo)
                print(
                    f"\n🤖 IA ha giocato {carta_da_giocare} e raccolto: {' + '.join(str(carta) for carta in miglior_presa)}")
            else:
                tavolo.aggiungi_carta_da_giocatore(carta_da_giocare)
                print(f"\n🤖 IA ha lasciato {carta_da_giocare} sul tavolo")

            self.carte_mano.remove(carta_da_giocare)
            return bool(prese_possibili)

        while True:  # Continua a chiedere input finché non è valido
            try:
                scelta = input(f"\nScegli una carta da giocare (1-{len(self.carte_mano)}): ")
                if scelta.lower() == 'q':  # Opzionale: permette di uscire dal gioco
                    raise KeyboardInterrupt

                scelta = int(scelta)
                if not (1 <= scelta <= len(self.carte_mano)):
                    print("⚠️  Scelta non valida. Inserisci un numero tra 1 e", len(self.carte_mano))
                    time.sleep(1)
                    continue  # Torna all'inizio del ciclo while

                carta_da_giocare = self.carte_mano[scelta - 1]
                prese_possibili = self.cerca_prese_possibili(carta_da_giocare, tavolo.carte)
                ha_fatto_presa = False

                if prese_possibili:
                    if len(prese_possibili) == 1:
                        self.raccogli_carte(carta_da_giocare, prese_possibili[0], tavolo)
                        print(f"\n✅ Presa automatica: {' + '.join(str(carta) for carta in prese_possibili[0])}")
                        ha_fatto_presa = True
                    else:
                        self.mostra_combinazioni(carta_da_giocare, prese_possibili)
                        scelta_presa = self.get_valid_choice(len(prese_possibili))
                        self.raccogli_carte(carta_da_giocare, prese_possibili[scelta_presa - 1], tavolo)
                        print("\n✅ Carte raccolte con successo!")
                        ha_fatto_presa = True
                else:
                    tavolo.aggiungi_carta_da_giocatore(carta_da_giocare)
                    print("\n📌 Nessuna presa possibile, carta lasciata sul tavolo")

                self.carte_mano.remove(carta_da_giocare)
                time.sleep(1.5)
                return ha_fatto_presa

            except ValueError:
                print("⚠️  Input non valido. Inserisci un numero.")
                time.sleep(1)
                continue

    def mostra_mano(self):
        """Stampa le carte in mano del giocatore con un indice dinamico."""
        for i, carta in enumerate(self.carte_mano, 1):  # l'indice parte da 1
            print(f"{i}: {carta}")
