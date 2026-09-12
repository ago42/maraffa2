def ordi(l):
    l.sort()
    diz={}
    for x in l:
        s=x.split(" ")
        if s[1]=="Asso":
            diz.update({x:8})
        elif s[1]=="2":
            diz.update({x:9})
        elif s[1]=="3":
            diz.update({x:10})
        elif s[1]=="4":
            diz.update({x:1})
        elif s[1]=="5":
            diz.update({x:2})
        elif s[1]=="6":
            diz.update({x:3})
        elif s[1]=="7":
            diz.update({x:4})
        elif s[1]=="Fante":
            diz.update({x:5})
        elif s[1]=="Cavallo":
            diz.update({x:6})
        elif s[1]=="Re":
            diz.update({x:7})
    return diz
def conta(l):
    somma=0
    for x in l:
        if x=='4' or x=='5' or x=='6' or x=='7':
            somma=somma
        elif x=="Asso":
            somma=somma+3
        else:
            somma=somma+1
    return somma/3
import random
stop=0
sommatot1=0
sommatot2=0
while(stop!=1):
    turni=0
    mano_g1=[]
    mano_g2=[]
    q=0
    punti1=[]
    punti2=[]
    carte=["Denari Asso", "Denari 2", "Denari 3", "Denari 4", "Denari 5", "Denari 6", "Denari 7", "Denari Fante", "Denari Cavallo", "Denari Re", "Coppe Asso", "Coppe 2", "Coppe 3", "Coppe 4", "Coppe 5", "Coppe 6", "Coppe 7", "Coppe Fante", "Coppe Cavallo", "Coppe Re", "Spade Asso", "Spade 2", "Spade 3", "Spade 4", "Spade 5", "Spade 6", "Spade 7", "Spade Fante", "Spade Cavallo", "Spade Re", "Bastoni Asso", "Bastoni 2", "Bastoni 3", "Bastoni 4", "Bastoni 5", "Bastoni 6", "Bastoni 7", "Bastoni Fante", "Bastoni Cavallo", "Bastoni Re"]
    for a in range (0,10,1):
        x=random.randint(0,39-q)
        mano_g1.append(carte[x])
        carte.pop(x)
        q=q+1
    for a in range (0,10,1):
        x=random.randint(0,39-q)
        mano_g2.append(carte[x])
        carte.pop(x)
        q=q+1
    ordg1=ordi(mano_g1)
    ordg2=ordi(mano_g2)
    print(mano_g1)
    print(mano_g2)
    if turni%2==0:
        briscole=input("Giocatore 1 scegli le briscole")
    else:
         briscole=input("Giocatore 2 scegli le briscole")
    prio=1
    for x in range(0,10,1):
        if prio==1:
            carta1=input("giocatore 1 cosa butti")
            carta2=input("giocatore 2 cosa rispondi")
            mano_g1.remove(carta1)
            mano_g2.remove(carta2)
            ordg1.remove(carta1)
            ordg2.remove(carta2)
            carta1s=carta1.split(" ")
            carta2s=carta2.split(" ")
            if carta1s[0]==carta2s[0]:
                if ordg1[carta1]>ordg2[carta2]:
                    punti1.append(carta1s[1])
                    punti1.append(carta2s[1])
                    prio=1
                elif ordg1[carta1]<ordg2[carta2]:
                    punti2.append(carta1s[1])
                    punti2.append(carta2s[1])
                    prio=2
            elif carta2s[0]==briscole:
                punti2.append(carta1s[1])
                punti2.append(carta2s[1])
                prio=2
            else:
                punti1.append(carta1s[1])
                punti1.append(carta2s[1])
                prio=1
        else:
            carta2=input("giocatore 2 cosa butti")
            carta1=input("giocatore 1 cosa rispondi")
            mano_g1.remove(carta1)
            mano_g2.remove(carta2)
            ordg1.remove(carta1)
            ordg2.remove(carta2)
            carta1s=carta1.split(" ")
            carta2s=carta2.split(" ")
            if carta2s[0]==carta1s[0]:
                if ordg2[carta2]>ordg1[carta1]:
                    punti2.append(carta2s[1])
                    punti2.append(carta1s[1])
                    prio=2
                elif ordg2[carta2]<ordg1[carta1]:
                    punti1.append(carta1s[1])
                    punti1.append(carta2s[1])
                    prio=1
            elif carta1s[0]==briscole:
                punti1.append(carta1s[1])
                punti1.append(carta2s[1])
                prio=1
            else:
                punti2.append(carta1s[1])
                punti2.append(carta2s[1])
                prio=2
        x=random.randint(0,39-q)
        mano_g1.append(carte[x])
        q=q+1
        carte.pop(x)
        x=random.randint(0,39-q)
        mano_g2.append(carte[x])
        q=q+1
        carte.pop(x)
        ordg1=ordi(mano_g1)
        ordg2=ordi(mano_g2)
    if prio==1:
        somma1=conta(punti1)+1
        somma2=conta(punti2)
    else:
        somma2=conta(punti2)+1
        somma1=conta(punti1)
    sommatot1=sommatot1+somma1
    sommatot2=sommatot2+somma2
    turni=turni+1
    
        
                
                
                    
                 
            
        
