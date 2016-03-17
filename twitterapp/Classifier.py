# -*- coding: utf-8 -*-
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
import pickle


class Classifier:
    def __init__(self):
        self.train_data = []
        self.train_labels = []
        self.test_data = []   
        self.vectorizer = TfidfVectorizer(sublinear_tf=True, use_idf=True)
        self.classifier = SGDClassifier()

    #classifier
    def getClassifier(self):
        s = pickle.dumps(self.classifier)
        return s

    def setClassifier(self,classifier):
        self.classifier = pickle.loads(classifier)
        
    #train
    def addTrain(self,text,classes):
        self.train_data.append(text)
        self.train_labels.append(classes)

    def addTrainList(self,textList,classesList):
        self.train_data.extend(textList)
        self.train_labels.extend(classesList)

    def clearTrain(self):
        self.train_data = []
        self.train_labels = []

    def setTrain(self,text,classes):
        self.clearTrain()
        self.train_data.append(text)
        self.train_labels.append(classes)

    def setTrainList(self,textList,classesList):
        self.clearTrain()
        self.train_data.extend(textList)
        self.train_labels.extend(classesList)

    def vecTrain(self):
        self.train_vectors = self.vectorizer.fit_transform(self.train_data)

    def fit(self):
        self.classifier.fit(self.train_vectors, self.train_labels)

    def getVecTrain(self):
        return self.train_vectors

    def setVecTrain(self,train_vectors):
        self.train_vectors = train_vectors

    def vecFitTrain(self):
        self.vecTrain()
        self.fit()

    def getTrainLists(self):
        return self.train_data, self.train_labels

    def getTrainSet(self):
        TrainSet = []
        for i in range(len(self.train_data)):
            TrainSet.append({'text':self.train_data[i],'lable':self.train_labels[i]})
        return TrainSet
    

    #test    
    def addTest(self,text):
        self.test_data.append(text)

    def addTestList(self,text_list):
        self.test_data.extend(text_list)

    def clearTest(self):
        self.test_data = []

    def setTest(self,text):
        self.clearTest()
        self.test_data.append(text)

    def setTestList(self,text_list):
        self.clearTest()
        self.test_data = text_list
        
    def getTestList(self):
        return self.test_data
        
    def vecTest(self):
        self.test_vectors = self.vectorizer.transform(self.test_data)

    def getVecTest(self):
        return self.test_vectors

    def predict(self):
        self.prediction = self.classifier.predict(self.test_vectors)
        #print self.prediction
        return self.prediction

    def vecPredictTest(self):
        self.vecTest()
        return self.predict()
