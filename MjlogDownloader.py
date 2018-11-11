from requests import get
from lxml import html
import urllib2
from bs4 import BeautifulSoup

tenhou_sc_raw = "http://tenhou.net/sc/raw/"
url = "http://tenhou.net/sc/raw/viewer.cgi?scc2018110500.html.gz&3147"

page = urllib2.urlopen("file://Dropbox/CC/Mahjong/AI/scc2018110502.html").read()
print(page)
