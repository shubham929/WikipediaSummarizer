from bs4 import BeautifulSoup
from selenium import webdriver
import urllib
import re
import time
import threading
from nltk.corpus import wordnet as wn


driver = webdriver.Firefox()
slock = threading.Lock()
def resultCount(query):
    query = urllib.urlencode({'q' : query})
    url = "https://www.google.co.in/search?client=ubuntu&channel=fs&" + query + "&ie=utf-8&oe=utf-8&gfe_rd=cr&ei=I3I_VamyO6Ol8weZ-oC4DQ"
    slock.acquire()
    time.sleep(2)
    driver.get(url)
    html = driver.page_source
    slock.release()
    soup = BeautifulSoup(html)
    data = soup.find("div", {"id": "resultStats"})
    if data == None:
        print query
        return 1
    out = re.search(r'About ([0-9,]*) results', data.text).group(1)
    out = out.replace(",", "")
    out = int(out)
    return out


wplock = threading.Lock()
def word_path_similarity(s1, s2):
    wplock.acquire()
    val = 0
    if(s1.lower == s2.lower):
        return 1.0

    ss1 = wn.synsets(s1.lower())
    ss2 = wn.synsets(s2.lower())
    for t1 in ss1:
        for t2 in ss2:
            val = max(wn.path_similarity(t1, t2), val)
    wplock.release()
    return val
