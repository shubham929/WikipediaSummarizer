import urllib2
import json
from bs4 import BeautifulSoup
from stemming.porter2 import stem
from nltk.stem.wordnet import WordNetLemmatizer
import re


url = "http://localhost:8000/wiki/?url=http%3A%2F%2Fen.wikipedia.org%2Fwiki%2FSpecial%3ARandom" 

def dataTotalFrq():
    vocab = {}
    lmtzr = WordNetLemmatizer()
    for i in range(0, 1000):
        try:
            page=urllib2.urlopen(url)
            content = page.read()
            soup = BeautifulSoup(content)
            data = soup.get_text()
            words = re.findall(r'\b\w+\b', content)
            for word in words:
                word = word.lower()
                word = stem(word)
                if word in vocab:
                    vocab[word]+=1
                else:
                    vocab[word]=1
        except:
            continue
    return {"frequency" : vocab, "pages" : i+1}


def dataDocFrq():
    docFrq = {}
    count = 0
    for i in range(0, 1000):
        wordPresent = {}
        try:
            page=urllib2.urlopen(url)
            content = page.read()
            soup = BeautifulSoup(content)
            data = soup.get_text()
            words = re.findall(r'\b\w+\b', content)
            for word in words:
                word = word.lower()
                word = stem(word)
                wordPresent[word] = True
        except:
            continue
        count+=1
        for word in wordPresent:
            if word in docFrq:
                docFrq[word]+=1
            else:
                docFrq[word]=1

    return {"docFrq" : docFrq, "pages" : count}




data = dataDocFrq()
with open('data_wiki_docFrq', 'w') as outfile:
    json.dump(data, outfile)
        




        
