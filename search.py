from bs4 import BeautifulSoup
import urllib2
from urlparse import urljoin
from selenium import webdriver
import urllib
import re
import time
import threading

driver = webdriver.Firefox()
lock = threading.Lock()
def resultCount(query):
    query = urllib.urlencode({'q' : query})
    url = "https://www.google.co.in/search?client=ubuntu&channel=fs&" + query + "&ie=utf-8&oe=utf-8&gfe_rd=cr&ei=I3I_VamyO6Ol8weZ-oC4DQ"
    lock.acquire()
    time.sleep(2)
    driver.get(url)
    html = driver.page_source
    lock.release()
    soup = BeautifulSoup(html)
    data = soup.find("div", {"id": "resultStats"})
    if type(data) == None:
        return 1
    out = re.search(r'About ([0-9,]*) results', data.text).group(1)
    out = out.replace(",", "")
    out = int(out)
    return out
