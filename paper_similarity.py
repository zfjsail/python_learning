import urllib2
import enchant
import re

from difflib import SequenceMatcher

def similar(a, b): # title similarity
    a = a.lower()
    b = b.lower()
    return SequenceMatcher(None, a, b).ratio()

def isTitle(T, d): # determine whether a string is a title
    cnt = 0
    words = T.split()
    for word in words:
        if d.check(word.lower()):
            cnt += 1
    r = float(cnt) / len(words)
    if(len(words) <= 1):
        return False
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
    pos = content.index("Journal")
    content = content[pos:] # after 'journal ' is considered papers
    items = []
    while True:
        begin1 = content.find('<li>')
        begin2 = content.find('<LI>')
        begin = min(begin1, begin2)
        if begin1 == -1 and begin2 == -1:
            break
        end1 = content.find('</li>')
        end2 = content.find('</LI>')
        e_min = min(end1, end2)
        if e_min != -1:
            end = e_min
        elif end1 == -1:
            end = end2
        else:
            end = end1
        items.append(content[begin:end+5])
        content = content[end+5:]
    dic = enchant.Dict("en_US")
    titles1 = []
    pattern = re.compile('<(li|LI)>(.|\n)*?\.((.|\n)*?)\.(.|\n)*?</(li|LI)>', re.M)
    cnt = 0
    for item in items:
        cnt += 1
        title = re.findall(pattern, item)
        if title: 
            t = title[0][2]
            t = t.lstrip() # pre-process
            t = t.replace('\r', '')
            t = t.replace('\n', ' ')
            if isTitle(t, dic):
                titles1.append(t)
                # print t
    print cnt

    titles2 = []
    for cstart in url2_cstart_list:
        request = urllib2.Request(url2_base + str(cstart))
        response = urllib2.urlopen(request)
        content = response.read() 
        pattern = re.compile('<tbody id="gsc_a_b"(.|\n)*?</tbody>', re.M)
        content = re.search(pattern, content)
        content = content.group(0)
        pattern = re.compile('class="gsc_a_at">((.|\n)*?)</a>', re.M)
        items = re.findall(pattern, content)
        for item in items:
            titles2.append(item[0])
            # print item[0]

    diff = []
    for t1 in titles1:
        maxr = 0
        for t2 in titles2:
            sim = similar(t1, t2)
            maxr = max(maxr, sim)
        if maxr < 0.5:
            diff.append(t1)

    i = 1
    for t in diff:
        # print i, t
        i += 1

except urllib2.URLError, e:
    if hasattr(e, "code"):
        print e.code
    if hasattr(e, "reason"):
        print e.reason
