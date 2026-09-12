import random

class PartitaBriscola:
    def __init__(self):
        self.giocatori_connessi = 0
        self.reset_partita()

    def reset_partita(self):
        # Valori delle carte per il calcolo dei punti
        self.valori_punti = {
            'Asso': 11, '3': 10, 'Re': 4, 'Cavallo': 3, 'Fante': 2,
            '7': 0, '6': 0, '5': 0, '4': 0, '2': 0
        }
        
        # Gerarchia di presa della singola carta
        self.gerarchia = {
            'Asso': 10, '3': 9, 'Re': 8, 'Cavallo': 7, 'Fante': 6,
            '7': 5, '6': 4, '5': 3, '4': 2, '2': 1
        }

        # Creazione del mazzo da 40 carte
        semi = ['Denari', 'Coppe', 'Spade', 'Bastoni']
        valori = list(self.valori_punti.keys())
        self.mazzo = [f"{seme} {valore}" for seme in semi for valore in valori]
        random.shuffle(self.mazzo)

        # Distribuzione iniziale (3 carte a testa)
        self.mano_g1 = [self.mazzo.pop() for _ in range(3)]
        self.mano_g2 = [self.mazzo.pop() for _ in range(3)]

        self.briscola = None
        self.prio = 1  # 1: Turno di G1, 2: Turno di G2
        self.punti_g1 = 0
        self.punti_g2 = 0
        
        # Carte attualmente sul tavolo nel turno corrente
        self.carta1_in_tavola = None
        self.carta2_in_tavola = None
        self.fase = "IN_CORSO"

    def imposta_briscola(self, seme):
        """Imposta il seme di briscola scelto dal Giocatore 1"""
        self.briscola = seme

    def gioca_carta_singola(self, num_giocatore, carta):
        """Gestisce la giocata di una carta da uno dei due schermi"""
        if self.fase == "FINITA":
            return

        # Il Giocatore 1 gioca la sua carta
        if num_giocatore == 1 and not self.carta1_in_tavola:
            if carta in self.mano_g1:
                self.mano_g1.remove(carta)
                self.carta1_in_tavola = carta

        # Il Giocatore 2 gioca la sua carta
        elif num_giocatore == 2 and not self.carta2_in_tavola:
            if carta in self.mano_g2:
                self.mano_g2.remove(carta)
                self.carta2_in_tavola = carta

        # Se entrambi i giocatori hanno giocato la carta, risolvi la mano
        if self.carta1_in_tavola and self.carta2_in_tavola:
            self.risolvi_turno()

    def risolvi_turno(self):
        """Confronta le carte in tavola, assegna i punti e distribuisce nuove carte"""
        seme1, val1 = self.carta1_in_tavola.split(' ')
        seme2, val2 = self.carta2_in_tavola.split(' ')

        punti_mano = self.valori_punti[val1] + self.valori_punti[val2]
        vincitore_mano = 1

        # Logica per determinare chi vince la mano
        if seme1 == seme2:
            if self.gerarchia[val2] > self.gerarchia[val1]:
                vincitore_mano = 2
        elif seme2 == self.briscola:
            vincitore_mano = 2

        # Se il primo a giocare nel turno era G2, invertiamo la logica di partenza
        if self.prio == 2:
            vincitore_mano = 2 if vincitore_mano == 1 else 1

        # Assegnazione punti e aggiornamento priorità di gioco
        if vincitore_mano == 1:
            self.punti_g1 += punti_mano
            self.prio = 1
        else:
            self.punti_g2 += punti_mano
            self.prio = 2

        # Resetta il tavolo
        self.carta1_in_tavola = None
        self.carta2_in_tavola = None

        # Pesca di nuove carte dal mazzo (se ce ne sono)
        if len(self.mazzo) >= 2:
            if self.prio == 1:
                self.mano_g1.append(self.mazzo.pop())
                self.mano_g2.append(self.mazzo.pop())
            else:
                self.mano_g2.append(self.mazzo.pop())
                self.mano_g1.append(self.mazzo.pop())

        # Controlla la fine della partita
        if not self.mano_g1 and not self.mano_g2:
            self.fase = "FINITA"

    def to_dict(self):
        """Converte lo stato del gioco in dizionario per inviarlo al browser via JSON"""
        return {
            "mano_g1": self.mano_g1,
            "mano_g2": self.mano_g2,
            "carta1_in_tavola": self.carta1_in_tavola,
            "carta2_in_tavola": self.carta2_in_tavola,
            "briscole": self.briscola,
            "prio": self.prio,
            "carte_rimaste_mazzo": len(self.mazzo),
            "punti_g1": self.punti_g1,
            "punti_g2": self.punti_g2,
            "fase": self.fase
        } 
                    
                 
            
        
