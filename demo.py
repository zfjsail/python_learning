
import string
import urllib
import urllib2
import re

# from __future__ import print_function

url = 'http://keg.cs.tsinghua.edu.cn/jietang/publication_list.html'
try:
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    content = response.read().decode('utf-8')
    pattern = re.compile('<(li|LI)>(.|\n)*?\.((.|\n)*?)\.(.|\n)*?</(li|LI)>', re.M)
    # pattern = re.compile('<li>(.*?)</li>', re.S)
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
        # print begin, end
        # print cnt, content[begin:end]
        items.append(content[begin:end+5])
        # print ' '
        content = content[end+1:]
        big = 0
        cnt = cnt + 1
        # if cnt == 155:
        #    break
    titles = []
    for item in items:
        title = re.findall(pattern, item)
        if title: # and "," not in title[0][2]:
            filt =  title[0][2]
            filt.replace("\n", " ")
            if "," not in filt:
                print filt
            # print filt
            # title = title[0][2]
            # pattern = re.compile('^\s.*', re.M)
            # title = re.findall(pattern, title)
            # re.sub('\n', ' ', title)
            # title.strip()
            # print title
        print ' '
        titles.append(title)
    # print content[0:50]
    # pattern = re.compile('Journal .*?Conference', re.S)
    # journal = re.search(pattern, content)
    # print journal.group(1)
    # result = re.search(pattern, content)
    # items = re.findall(pattern, content)
    # for item in items:
       # print result.group(0).strip()
       # print item
       # print ' '
except urllib2.URLError, e:
    if hasattr(e, "code"):
        print e.code
    if hasattr(e, "reason"):
        print e.reason
