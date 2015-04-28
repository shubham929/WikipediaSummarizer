import urllib
from lxml import etree
import urllib2
import nltk
import simplejson
import json
from stopwords import isStopWord
from google.google import search
from bs4 import BeautifulSoup
import re
import lxml
from lxml.html.clean import Cleaner
from StringIO import StringIO


cleaner = Cleaner()
cleaner.javascript = True 
cleaner.style = True 

def getURL(keyword):
    out=[]
    for url in search(keyword, stop=10):
        out.append(url)
    return out


def getText(url):
    page = urllib2.urlopen(url)
    content = page.read()
    html_doc = cleaner.clean_html(content)
    soup = BeautifulSoup(html_doc)
#    print soup.get_text()
    return soup.get_text()

def buildVocab(title):
    vocab = {}
    urlList = getURL(title)
    for url in urlList:
        text = getText(url)
        words = re.findall(r'\b\w+\b', text)
        for word in words:
            if isStopWord(word):
                continue
            print word
            if word in vocab:
                vocab[word]+=1
            else:
                vocab[word]=1
    return vocab


dKeys =  buildVocab("sachin tendulkar")

for word in dKeys:
    if dKeys[word]>1:
        print word,


