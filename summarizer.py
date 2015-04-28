from extractor import getJSON
from section import Section
from sentence import Sentence
from stemming.porter2 import stem
import re
import nltk.data
import json
from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet as st
from time import time
import threading
from search import resultCount
from stopwords import isStopWord


wordDocFrq = {}
with open('data_wiki_docFrq.json') as data_file:    
    wordDocFrq = json.load(data_file)



wordDocFrq = wordDocFrq['docFrq']
class Summarizer:
    
    def __init__(self, title):
        self.lock = threading.Lock()
        self.article = getJSON(title)
        self.title = self.article['title']
        self.titleImp = resultCount(title)
        self.sections = []
        self.positiveKeywords = ["cricket"]
        self.negativeKeywords = ["family"]
        for section in self.article['sections']:
            self.sections.append(Section(section))
        self.threshold = 0
        self.word_path_similarity("cat", "bat")

    def summarize(self):
        
        threadList = []
        i = 1
        for section in self.sections:
            
            t1 = threading.Thread(target = self.sentencePosition,
                                  kwargs = {'section': section})
            t1.start()

            t2 = threading.Thread(target = self.tfIDF, 
                                  kwargs = {'section': section})
            t2.start()

            t3 = threading.Thread(target = self.positiveNess, 
                                  kwargs = {'section': section})
            t3.start()

            t4 = threading.Thread(target = self.negativeNess,
                                  kwargs = {'section': section})
            t4.start()

            t5 = threading.Thread(target = self.sectionImportance,
                                  kwargs = {'section': section})
            t5.start()

            threadList.extend((t1, t2, t3, t4, t5))
            i += 2
        
            
        for thread in threadList:
            thread.join()
            
        print "cat"
        self.calculateScore()
        
    def sentencePosition(self, section):
        nSen = section.nSen
        pos = 1
        for sen in section.sentences:
            sen.pos = float(nSen+1-pos)/nSen
            pos += 1
        
    def sectionImportance(self, section):

        count = resultCount(self.title + " " + section.heading)
        section.importance = float(count)/self.titleImp
        for sen in section.sentences:
            sen.imp = section.importance

    def tfIDF(self, section):
        for sentence in section.sentences:
            val = 0
            for word in sentence.words:
                word = word.lower()
                word = stem(word)
                if word in wordDocFrq:
                    val += 1.0/wordDocFrq[word]
                else:
                    val += 2
            val /= sentence.length
            sentence.tfidf = val

    
    def positiveNess(self, section):

        sectionKey = section.heading.split(" ")
        section.positiveScore = 1
        for key in sectionKey:
            key = key.lower()
            if isStopWord(key):
                continue
            for pos in self.positiveKeywords:
                pos = pos.lower()
                if isStopWord(pos):
                    continue
                section.positiveScore = max(section.positiveScore,
                                            self.word_path_similarity(key, pos) + 1)
        for sentence in section.sentences:
            sentence.positiveScore = 1
            for word in sentence.words:
                word = word.lower()
                if isStopWord(word):
                    continue
                for pos in self.positiveKeywords:
                    pos = pos.lower()
                    if isStopWord(pos):
                        continue
                    sentence.positiveScore = max(sentence.positiveScore, 
                                            self.word_path_similarity(pos, word) + 1)

    def negativeNess(self, section):

        sectionKey = section.heading.split(" ")
        for key in sectionKey:
            key = key.lower()
            if isStopWord(key):
                continue
            for neg in self.negativeKeywords:
                neg = neg.lower()
                if isStopWord(neg):
                    continue
                section.negativeScore = min(section.negativeScore,
                                            1 - self.word_path_similarity(key, neg))

        for sentence in section.sentences:
            sentence.negativeScore = 1
            for word in sentence.words:
                word = word.lower()
                if isStopWord(word):
                    continue
                for neg in self.negativeKeywords:
                    neg = neg.lower()
                    if isStopWord(neg):
                        continue
                    sentence.negativeScore = min(sentence.negativeScore,
                                            1 - self.word_path_similarity(neg, word))

    
    def word_path_similarity(self, s1, s2):
        self.lock.acquire()
        val = 0
        if(s1.lower == s2.lower):
            return 1.0
        
        ss1 = wn.synsets(s1.lower())
        ss2 = wn.synsets(s2.lower())
        for t1 in ss1:
            for t2 in ss2:
                val = max(wn.path_similarity(t1, t2), val)
        self.lock.release()
        return val


    def calculateScore(self):
        for section in self.sections:
            for sentence in section.sentences:
                sentence.score = sentence.tfidf
                sentence.score *= sentence.pos
                sentence.score *= sentence.imp
                sentence.score *= sentence.positiveScore
                sentence.score *= sentence.negativeScore
                sentence.score *= section.positiveScore
                sentence.score *= section.negativeScore


    def printScore(self):
        for section in self.sections:
            for sentence in section.sentences:
                score = 1
                print sentence.sentence,
                print sentence.tfidf,
                print sentence.pos
                print sentence.imp
                print sentence.positiveScore
                print sentence.negativeScore
                print section.positiveScore
                print section.negativeScore
                print sentence.score



    def printSummary(self):
        values = []
        for section in self.sections:
            for sentence in section.sentences:
                values.append(sentence.tfidf*sentence.pos*sentence.imp)
        
        length = len(values)
        values = sorted(values)
        self.threshold = values[(4*length)/5]
        
        for section in self.sections:
            for sentence in section.sentences:
                if sentence.tfidf*sentence.pos*sentence.imp > self.threshold:
                    print sentence.sentence,

    def summary(self):
        values = []
        out = ""
        for section in self.sections:
            for sentence in section.sentences:
                values.append(sentence.tfidf*sentence.pos*sentence.imp)
        
        length = len(values)
        values = sorted(values)
        self.threshold = values[(80*len(values))/100]
        
        for section in self.sections:
            for sentence in section.sentences:
                if sentence.tfidf*sentence.pos*sentence.imp > self.threshold:
                    out += " " + sentence.sentence
        return out
        
    def test(self):
        print self.sections[0].sentences[0].sentence



def summary(url):
    s=Summarizer(url)
    s.summarize()
    s.printScore()


s = "en.wikipedia.org/wiki/Sachin_Tendulkar"
summary(s)


