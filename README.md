
#### Modules being Used
numpy, pandas, sklearn, mahjong, requests
make sure to `python3 -m pip install numpy pandas sklearn mahjong requests` before running

#### Description
All the html files in `htmls` contains link to a game with Paifu
`webparser.py` iterates through all the html files in `htmls` to create `[gameid].txt` files
Those text files are the raw files for all the games

`Mjlogreader3.py` iterates through all the text files in `mjlog` and writes out csv files into `csvs`

As of now, `mjML.py` uses machines from sklearn to predict and uses Mean Squared Errors or Mean Absolute Errors to get score.
The score that it prints out is calculated as `1 - (score/6)`



`python3 Mjlogreader3.py` to make csv files from mjlogs

Run "webparser.py" to get datas from htmls
