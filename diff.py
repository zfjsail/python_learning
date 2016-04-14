import re

f1 = open('t1.txt', 'r')
f2 = open('t2.txt', 'r')

ts1 = []
ts2 = []
for line in f1:
    ts1.append(line)
for line in f2:
    ts2.append(line)
f1.close()
f2.close()

# step 1
diff1 = []
cnt = 0
for t1 in ts1:
    isInTs2 = 0
    for t2 in ts2:
        if t1.lower() == t2.lower(): # compare directly
            isInTs2 = 1
            cnt += 1
    if isInTs2 == 0:
        diff1.append(t1)

print 'step 1: diff amount', len(diff1)

pattern = re.compile('[ :?().]', re.S) # split pattern

diff2 = []
for t1 in diff1:
    t1 = t1.lower()
    a = re.split(pattern, t1) # split
    len1 = len(a)
    maxs = 0
    for t2 in ts2:
        cnt = 0
        t2 = t2.lower()
        b = re.split(pattern, t2)
        len2 = len(b)
        minl = min(len1, len2)
        for i in range(0, minl):
            if a[i] == b[i]: # compare words sequentially
                cnt += 1
        maxs = max(maxs, float(cnt)/len1)
    if maxs < 0.6:
        diff2.append(t1)

print 'step 2: diff amount', len(diff2)

diff3 = []
for t1 in diff2:
    t1 = t1.lower()
    a = re.split(pattern, t1)
    len1 = len(a)
    maxs = 0
    for t2 in ts2:
        cnt = 0
        t2 = t2.lower()
        b = re.split(pattern, t2)
        for i in range(0, len1): # decide whether every word in t1 is in t2
            if a[i] in b:
                cnt += 1
        maxs = max(maxs, float(cnt)/len1)
    if maxs < 0.6:
        diff3.append(t1)

print 'step 3: diff amount', len(diff3), '\n'
for i in range(0, len(diff3)):
    print i+1, diff3[i]
