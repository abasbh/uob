# -*- coding: utf-8 -*-
from .Classifier import *
from .Preprocess import *
import pymongo 
from pymongo import MongoClient

client = MongoClient()
db = client.twitterdb
collection = db.stream
collection2 = db.label

class tools:
    def __init__(self):
        self.text = []
        self.sent = []
        self.main = []
        self.subt = []
        self.loadSets()
        self.text_pre = []
        self.pre = Preprocess()
        self.preP()
        self.cSent = Classifier()
        self.cMain = Classifier()
        self.cSubt = Classifier()
        self.setC()
                
        
    def loadSets(self):
        query = collection2.find()
        for i in query:
            q = collection.find({'data.id_str': i['id'] })
            for j in q:
                self.text.append(j['data']['text'])
                self.sent.append(i['sent'])
                self.main.append(i['main'])
                self.subt.append(i['subt'])

    
    def preP(self):
        self.text_pre = self.pre.analysisList(self.text)

    def setC(self):
        self.cSent.addTrainList(self.text_pre,self.sent)
        self.cMain.addTrainList(self.text_pre,self.main)
        self.cSent.vecFitTrain()
        self.cMain.vecFitTrain()

    def setCSubt(self,pMain):
        self.cSubt.clearTrain()
        for i in range(len(self.main)):
            if self.main[i] == pMain:
                self.cSubt.addTrain(self.text_pre[i],self.subt[i])
        self.cSubt.vecFitTrain()

    def preText(self,text):
        self.cSent.setTest(text)
        self.cMain.setTest(text)
        self.pSent = self.cSent.vecPredictTest()
        self.pMain = self.cMain.vecPredictTest()
        self.setCSubt(self.pMain[0])
        self.cSubt.setTest(text)
        self.pSubt = self.cSubt.vecPredictTest()
        return self.pSent[0], self.pMain[0], self.pSubt[0]
        
        

    
        

        
        

    
