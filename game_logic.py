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
    if x == "4" or x == "5" or x == "6" or x == "7":
      somma = somma
    elif x == "Asso":
      somma = somma + 3
    else:
      somma = somma + 1
  return somma / 3


class PartitaBriscola:

  def __init__(self):
    self.giocatori_connessi = 0
    self.turni = 0
    self.sommatot1 = 0
    self.sommatot2 = 0
    self.reset_partita()

  def reset_partita(self):
    self.mano_g1 = []
    self.mano_g2 = []
    self.punti1 = []
    self.punti2 = []
    self.q = 0

    self.carte = [
        "Denari Asso",
        "Denari 2",
        "Denari 3",
        "Denari 4",
        "Denari 5",
        "Denari 6",
        "Denari 7",
        "Denari Fante",
        "Denari Cavallo",
        "Denari Re",
        "Coppe Asso",
        "Coppe 2",
        "Coppe 3",
        "Coppe 4",
        "Coppe 5",
        "Coppe 6",
        "Coppe 7",
        "Coppe Fante",
        "Coppe Cavallo",
        "Coppe Re",
        "Spade Asso",
        "Spade 2",
        "Spade 3",
        "Spade 4",
        "Spade 5",
        "Spade 6",
        "Spade 7",
        "Spade Fante",
        "Spade Cavallo",
        "Spade Re",
        "Bastoni Asso",
        "Bastoni 2",
        "Bastoni 3",
        "Bastoni 4",
        "Bastoni 5",
        "Bastoni 6",
        "Bastoni 7",
        "Bastoni Fante",
        "Bastoni Cavallo",
        "Bastoni Re",
    ]

    # Distribuzione iniziale (10 carte a testa come nel tuo codice)
    for a in range(0, 10):
      x = random.randint(0, 39 - self.q)
      self.mano_g1.append(self.carte[x])
      self.carte.pop(x)
      self.q += 1

    for a in range(0, 10):
      x = random.randint(0, 39 - self.q)
      self.mano_g2.append(self.carte[x])
      self.carte.pop(x)
      self.q += 1

    self.ordg1 = ordi(self.mano_g1)
    self.ordg2 = ordi(self.mano_g2)

    self.briscole = None
    self.prio = 1
    self.carta1_in_tavola = None
    self.carta2_in_tavola = None
    self.fase = "IN_CORSO"

  def imposta_briscola(self, seme):
      self.briscole = seme
      # Chi deve scegliere la briscola (G1 nei turni pari, G2 nei dispari) gioca anche per primo
      chi_ha_scelto = 1 if (self.turni % 2 == 0) else 2
      self.prio = chi_ha_scelto
  def gioca_carta_singola(self, num_giocatore, carta):
    if self.fase == "FINITA":
      return

    # Registra la giocata dal rispettivo schermo
    if num_giocatore == 1 and not self.carta1_in_tavola:
      if carta in self.mano_g1:
        self.carta1_in_tavola = carta
    elif num_giocatore == 2 and not self.carta2_in_tavola:
      if carta in self.mano_g2:
        self.carta2_in_tavola = carta

    # Quando entrambi hanno tirato, risolve la mano con la tua logica esatta
    if self.carta1_in_tavola and self.carta2_in_tavola:
      self.risolvi_turno()

  def risolvi_turno(self):
    carta1 = self.carta1_in_tavola
    carta2 = self.carta2_in_tavola

    self.mano_g1.remove(carta1)
    self.mano_g2.remove(carta2)
    if carta1 in self.ordg1:
      del self.ordg1[carta1]
    if carta2 in self.ordg2:
      del self.ordg2[carta2]

    carta1s = carta1.split(" ")
    carta2s = carta2.split(" ")

    if self.prio == 1:
      if carta1s[0] == carta2s[0]:
        if self.ordg1[carta1] > self.ordg2[carta2]:
          self.punti1.append(carta1s[1])
          self.punti1.append(carta2s[1])
          self.prio = 1
        elif self.ordg1[carta1] < self.ordg2[carta2]:
          self.punti2.append(carta1s[1])
          self.punti2.append(carta2s[1])
          self.prio = 2
      elif carta2s[0] == self.briscole:
        self.punti2.append(carta1s[1])
        self.punti2.append(carta2s[1])
        self.prio = 2
      else:
        self.punti1.append(carta1s[1])
        self.punti1.append(carta2s[1])
        self.prio = 1
    else:
      if carta2s[0] == carta1s[0]:
        if self.ordg2[carta2] > self.ordg1[carta1]:
          self.punti2.append(carta2s[1])
          self.punti2.append(carta1s[1])
          self.prio = 2
        elif self.ordg2[carta2] < self.ordg1[carta1]:
          self.punti1.append(carta1s[1])
          self.punti1.append(carta2s[1])
          self.prio = 1
      elif carta1s[0] == self.briscole:
        self.punti1.append(carta1s[1])
        self.punti1.append(carta2s[1])
        self.prio = 1
      else:
        self.punti2.append(carta1s[1])
        self.punti2.append(carta2s[1])
        self.prio = 2

    # Pesca nuova carta se ce ne sono ancora
    if len(self.carte) >= 2:
      x = random.randint(0, 39 - self.q)
      self.mano_g1.append(self.carte[x])
      self.q += 1
      self.carte.pop(x)

      x = random.randint(0, 39 - self.q)
      self.mano_g2.append(self.carte[x])
      self.q += 1
      self.carte.pop(x)

      self.ordg1 = ordi(self.mano_g1)
      self.ordg2 = ordi(self.mano_g2)

    self.carta1_in_tavola = None
    self.carta2_in_tavola = None

    # Fine mano: calcola i punti esattamente con la tua funzione conta()
    if not self.mano_g1 and not self.mano_g2:
      if self.prio == 1:
        somma1 = conta(self.punti1) + 1
        somma2 = conta(self.punti2)
      else:
        somma2 = conta(self.punti2) + 1
        somma1 = conta(self.punti1)

      self.sommatot1 += somma1
      self.sommatot2 += somma2
      self.turni += 1
      self.fase = "FINITA"

  def to_dict(self):
    return {
        "mano_g1": self.mano_g1,
        "mano_g2": self.mano_g2,
        "carta1_in_tavola": self.carta1_in_tavola,
        "carta2_in_tavola": self.carta2_in_tavola,
        "briscole": self.briscole,
        "prio": self.prio,
        "carte_rimaste_mazzo": len(self.carte),
        "punti_g1": conta(self.punti1),
        "punti_g2": conta(self.punti2),
        "sommatot1": self.sommatot1,
        "sommatot2": self.sommatot2,
        "fase": self.fase,
    }
                    
                 
            
        
