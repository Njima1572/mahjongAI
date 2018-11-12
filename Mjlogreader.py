# Get Tehai from hai0, hai1, hai2, hai3
#Use T, U, V, W for Tsumos
#Use D, E, F, G for Dahai
#Keep track of hand and Shanten
#Stack up each Junme in specific format
#Junme, Tehai, Shanten, Sutehai

"""
0 ~ 8 Manzu
9 ~ 17 Pinzu
18 ~ 26 Souzu
27 ~ 30 Directions E, S, W, N
31 ~ 33 Dragons W, G, R

In mjlog,
0 ~ 35 Manzu
36 ~ 71 Souzu
72 ~ 107 Souzu
108 ~ 123 Directions
124 ~ 135 Dragons

Format:
Haipai:
hai0 = "[[Hais]]"

Tsumos:
<T[Hai]/>
<U[Hai]/>
<V[Hai]/>
<W[Hai]/>

Discards:
<D[Hai]/>
<E[Hai]/>
<F[Hai]/>
<G[Hai]/>
"""
from mahjong.shanten import Shanten
import numpy as np
import re
# File to Open should be mjlog
# File to Write should be csv file
class MjlogToCSV:
    def __init__(self, file_to_open, file_to_write):
        self.file_to_open = file_to_open
        self.file_to_write = file_to_write
        self.mjlog = open(self.file_to_open, "r")
        self.csv = open(self.file_to_write, "w")
        self.text = self.mjlog.read()

    def getTehais(self):
        hand = np.zeros((4,34))
        shanten = Shanten()
        discard = np.array(4)
        text = self.text
        #p1 = re.compile(r'hai\d="\d+"')
        initialHands = []
        """for i in range(4):
            Hand = re.findall('hai' + str(i) + '="(.+?)"',text)
            Hand = [kyoku.split(",") for kyoku in Hand]
            Hand = [[self.haiConverter(int(tile)) for tile in kyoku] for kyoku in Hand]
            initialHands.append(Hand)
            """
        inits = []
        for val in (re.finditer("<INIT", text)):
            inits.append(val.span())

        for i in range(len(inits)):
            csvfile = open("csvs/data%d.csv"%(i),"w")
            hand = np.zeros((4,34))
            discards = []
            if(i < len(inits) -1):
                text = self.text[inits[i][1]:inits[i+1][0]]
            else:
                text = self.text[inits[i][1]:]
            for j in range(4):
                Hand = re.findall('hai' + str(j) + '="(.+?)"',text)
                Hand = [kyoku.split(",") for kyoku in Hand]
                Hand = [[self.haiConverter(int(tile)) for tile in kyoku] for kyoku in Hand]
                for k in range(len(Hand[0])):
                    hand[j][Hand[0][k]] += 1

            p1Tsumo = [self.haiConverter(int(tile[2:])) for tile in re.findall(r'<T\d+',text)]
            p2Tsumo = [self.haiConverter(int(tile[2:])) for tile in re.findall(r'<U\d+',text)]
            p3Tsumo = [self.haiConverter(int(tile[2:])) for tile in re.findall(r'<V\d+',text)]
            p4Tsumo = [self.haiConverter(int(tile[2:])) for tile in re.findall(r'<W\d+',text)]
            p1Discards = [self.haiConverter(int(tile[2:])) for tile in re.findall(r'<D\d+',text)]
            p2Discards = [self.haiConverter(int(tile[2:])) for tile in re.findall(r'<E\d+',text)]
            p3Discards = [self.haiConverter(int(tile[2:])) for tile in re.findall(r'<F\d+',text)]
            p4Discards = [self.haiConverter(int(tile[2:])) for tile in re.findall(r'<G\d+',text)]
            Tsumos = [p1Tsumo, p2Tsumo, p3Tsumo, p4Tsumo]
            Discards = [p1Discards, p2Discards, p3Discards, p4Discards]

            for player in range(4):
                discard = []
                smaller = len(Tsumos[player])
                if(len(Discards[player]) < len(Tsumos[player])):
                    smaller = len(Discards[player])
                for k in range(smaller):
                    hand[player][Tsumos[player][k]] += 1
                    hand[player][Discards[player][k]] -= 1
                    print(hand)
                    discard.append(Discards[player][k])
                    target = shanten.calculate_shanten(hand[player])
                discards.append(discard)


    def haiConverter(self, tile):
        tile = tile / 4
        return tile

def main():
    mj = MjlogToCSV("mjlogs/sample2.mjlog", "test.csv")
    mj.getTehais()


main()
