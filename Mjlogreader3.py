# Get Tehai from hai0, hai1, hai2, hai3
#Use T, U, V, W for Tsumos
#Use D, E, F, G for Dahai
#Keep track of hand and Shanten
#Stack up each Junme in specific format
#Junme, Tehai, Shanten, Sutehai

"""
@author - Kochi Nakajima

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
        self.shanten = Shanten()


    """
    Gets the positions for <INIT tag to keep track of games
    """
    def getInitTagPos(self, text):
        inits = []
        for val in (re.finditer("<INIT", text)):
            inits.append(val.span())
        return inits

    """
    Cleans hand and discards
    """
    def initializeRound(self):
        hand = np.zeros((4,34))
        discards = []

        return hand, discards

    """
    Get initial hand from given text
    """
    def retrieveHand(self, text):
        hands = np.zeros((4,34))
        for j in range(4):
            Hand = re.findall('hai' + str(j) + '="(.+?)"',text)
            Hand = [kyoku.split(",") for kyoku in Hand]
            Hand = [[self.haiConverter(int(tile)) for tile in kyoku] for kyoku in Hand]
            for k in range(len(Hand[0])):
                hands[j][int(Hand[0][k])] += 1
        return hands

    """
    Get tsumos of players from given text
    """
    def retrieveTsumo(self, text):
        tsumos = []
        tsumos.append([self.haiConverter(int(tile[2:])) for tile in re.findall(r'<T\d+',text)])
        tsumos.append([self.haiConverter(int(tile[2:])) for tile in re.findall(r'<U\d+',text)])
        tsumos.append([self.haiConverter(int(tile[2:])) for tile in re.findall(r'<V\d+',text)])
        tsumos.append([self.haiConverter(int(tile[2:])) for tile in re.findall(r'<W\d+',text)])
        return tsumos
    """
    Get discards of players from given text
    """
    def retrieveDiscards(self, text):
        discards = []
        discards.append([self.haiConverter(int(tile[2:])) for tile in re.findall(r'<D\d+',text)])
        discards.append([self.haiConverter(int(tile[2:])) for tile in re.findall(r'<E\d+',text)])
        discards.append([self.haiConverter(int(tile[2:])) for tile in re.findall(r'<F\d+',text)])
        discards.append([self.haiConverter(int(tile[2:])) for tile in re.findall(r'<G\d+',text)])
        return discards

    """
    Get text for a round_num round
    """
    def getRoundText(self, text, round_num, inits):
        if(round_num < len(inits) - 1):
            return text[inits[round_num][1]:inits[round_num+1][0]]
        else:
            return text[inits[round_num][1]:]
    """
    Writes info in a specific way into csv
    Shanten | Discards
    """
    def writeToCSV(self, hands, tsumos, discards, csvfile):
        for player in range(4):
            discard = []
            smaller = len(tsumos[player])
            if(len(discards[player]) < len(tsumos[player])):
                smaller = len(discards[player])
            for k in range(smaller):
                hands[player][tsumos[player][k]] += 1
                hands[player][discards[player][k]] -= 1
                discard.append(discards[player][k])
                target = self.shanten.calculate_shanten(hands[player])
                csvfile.write("%d"%target)
                for m in range(len(discard)):
                    csvfile.write(",%s"%(discard[m]))
                csvfile.write("\n")

    """
    Checks if the game is Three people mahjong or not
    """
    def sanmaCheck(self):
        if(re.search('n3=\"\"',self.text)):
            return True
    """
    converts the mjlog into CSV file with specific format under /csvs/
   Csv file that is less than 10 bytes will be deleted here
    """
    def convertToCSV(self, foldername):
        hand, discards = self.initializeRound()
        filename = "csvs/%s.csv"%(foldername)
        csvfile = open(filename,"w")
        inits = self.getInitTagPos(self.text)

        for i in range(len(inits)):
            discards = []
            text = self.getRoundText(self.text, i, inits)
            if(re.search('<N',text)):
                #print("Naki, Not going to consider")
                continue

            hands = self.retrieveHand(text)
            tsumos = self.retrieveTsumo(text)
            discards = self.retrieveDiscards(text)
            self.writeToCSV(hands, tsumos, discards, csvfile)
        csvfile.flush()
        csvfile.close()
        if(os.stat(filename).st_size < 10):
            os.remove(filename)
            print("Insignificant size, deleted")

    """
    Converts 136 into 34 tile types
    """
    def haiConverter(self, tile):
        tile = tile / 4
        return int(tile)

"""
Directory Tree
        . ------ mjlogs ----- [ids] - mj_data.txt
          |
          |
          ------ csvs ------ [ids] ------ [mj_data].csv
          |
          |
          ------ htmls ----- html


          directories = mjlogs
          directory = things in directories [ids]
          dirname = ./mjlogs/[ids]/
          file_ = things in dirname - mj_data.txt
          my_dir = "./csvs/[ids]/[mj_data]

"""
def main():
    directories = os.fsencode("./mjlogs/")
    for directory in os.listdir(directories):
#            if os.path.isdir(directory.decode('utf-8')):
        dirname = directories + os.fsencode(directory + b"/")
        mY_dir = "./csvs/" + directory.decode("utf-8")
        if not os.path.exists(mY_dir):
            os.mkdir(mY_dir)

        for file_ in os.listdir(dirname):
            if file_.endswith(b".txt"):
                my_dir = directory.decode("utf-8") + "/" + file_.decode('utf-8')[:-4]
                mj = MjlogToCSV((dirname + file_).decode('utf-8'))
                if not mj.sanmaCheck():
                    mj.convertToCSV(my_dir)
                print(file_.decode('utf-8') + " Done!")
        print("Dir " + directory.decode('utf-8')+" Done!")

main()
