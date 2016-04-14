
import string
import urllib
import urllib2
import requests
import enchant
import re

from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def isTitle(T, d):
    # print t
    cnt = 0
    words = T.split()
    for word in words:
        if d.check(word):
            cnt += 1
    r = float(cnt) / len(words)
    if(len(words) <= 1):
        return False
    # print r
    if r > 0.6:
        return True
    else:
        return False


url1 = 'http://keg.cs.tsinghua.edu.cn/jietang/publication_list.html'
url2_base = 'https://scholar.google.com/citations?user=n1zDCkQAAAAJ&hl=en&view_op=list_work&cstart=&pagesize=100&cstart='
url2_cstart_list = [0, 100, 200]
try:
    request = urllib2.Request(url1)
    response = urllib2.urlopen(request)
    content = response.read() # .decode('utf-8')
    pattern = re.compile('<(li|LI)>(.|\n)*?\.((.|\n)*?)\.(.|\n)*?</(li|LI)>', re.M)
    pos = content.index("Journal")
    content = content[pos:]
    cnt = 1
    big = 0
    items = []
    while True:
        begin1 = content.find('<li>')
        begin2 = content.find('<LI>')
        if begin1 == -1 and begin2 == -1:
            break
        if begin1 == -1:
            begin = begin2
            big = 1
        elif begin2 == -1:
            begin = begin1
        elif begin1 <= begin2:
            begin = begin1
        else:
            begin = begin2
            big = 1
        end1 = content.find('</li>')
        end2 = content.find('</LI>')
        if end1 == -1:
            end = end2
        elif end2 == -1:
            end = end1
        elif end1 <= end2:
            end = end1
        else:
            end = end2
        items.append(content[begin:end+5])
        content = content[end+1:]
        big = 0
        cnt = cnt + 1
    dic = enchant.Dict("en_US")
    titles1 = []
    cnt = 0
    for item in items:
        title = re.findall(pattern, item)
        if title: # and "," not in title[0][2]:
            cnt += 1
            t =  title[0][2]
            t = t.lstrip()
            t = t.replace("\n", " ")
            t = t.replace("\r", "")
            # if isTitle(t, dic):
            titles1.append(t)
            # print t
    # print cnt

    titles2 = []
    for cstart in url2_cstart_list:
        request = urllib2.Request(url2_base + str(cstart))

        # headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        # with requests.Session() as session:
        #    responset = session.post(url2, headers=headers)
        #    contentt = responset.content
        #    print contentt
        #    print '``````````````````````````````````````````````````````'
        response = urllib2.urlopen(request)
        content = response.read() # .decode('utf-8')
        pattern = re.compile('<tbody id="gsc_a_b"(.|\n)*?</tbody>', re.M)
        content = re.search(pattern, content)
        content = content.group(0)
    # print content.group(0)
        pattern = re.compile('class="gsc_a_at">((.|\n)*?)</a>', re.M)
        items = re.findall(pattern, content)
        for item in items:
            print item[0]
            titles2.append(item[0])

    for t1 in titles1:
        maxr = 0
        for t2 in titles2:
            sim = similar(t1, t2)
            if maxr < sim:
                maxr = sim
        if maxr > 0.8:
            titles1.remove(t1)
            # print t1

    # print "--------------------------------------"
    # for t in titles1:
        # print t

except urllib2.URLError, e:
    if hasattr(e, "code"):
        print e.code
    if hasattr(e, "reason"):
        print e.reason
