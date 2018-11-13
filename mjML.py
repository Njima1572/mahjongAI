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
from sklearn.linear_model import Perceptron 
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import f1_score
#from sklearn.feature_extraction.text import CountVectorizer
#from sklearn.feature_extraction.text import TfidfTransformer
#from sklearn.pipeline import Pipeline
#from sklearn.model_selection import GridSearchCV 

from metrics import mjMetrics
 
#Metric tools
from sklearn.metrics import classification_report
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
#useful libs
import os
import pandas as pd
import numpy as np
from sklearn.externals import joblib



class mjMachineLearner:
    '''
    log:
    #should be a float number 0 < trian_ratio < 1
    #train_ratio = 0.7 -> sent to init
    #count = 0 -> sent to trainData param
    #directories = os.fsencode("./csvs/") -> sent to init
    #directory_length=  len(os.listdir(directories)) -> worked out in init
    #train_amount = int(directory_length * train_ratio) -> worked out in init
    #test_amount = directory_length - train_amount -> worked out in init
    '''
    #TODO: add default train ratio
    def __init__(self, learningMachine, train_ratio = 0.7, directories):
        self.learningMachine = learningMachine
        self.trainRatio = train_ratio
        self.directories = directories
        self.directory_length = len(os.listdir(directories))
        self.train_amount = int(directory_length * train_ratio)
        self.test_amount = directory_length - train_amount
        
    
    def trainData(self, count = 0):
        """
        trains a machineLearner with csv game files
        creates a joblib with the trained machine content
        """
        for directory in os.listdir(self.directories):
            
            if count > (self.train_amount):
                break
            
            dirname = self.directories + os.fsencode(directory + b"/")
            count += 1
        
            for file_ in os.listdir(dirname):
                if file_.endswith(b".csv"):
                    filename_str = (dirname + file_).decode('utf-8')
                    file = open(filename_str, "r", encoding = "utf-8")
                    file = file.read()
                    columns = [i for i in range(20 + 1)]
                    df = pd.read_csv(filename_str, delimiter=',', header= None, names = columns, engine = 'python', skipfooter = 1)
                    df = df.fillna(value=int(-1))
                    if(len(df) < 2):
                        continue
                    y_labels = df.iloc[:, 0]
                    if(len(np.unique(y_labels)) < 2):
                        continue
                    X_ = df.iloc[:, 1:]
                    
                    self.learningMachine.fit(X_, y_labels)
                    
        joblib.dump(self.learningMachine, "%s.joblib"%(str(self.learningMachine)), compress=True)
        print("%s trained, joblib created!")
        
    def testData(self, count = 0):
        '''
        loads the trainData joblib and currently utilizes f1_scores
        assumes data is in CSV format
        '''
        #TODO: add a metric attribute to the class.
        
        trainedMachine = joblib.load("%s.joblib"%(str(self.learningMachine)))
        f1_scores = []
        
        for i in range(self.test_amount):
        
            directory = os.listdir(self.directories)[self.train_amount + i]
            dirname = self.directories + os.fsencode(directory + b"/")
            count += 1
        
            for file_ in os.listdir(dirname):
                if file_.endswith(b".csv"):
                    filename_str = (dirname + file_).decode('utf-8')
                    file = open(filename_str, "r", encoding = "utf-8")
                    file = file.read()
                    columns = [i for i in range(20 + 1)]
                    df = pd.read_csv(filename_str, delimiter=',', header= None, names = columns, engine = 'python', skipfooter = 1)
                    df = df.fillna(value=int(-1))
                    if(len(df) < 2):
                        continue
                    y_labels = df.iloc[:, 0]
                    X_ = df.iloc[:, 1:]
                    prediction = self.learningMachine.predict(X_)
                    f1_scores.append(mean_absolute_error(y_labels, prediction))
                    print(f1_scores)
        
    def __main__():
        """
        currently creates a SVM mjML instance and passes in the local csvs directory
        to instantiate the machineLearner object to utilize the SVC model.
        """
        #TODO: add and test different SKLearn learning machines
        svm = SVC(kernel='rbf', gamma="auto")
        mjML = mhMachineLearner(svm, os.fsencode("./csvs/"))
        
"""
backlog (delete once working):
old train Data code:
for directory in os.listdir(directories):
    
    if count > (train_amount):
        break
    
    dirname = directories + os.fsencode(directory + b"/")
    count += 1

    for file_ in os.listdir(dirname):
        if file_.endswith(b".csv"):
            filename_str = (dirname + file_).decode('utf-8')
            file = open(filename_str, "r", encoding = "utf-8")
            file = file.read()
            columns = [i for i in range(20 + 1)]
            df = pd.read_csv(filename_str, delimiter=',', header= None, names = columns, engine = 'python', skipfooter = 1)
            df = df.fillna(value=int(-1))
            if(len(df) < 2):
                continue
            y_labels = df.iloc[:, 0]
            if(len(np.unique(y_labels)) < 2):
                continue
            X_ = df.iloc[:, 1:]
            
            svm.fit(X_, y_labels)
            
joblib.dump(svm, "SVM-rbf.joblib", compress=True)
"""
"""
old Test Data code:
svm = joblib.load("SVM-rbf.joblib")
f1_scores = []

for i in range(test_amount):

    directory = os.listdir(directories)[train_amount + i]
    dirname = directories + os.fsencode(directory + b"/")
    count += 1

    for file_ in os.listdir(dirname):
        if file_.endswith(b".csv"):
            filename_str = (dirname + file_).decode('utf-8')
            
            file = open(filename_str, "r", encoding = "utf-8")
            file = file.read()
            columns = [i for i in range(20 + 1)]
            df = pd.read_csv(filename_str, delimiter=',', header= None, names = columns, engine = 'python', skipfooter = 1)
            df = df.fillna(value=int(-1))
            if(len(df) < 2):
                continue
            y_labels = df.iloc[:, 0]
            X_ = df.iloc[:, 1:]
            prediction = svm.predict(X_)
            f1_scores.append(mean_absolute_error(y_labels, prediction))
            #print( "a file has been tested!")

print(f1_scores)
"""
            
      


