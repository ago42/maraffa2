import random

def ordi(l):
    l.sort()
    diz = {}
    for x in l:
        s = x.split(" ")
        if s[1] == "Asso":
            diz.update({x: 8})
        elif s[1] == "2":
            diz.update({x: 9})
        elif s[1] == "3":
            diz.update({x: 10})
        elif s[1] == "4":
            diz.update({x: 1})
        elif s[1] == "5":
            diz.update({x: 2})
        elif s[1] == "6":
            diz.update({x: 3})
        elif s[1] == "7":
            diz.update({x: 4})
        elif s[1] == "Fante":
            diz.update({x: 5})
        elif s[1] == "Cavallo":
            diz.update({x: 6})
        elif s[1] == "Re":
            diz.update({x: 7})
    return diz

def conta(l):
    somma = 0
    for x in l:
        if x in ['4', '5', '6', '7']:
            somma = somma
        elif x == "Asso":
            somma = somma + 3
        else:
            somma = somma + 1
    return somma / 3

class PartitaBriscola:
    def __init__(self):
        self.reset_partita()

    def reset_partita(self):
        self.carte = [
            "Denari Asso", "Denari 2", "Denari 3", "Denari 4", "Denari 5", "Denari 6", "Denari 7", "Denari Fante", "Denari Cavallo", "Denari Re",
            "Coppe Asso", "Coppe 2", "Coppe 3", "Coppe 4", "Coppe 5", "Coppe 6", "Coppe 7", "Coppe Fante", "Coppe Cavallo", "Coppe Re",
            "Spade Asso", "Spade 2", "Spade 3", "Spade 4", "Spade 5", "Spade 6", "Spade 7", "Spade Fante", "Spade Cavallo", "Spade Re",
            "Bastoni Asso", "Bastoni 2", "Bastoni 3", "Bastoni 4", "Bastoni 5", "Bastoni 6", "Bastoni 7", "Bastoni Fante", "Bastoni Cavallo", "Bastoni Re"
        ]
        self.mano_g1 = []
        self.mano_g2 = []
        self.punti1 = []
        self.punti2 = []
        self.briscole = None
        self.prio = 1
        self.turni = 0
        self.fase = "SCELTA_BRISCOLA"  # Può essere SCELTA_BRISCOLA, GIOCATA_G1, GIOCATA_G2, FINITA
        self.carta1_in_tavola = None
        self.carta2_in_tavola = None
        
        # Distribuzione iniziale (10 carte a testa)
        for _ in range(10):
            x = random.randint(0, len(self.carte) - 1)
            self.mano_g1.append(self.carte.pop(x))
            
        for _ in range(10):
            x = random.randint(0, len(self.carte) - 1)
            self.mano_g2.append(self.carte.pop(x))

        self.ordg1 = ordi(self.mano_g1)
        self.ordg2 = ordi(self.mano_g2)

    def imposta_briscola(self, seme_briscola):
        """Sostituisce input('Giocatore X scegli le briscole')"""
        self.briscole = seme_briscola
        self.fase = "GIOCATA_G1" if self.prio == 1 else "GIOCATA_G2"

    def gioca_turno(self, carta1, carta2):
        """Sostituisce i blocchi di input e la logica interna della mano"""
        # Rimozione dalle mani
        self.mano_g1.remove(carta1)
        self.mano_g2.remove(carta2)
        
        # Corretto il bug del dizionario (.pop al posto di .remove)
        if carta1 in self.ordg1: self.ordg1.pop(carta1)
        if carta2 in self.ordg2: self.ordg2.pop(carta2)

        carta1s = carta1.split(" ")
        carta2s = carta2.split(" ")

        # Calcolo priorità e punti
        if self.prio == 1:
            if carta1s[0] == carta2s[0]:
                if ordi([carta1])[carta1] > ordi([carta2])[carta2]:
                    self.punti1.extend([carta1s[1], carta2s[1]])
                    self.prio = 1
                else:
                    self.punti2.extend([carta1s[1], carta2s[1]])
                    self.prio = 2
            elif carta2s[0] == self.briscole:
                self.punti2.extend([carta1s[1], carta2s[1]])
                self.prio = 2
            else:
                self.punti1.extend([carta1s[1], carta2s[1]])
                self.prio = 1
        else:
            if carta2s[0] == carta1s[0]:
                if ordi([carta2])[carta2] > ordi([carta1])[carta1]:
                    self.punti2.extend([carta2s[1], carta1s[1]])
                    self.prio = 2
                else:
                    self.punti1.extend([carta1s[1], carta2s[1]])
                    self.prio = 1
            elif carta1s[0] == self.briscole:
                self.punti1.extend([carta1s[1], carta2s[1]])
                self.prio = 1
            else:
                self.punti2.extend([carta1s[1], carta2s[1]])
                self.prio = 2

        # Pesca nuove carte se il mazzo contiene ancora elementi
        if len(self.carte) >= 2:
            x = random.randint(0, len(self.carte) - 1)
            self.mano_g1.append(self.carte.pop(x))
            x = random.randint(0, len(self.carte) - 1)
            self.mano_g2.append(self.carte.pop(x))

        self.ordg1 = ordi(self.mano_g1)
        self.ordg2 = ordi(self.mano_g2)

        # Controlla se la partita è terminata
        if len(self.mano_g1) == 0 and len(self.mano_g2) == 0:
            self.fase = "FINITA"

    def calcola_punteggio_finale(self):
        """Esegue il calcolo finale dei punti mantenendo la tua formula originale"""
        if self.prio == 1:
            somma1 = conta(self.punti1) + 1
            somma2 = conta(self.punti2)
        else:
            somma2 = conta(self.punti2) + 1
            somma1 = conta(self.punti1)
        return somma1, somma2

    def to_dict(self):
        """Invia lo stato completo del gioco al frontend/Render in formato JSON"""
        return {
            "mano_g1": self.mano_g1,
            "mano_g2": self.mano_g2,
            "briscole": self.briscole,
            "prio": self.prio,
            "fase": self.fase,
            "carte_rimaste_mazzo": len(self.carte)
        }
        
                
                
                    
                 
            
        
