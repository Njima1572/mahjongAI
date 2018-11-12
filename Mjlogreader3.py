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
import os
import re

# File to Open should be mjlog
# File to Write should be csv file
class MjlogToCSV:
    def __init__(self, file_to_open):
        self.file_to_open = file_to_open
        self.mjlog = open(self.file_to_open, "r")
        self.text = self.mjlog.read()

    def getTehais(self, foldername):
        hand = np.zeros((4,34))
        shanten = Shanten()
        discard = np.array(4)
        text = self.text
        
        if(re.search('n3=\"\"',text)):
            print("Sanma, Not going to Consider")
            return
        """
        #p1 = re.compile(r'hai\d="\d+"')
        for i in range(4):
            Hand = re.findall('hai' + str(i) + '="(.+?)"',text)
            Hand = [kyoku.split(",") for kyoku in Hand]
            Hand = [[self.haiConverter(int(tile)) for tile in kyoku] for kyoku in Hand]
            initialHands.append(Hand)
            """
        csvfile = open("csvs/%s.csv"%(foldername),"w")
        inits = []
        for val in (re.finditer("<INIT", text)):
            inits.append(val.span())

        for i in range(len(inits)):
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
                    hand[j][int(Hand[0][k])] += 1

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
                    discard.append(Discards[player][k])
                    target = shanten.calculate_shanten(hand[player])
                    csvfile.write("%d"%target)
                    for m in range(len(discard)):
                        csvfile.write(",%s"%(discard[m]))
                    csvfile.write("\n")
                discards.append(discard)
        csvfile.flush()
        csvfile.close()

    def haiConverter(self, tile):
        tile = tile / 4
        return int(tile)

"""
Directory Tree
        . ------ mjlogs ----- [ids] - mj_data.txt
          |         
          |
          ------ csvs ------ [ids] ------ [mj_data] ------ csv
          |
          |
          ------ htmls ----- html


          directories = mjlogs
          directory = things in directories [ids]
          dirname = ./mjlogs/[ids]/
          file_ = things in dirname - mj_data.txt
          my_dir = "./csvs/[ids]/[mj_data]

"""
def txtParser():
        directories = os.fsencode("./mjlogs/")
        for directory in os.listdir(directories):
#            if os.path.isdir(directory.decode('utf-8')):
            dirname = directories + os.fsencode(directory + b"/")
            mY_dir = "./csvs/" + directory.decode("utf-8")
            if not os.path.exists(mY_dir):
                os.mkdir(mY_dir)
                
            for file_ in os.listdir(dirname):
                if file_.endswith(b".txt"):
                    my_dir = directory.decode("utf-8") + "/" + file_.decode('utf-8')[:-5]
                    mj = MjlogToCSV((dirname + file_).decode('utf-8'))
                    mj.getTehais(my_dir)
                    print(file_.decode('utf-8') + " Done!")
            print("Dir " + directory.decode('utf-8')+" Done!")
def main():
    #mj = MjlogToCSV("mjlogs/scc2018110500/mj_data_0.txt") 
    #mj.getTehais(filename)
    txtParser()

main()
