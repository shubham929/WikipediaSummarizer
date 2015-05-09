import nltk
import re
from sentence import Sentence

class Section:
    
    def __init__(self, data):
        
        self.heading = data['heading']  #heading of the section
        if self.heading == 'Main':
            self.heading = ''
        self.heading = ''.join([i if ord(i) < 128 else ' ' for i in self.heading])
        self.content = data['content']   #data contained in the section
        self.importance = 0
        self.negativeScore = 1
        self.positiveScore = 1
        sentences = self.splitContentToSentences()
        self.sentences = []
        for sentence in sentences:
            if re.search(r'\w', sentence):
                self.sentences.append(Sentence(sentence))
        
        self.nSen = len(sentences)

    def splitContentToSentences(self):
        sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
        content = ""
        content = ''.join([i if ord(i) < 128 else ' ' for i in self.content])
        sentences =  sent_detector.tokenize(content)
        return sentences
