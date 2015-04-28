from nltk.corpus import wordnet as wn

def word_path_similarity(s1, s2):
    print "<<"
    val = 0
    if(s1.lower == s2.lower):
        return 1.0
        
    ss1 = wn.synsets(s1.lower())
    ss2 = wn.synsets(s2.lower())
    for t1 in ss1:
        for t2 in ss2:
            val = max(wn.path_similarity(t1, t2), val)
            print "::"
    print ">>"
    return val
