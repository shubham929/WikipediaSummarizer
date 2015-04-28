class Sentence:
    
    def __init__(self, sentence):
        self.rating = 0
        self.sentence = sentence
        self.words = re.findall(r'\w+', sentence)
        self.length = len(self.words)
        self.pos = 0
        self.tfidf = 0
        self.imp = 0
        self.negativeScore = 1
        self.positiveScore = 1
        self.score = 0
