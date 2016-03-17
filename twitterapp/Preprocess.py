# -*- coding: utf-8 -*-
from nltk.stem.isri import ISRIStemmer
from nltk import word_tokenize
import re
import os


class Preprocess:    
    def __init__(self):
        self.st = ISRIStemmer()
        self.getStopwords()
        self.getNegationwords()
        self.getSymbol()


       
    def analysis(self,line):
        line = self.enLine(line)
        line = self.tokenize(line)
        line = self.remSW(line)
        line = self.getTerms(line)
        line = self.remNE(line)
        line = self.removeNA(line)
        line = self.asLine(line)
        return line


    def analysisList(self,line_list):
        newList = list()
        for line in line_list:
            line = self.enLine(line)
            line = self.tokenize(line)
            line = self.remSW(line)
            line = self.getTerms(line)
            line = self.remNE(line)
            line = self.removeNA(line)
            line = self.asLine(line)
            newList.append(line)
        return newList
    
    def getStopwords(self):
        '''get stopwords from the stopwords file'''
        module_dir = os.path.dirname(__file__)  # get current directory
        file_path = os.path.join(module_dir, 'stopword.txt')
        f = open(file_path, 'r')
        stopwords = [line.rstrip() for line in f]
        sw = dict.fromkeys(stopwords)
        f.close()
        self.sw = [z.decode('utf-8') for z in sw]


    def getNegationwords(self):
        '''get negation words from the negation file'''
        module_dir = os.path.dirname(__file__)  # get current directory
        file_path = os.path.join(module_dir, 'negation.txt')
        f = open(file_path, 'r')
        newords = [line.rstrip() for line in f]
        ne = dict.fromkeys(newords)
        f.close()
        self.ne = [n.decode('utf-8') for n in ne]

    def getSymbol(self):
        '''get symbol from symbol file'''
        module_dir = os.path.dirname(__file__)  # get current directory
        file_path = os.path.join(module_dir, 'symbol.txt')
        f = open(file_path, 'r')
        sy = [line.rstrip() for line in f]
        ne = dict.fromkeys(sy)
        f.close()
        self.sy = [s.decode('utf-8') for s in sy]

        
    def enLine(self,line):
        ''' convert line to unicode '''
        try:
            line = line.decode('utf-8')
            self.log_msg = "string is not UTF-8, length %d bytes" % len(line)
        except UnicodeError:
            self.log_msg = "string is UTF-8"

        for s in self.sy:
            try:
                s = s.decode('utf-8')
            except UnicodeError:
                log_msg = "string is UTF-8"
            line = line.replace(s, u' ' + s + u' ')
            
        #line = line.replace(u'.', u' . ')
        #line = line.replace(u'.', u' . ')
        return line

            
    def removeNA(self,token):
        '''remove non-Arabic'''
        #x = re.compile(ur'[\u064B-\u065F]+', re.UNICODE)
        #line = [x.sub('', word) for word in line]
        x = re.compile(ur'[^\u0621-\u064A|_]+[\u1F300-\u1F5FF\u1F600-\u1F64F\u1F680-\u1F6FF\u2600-\u26FF\u2700-\u27BF]+', re.UNICODE)
        token = [x.sub('', word) for word in token]
        x = re.compile(ur'[\u0023]+', re.UNICODE)
        token = [x.sub('', word) for word in token]

        token = [word for word in self.asLine(token).split()]
        return token


    def tokenize(self,line):
        if len(line) > 50000:
            n = len(line) / 50000
            l = list()
            for i in range(1,n):
                start = (i-1)*50000
                end = i * 50000
                l = l + word_tokenize(line[start:end])
            token = l
        else:
            token = word_tokenize(line)

        return token


    def remSW(self,token):
        token_clean = [x for x in token if x not in self.sw]
        return token_clean


    def remNE(self,token):
        for i in range(len(token)):
            if token[i] in self.ne:
                temp = token[i]
                for x in range(i+1,len(token)):
                    if token[x] in self.sy:
                        break
                    else:
                        token[x] = temp + '_' + token[x]
            
        token_clean = [x for x in token if x not in self.ne]
        token_clean = [x for x in token_clean if x not in self.sy]
        return token_clean


    def norma (self,word):
        if word[:2] == u'ال' :
            word = word[2:]
        #ألف 
        x = re.compile(ur'[\u0622|\u0623|\u0625]+', re.UNICODE)
        word = x.sub(ur'\u0627', word)
        #ياء + ألف مقصورة 
        x = re.compile(ur'[\u0649]+', re.UNICODE)
        word = x.sub(ur'\u064A', word)
        #تاء مربوطة + هاء
        x = re.compile(ur'[\u0629]+', re.UNICODE)
        word = x.sub(ur'\u0647', word)
        #تطويلة
        x = re.compile(ur'[\u0640]+', re.UNICODE)
        word = x.sub(ur'', word)
        return word


    def getTerms(self,token):     
        line = list()
        for i in range(len(token)):
            a = self.norma(token[i])
            a = self.st.stem(a)
            line.append(a)
        return line

    def asLine(self,token):
        return ' '.join(token)


