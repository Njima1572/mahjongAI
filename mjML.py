# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 11:24:56 2018

@author: p_giacominsanou, k_nakajima, i_gutierrez
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
from sklearn.ensemble import RandomForestClassifier
#from sklearn.feature_extraction.text import CountVectorizer
#from sklearn.feature_extraction.text import TfidfTransformer
#from sklearn.pipeline import Pipeline
#from sklearn.model_selection import GridSearchCV 

from metrics import mjMetrics
import imp 
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
    def __init__(self, learningMachine, directories, metrics="MSE" ,train_ratio = 0.7):
        self.learningMachine = learningMachine
        self.train_ratio = train_ratio
        self.directories = directories
        self.metrics = metrics
        self.directory_length = len(os.listdir(self.directories))
        self.train_amount = int(self.directory_length * self.train_ratio)
        self.test_amount = self.directory_length - self.train_amount
        
    
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
                    endindex = str(self.learningMachine).find('(')
        joblib.dump(self.learningMachine, "%s.joblib"%(str(self.learningMachine)[:endindex]), compress=True)
        print("%s trained, joblib created!"%str(self.learningMachine)[:endindex])
        
    def getScore(self, y_labels, prediction):
        if(self.metrics == "micro"):
            return f1_score(y_labels,prediction, average="micro")
        elif(self.metrics == "macro"):
            return f1_score(y_labels,prediction, average="macro")
        elif(self.metrics == "mj"):
            return mjMetrics(y_labels,prediction)
        elif(self.metrics == "MAE"):
            return 1 - mean_absolute_error(y_labels,prediction)/6
        elif(self.metrics == "MSE"):
            return 1 - mean_squared_error(y_labels, prediction)/6
        else:
            return 1 - mean_absolute_error(y_labels,prediction)/6

    def testData(self, count = 0):
        '''
        loads the trainData joblib and currently utilizes f1_scores
        assumes data is in CSV format
        '''
        #TODO: add a metric attribute to the class, f1_score isn't accurate rn
        endindex = str(self.learningMachine).find('(')
        
        trainedMachine = joblib.load("%s.joblib"%(str(self.learningMachine)[:endindex]))
        scores = []
        
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
                    prediction = trainedMachine.predict(X_)
                    scores.append(self.getScore(y_labels, prediction))
        return scores 
def main():
    """
    currently creates a SVM mjML instance and passes in the local csvs directory
    to instantiate the machineLearner object to utilize the SVC model.
    """
    #TODO: add and test different SKLearn learning machines when learning model is finalized
#Logistic Regression didn't converge
    Machines_ = [SVC(kernel="rbf", gamma="auto"), Perceptron(max_iter=1000), SGDClassifier(learning_rate="adaptive", eta0=0.5, max_iter=1000), RandomForestClassifier(n_estimators=10)]
    for machine in Machines_:
        machinename = str(machine)[:str(machine).find("(")]
        mjML = mjMachineLearner(machine, os.fsencode("./csvs/"), metrics="MAE")
        mjML2 = mjMachineLearner(machine, os.fsencode("./csvs/"), metrics="MSE")
        mjML.trainData()
        mjML2.trainData()
        
        scores = mjML.testData()
        scores2 = mjML2.testData()
        print("The average score with %s for %s is : %.5f"%(mjML.metrics, machinename, np.average(scores)))
        print("The average score with %s for %s is : %.5f"%(mjML2.metrics, machinename, np.average(scores2)))
if __name__=="__main__":
    main()

        
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
            joblib.dump(svm, "SVM-rbf.joblib", compress=True) """
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
            
      


