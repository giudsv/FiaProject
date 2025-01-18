class Carta:
    Seme = {
        'C': 'Coppe',
        'B': 'Bastoni',
        'D': 'Denari',
        'S': 'Spade'
    }

    def __init__(self, valore, seme):
        self.valore=valore
        self.seme=seme

    def __str__(self):
        return f"{self.seme} {self.valore}"

    @classmethod
    def da_sigla(cls, sigla):
        """Crea una carta a partire da una sigla come '1C'."""
        valore = int(sigla[:-1])  # Tutto tranne l'ultima lettera
        seme_lettera = sigla[-1].upper()  # Ultima lettera, in maiuscolo

        # Controlla se la lettera è valida
        if seme_lettera in cls.Seme and 1 <= valore <= 10:
            seme = cls.Seme[seme_lettera]
            return cls(seme, valore)
        else:
            raise ValueError("Sigla non valida.")

