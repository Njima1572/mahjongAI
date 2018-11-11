#Get Tehai from hai0, hai1, hai2, hai3
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

    def getTehais(self):
        hand = np.empty((4,34))
        discard = np.array(4)
        text = self.mjlog.read()
        #p1 = re.compile(r'hai\d="\d+"')
        #print(re.findall(r'hai\d="\d+"',text))
        print(re.findall(r'<T\d+',text))
        print(re.findall(r'hai\d+',text))


    def haiConverter(self, tile):
        tile.value = tile.value / 4
        return tile

def main():
    mj = MjlogToCSV("mjlogs/sample2.mjlog", "test.csv")
    mj.getTehais()


main()
