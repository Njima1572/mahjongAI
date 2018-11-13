#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 14:38:20 2018

@author: isabelgtz
"""
import re
import numpy as np 
import requests
import os

## gets the url id from files 
def readFile (filename):
    try:
        my_file=open(filename, 'r')
    except IOError:
        print("File not found or path is incorrect")
    
    number_id = []
    for line in my_file: 
        id = re.search('2018(.+?)">', line)
        if id:
            number_id.append(id.group(1))
    print (number_id)
    return number_id
    



#builds the urls, accesses them and retrieves the data from them 
#creates data files for every url 
def writeFile (number_ids,foldername):   
    urls = []
    for i in range (np.size(number_ids)):
        new_html = 'http://tenhou.net/0/log/?2018' + number_ids[i]
        urls.append(new_html)
        data = requests.get(new_html)
        with open("mjlogs/%s/mj_data_%s.txt" %(foldername, i),'w') as out_f:
            out_f.write(data.text)
        print ( i+1,'File written')



directory = os.fsencode("./htmls/")
for file in os.listdir(directory):
    filename = directory + os.fsencode(file)
    if filename.endswith(b".html"):
        if not os.path.exists("./mjlogs/%s"%file.decode('utf-8')[:-5]):
            os.mkdir("./mjlogs/%s"%file.decode('utf-8')[:-5])

        writeFile(readFile(filename),file.decode('utf-8')[:-5])
