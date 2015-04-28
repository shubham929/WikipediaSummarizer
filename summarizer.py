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

wordDocFrq = {}
with open('data_wiki_docFrq.json') as data_file:    
    wordDocFrq = json.load(data_file)



wordDocFrq = wordDocFrq['docFrq']
class Summarizer:
    
    def __init__(self, title):
        self.article = getJSON(title)
        self.title = self.article['title']
        try:
            from google.google import resultCount
        except Exception as e:
            raise NameError(type(e).__name__)
            self.titleImp = 1000
        self.titleImp = resultCount(title)
        self.sections = []
        self.positiveKeywords = ["cricket"]
        self.negativeKeywords = ["family"]
        for section in self.article['sections']:
            self.sections.append(Section(section))
        self.threshold = 0        

    def summarize(self):
        
        for section in self.sections:
            self.sentencePosition(section)
            self.sectionImportance(section)
            self.tfIDF(section)
            self.positiveNess(section)
            self.negativeNess(section)
        
        self.calculateScore()
        
    def sentencePosition(self, section):
        nSen = section.nSen
        pos = 1
        for sen in section.sentences:
            sen.pos = float(nSen+1-pos)/nSen
            pos += 1
        
    def sectionImportance(self, section):
        try:
            from google.google import resultCount
        except Exception as e:
            raise NameError(type(e).__name__)
            
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
            for pos in self.positiveKeywords:
                section.positiveScore = max(section.positiveScore,
                                            self.word_path_similarity(key, pos) + 1)

        for sentence in section.sentences:
            sentence.positiveScore = 1
            for word in sentence.words:
                for pos in self.positiveKeywords:
                    sentence.positiveScore = max(sentence.positiveScore, 
                                            self.word_path_similarity(pos, word) + 1)


    def negativeNess(self, section):
        sectionKey = section.heading.split(" ")
        for key in sectionKey:
            for neg in self.negativeKeywords:
                section.negativeScore = min(section.negativeScore,
                                            1 - self.word_path_similarity(key, neg))

        for sentence in section.sentences:
            sentence.negativeScore = 1
            for word in sentence.words:
                for neg in self.negativeKeywords:
                    sentence.negativeScore = min(sentence.negativeScore,
                                            1 - self.word_path_similarity(neg, word))

    
    def word_path_similarity(self, s1, s2):
        val = 0
        if(s1.lower == s2.lower):
            return 1.0
        
        ss1 = wn.synsets(s1.lower())
        ss2 = wn.synsets(s2.lower())
        for t1 in ss1:
            for t2 in ss2:
                val = max(wn.path_similarity(t1, t2), val)

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
                print tfidf,
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


