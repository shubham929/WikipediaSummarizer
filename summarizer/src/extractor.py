import urllib2
import urllib
import re
from bs4 import BeautifulSoup

def removeSqBr(s):
    out=""
    sLen=len(s)
    i=0
    while i < sLen:
        if s[i] is '[' and s[i+1] is '[':
            i+=2
            count=1
            news=""
            while count is not 0:
                if s[i] is '[' and s[i+1] is '[':
                    count+=1
                    news+="[["
                    i+=2
                
                elif s[i] is ']' and s[i+1] is ']':
                    count-=1
                    if count is not 0:
                        news+="]]"
                    i+=2
                else:
                    news+=s[i]
                    i+=1

            out+=removeSqBr(news)
            
        elif s[i] is '|':
            out=""
            i+=1
            
        else:
            out+=s[i]
            i+=1
    return out

def getTitle(url):
    title=re.sub(r'.*/([^/]*)', r'\1', url)
    if title=="":
        title=url
    return title

def getImageURL(url):
    title = getTitle(url)
    url = 'http://en.wikipedia.org/w/index.php?action=raw&title='+title
    data = urllib2.urlopen(url).read()
    #return data
    if re.search(r'image\s*=\s*([^\.]+\.\w+)', data):
        imagename = re.search(r'image\s*=\s*([^\.]+\.\w+)', data).group(1)
        imagename = imagename.replace(" ", "_")
        url1 = 'http://en.wikipedia.org/wiki/' + title
        soup = BeautifulSoup(urllib2.urlopen(url1).read())
        for s in soup.find_all('img'):
            decode = urllib.unquote(s['src'])
            if imagename in decode:
                return 'http://' + s['src'].replace("//", '')
    return ""
    
        



def getText(url):
    title = getTitle(url)
    data1=""
    url = 'http://en.wikipedia.org/w/index.php?action=raw&title='+title
    data=urllib2.urlopen(url)
    data=data.read()
#    return data
    data=re.sub("<ref[^>]*/>", "", data)
    data=re.sub("<ref([^</](<[^/])*/*)*</ref>", "", data)
    dLen=len(data)
    i=0
#    return data
    while i<dLen:
        
        if data[i]=='{' and data[i+1]=='{':
            count=1
            i+=2
            while count is not 0:
                if data[i]=='{' and data[i+1]=='{':
                    count+=1
                    i+=2
                elif data[i]=='}' and data[i+1]=='}':
                    count-=1
                    i+=2
                else:
                    i+=1
    
        elif data[i]=='[' and data[i+1]=='[':
            s="[["
            count=1
            i+=2
            flag=True
            if data[i:i+5]=="File:":
                flag=False
            while count is not 0:
                if data[i]=='[' and data[i+1]=='[':
                    s+="[["
                    count+=1
                    i+=2
            
                elif data[i]==']' and data[i+1]==']':
                    s+="]]"
                    count-=1
                    i+=2

                else:
                    s+=data[i]
                    i+=1
            if flag:
                data1+=removeSqBr(s)

        else:
            data1+=data[i]
            i+=1


    data1 = re.split("(=)*[S|s]ee [A|a]lso(=)*", data1)[0]
    data1 = re.sub("'*", "", data1)

    data1 = re.sub("<!--[^>]*-->", "", data1)
    data1 = re.sub("\(\)", "", data1)
    data1 = re.sub(" ,", ",", data1)
    data1 = re.sub(r'(==+)([^=]*(==?[^=])?)(==+)', r'\n!!!@@@\2===\n', data1)
    data1 = re.sub(r'{[^}]*}', '', data1)
    
#    data2=re.sub(r'==(\w+)==', r'{{Heading}}\1', data1)
#   data2=re.split('{{Heading}}', data2)
    return data1


def getJSON(url):
    title = getTitle(url)
    text = getText(title)
    text = re.sub(r'\n\*.*\n', r'\n', text)
    text = re.sub(r'\s+', r' ', text)
    text = '@@@Main===' + text + '!!!'
    rawSections = re.findall(r'(@@@([^!](!!?[^!])?)*!!!)', text)
    article = {}
    sections = []
    for section in rawSections:
        section_data = section[0]
        section_data = re.sub(r'@@@$', '', section_data)
        sec_div = re.split(r'===', section_data)
        #print sec_div
        heading = sec_div[0]
        content = sec_div[1]
        heading = re.sub(r'@@@', '', heading)
        content = re.sub(r'!!!', '', content)
        sections.append({'heading': heading, 'content' : content})
        
    title = title.replace("_", " ")
    article = {'sections': sections, 'title': title}
    return article
