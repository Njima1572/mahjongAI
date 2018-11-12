# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 11:24:56 2018

@author: p_giacominsanou
"""
 
#Learning machines:
#from sklearn.naive_bayes import MultinomialNB #For my own entretainment
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import SGDClassifier
from sklearn import svm 
from sklearn.linear_model import Perceptron 
from sklearn.linear_model import LogisticRegression
 
#from sklearn.feature_extraction.text import CountVectorizer
#from sklearn.feature_extraction.text import TfidfTransformer
#from sklearn.pipeline import Pipeline
#from sklearn.model_selection import GridSearchCV 
 
#Metric tools
from sklearn import metrics
from sklearn.metrics import classification_report

#useful libs
import os
import pandas as pd
import numpy as np

#def txtParser():
#        directories = os.fsencode("./csvs/")
#        for directory in os.listdir(directories):
##            if os.path.isdir(directory.decode('utf-8')):
#            dirname = directories + os.fsencode(directory + b"/")
#            mY_dir = "./csvs/" + directory.decode("utf-8")
#            if not os.path.exists(mY_dir):
#                os.mkdir(mY_dir)
#                
#            for file_ in os.listdir(dirname):
#                if file_.endswith(b".txt"):
#                    my_dir = directory.decode("utf-8") + "/" + file_.decode('utf-8')[:-4]
#                    mj = MjlogToCSV((dirname + file_).decode('utf-8'))
#                    mj.getTehais(my_dir)
#                    print(file_.decode('utf-8') + " Done!")
#            print("Dir " + directory.decode('utf-8')+" Done!")
        

file = open("./csvs/scc2018110500/mj_data_0.csv", "r", encoding = "utf-8")
file = file.read()
number_of_col= int(file[-2:])
columns = [i for i in range(number_of_col + 1)]
df = pd.read_csv("./csvs/scc2018110500/mj_data_0.csv", delimiter=',', header= None, names = columns, engine = 'python', skipfooter = 1)
print(df.head())

