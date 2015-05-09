from extractor import getJSON
from section import Section
from sentence import Sentence
import json
from nltk.corpus import wordnet as wn
import threading
from utility import resultCount
from features import sentencePosition, sectionImportance, tfIDF, positiveNess, negativeNess

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

    def summarize(self):
        
        threadList = []
        i = 1
        for section in self.sections:
            
            t1 = threading.Thread(target = sentencePosition,
                                  kwargs = {'section': section})
            t1.start()

            t2 = threading.Thread(target = tfIDF, 
                                  kwargs = {'section': section})
            t2.start()

            t3 = threading.Thread(target = positiveNess, 
                kwargs = {'section': section, 'positiveKeywords': self.positiveKeywords})
            t3.start()

            t4 = threading.Thread(target = negativeNess,
                kwargs = {'section': section, 'negativeKeywords': self.negativeKeywords})
            t4.start()

            t5 = threading.Thread(target = sectionImportance,
                kwargs = {'title': self.title, 'titleImp': self.titleImp, 'section': section})
            t5.start()

            threadList.extend((t1, t2, t3, t4, t5))
            i += 2
        
            
        for thread in threadList:
            thread.join()
            
        self.calculateScore()
        
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
                print sentence.sentence,
                print sentence.score

    def summary(self, ratio = 0.8):
        values = []
        out = ""
        for section in self.sections:
            for sentence in section.sentences:
                values.append(sentence.tfidf*sentence.pos*sentence.imp)
        
        length = len(values)
        values = sorted(values)
        self.threshold = values[len(values)*ratio]
        
        for section in self.sections:
            for sentence in section.sentences:
                if sentence.tfidf*sentence.pos*sentence.imp > self.threshold:
                    out += " " + sentence.sentence
        return out

    def getScores(self):
        out = []

        for section in self.sections:
            for sentence in section.sentences:
                package = {}
                package['sent'] = sentence.sentence
                package['score'] = sentence.score
                out.append(package)
        
            
        return {'data': out}
        
def getSummary(url):
    s=Summarizer(url)
    s.summarize()
    return s.getScores()
