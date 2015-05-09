from section import Section
from sentence import Sentence
from utility import resultCount, word_path_similarity
from stemming.porter2 import stem
from stopwords import isStopWord
import json

def sentencePosition(section):
    nSen = section.nSen
    pos = 1
    for sen in section.sentences:
        sen.pos = float(nSen+1-pos)/nSen
        pos += 1

def sectionImportance(title, titleImp, section):
    count = resultCount(title + " " + section.heading)
    section.importance = float(count)/titleImp
    for sen in section.sentences:
        sen.imp = section.importance


wordDocFrq = {}
with open('data/wiki_docFrq.json') as data_file:    
    wordDocFrq = json.load(data_file)
wordDocFrq = wordDocFrq['docFrq']


def tfIDF(section):
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


def positiveNess(section, positiveKeywords):

    sectionKey = section.heading.split(" ")
    section.positiveScore = 1
    for key in sectionKey:
        key = key.lower()
        if isStopWord(key):
            continue
        for pos in positiveKeywords:
            pos = pos.lower()
            if isStopWord(pos):
                continue
            section.positiveScore = max(section.positiveScore,
                                        word_path_similarity(key, pos) + 1)
    for sentence in section.sentences:
        sentence.positiveScore = 1
        for word in sentence.words:
            word = word.lower()
            if isStopWord(word):
                continue
            for pos in positiveKeywords:
                pos = pos.lower()
                if isStopWord(pos):
                    continue
                sentence.positiveScore = max(sentence.positiveScore, 
                                        word_path_similarity(pos, word) + 1)

def negativeNess(section, negativeKeywords):

    sectionKey = section.heading.split(" ")
    for key in sectionKey:
        key = key.lower()
        if isStopWord(key):
            continue
        for neg in negativeKeywords:
            neg = neg.lower()
            if isStopWord(neg):
                continue
            section.negativeScore = min(section.negativeScore,
                                        1 - word_path_similarity(key, neg))

    for sentence in section.sentences:
        sentence.negativeScore = 1
        for word in sentence.words:
            word = word.lower()
            if isStopWord(word):
                continue
            for neg in negativeKeywords:
                neg = neg.lower()
                if isStopWord(neg):
                    continue
                sentence.negativeScore = min(sentence.negativeScore,
                                        1 - word_path_similarity(neg, word))

