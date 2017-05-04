# -*- coding: utf-8 -*-
import sys
import re
import operator

reload(sys)
sys.setdefaultencoding('utf-8')

switch = {
    "건강과 의학": 0,
    "경제": 1,
    "과학": 2,
    "교육": 3,
    "문화와 종교": 4,
    "사회": 5,
    "산업": 6,
    "여가생활": 7
}
# merge files
fr = open("HKIB-20000_merge.txt", 'w')
fr1 = open("HKIB-20000_001.txt", 'r')
fr.write(fr1.read())
fr1.close()
fr2 = open("HKIB-20000_002.txt", 'r')
fr.write(fr2.read())
fr2.close()
fr3 = open("HKIB-20000_003.txt", 'r')
fr.write(fr3.read())
fr3.close()
fr4 = open("HKIB-20000_004.txt", 'r')
fr.write(fr4.read())
fr4.close()
fr.write("@DOCUMENT")
fr.close()

# global variable
text_arr = {}
chi_result = {}
textflag = 0


# make text list
textflag = 0
t = u""
text_arr = []
n = 0
fr = open("HKIB-20000_merge.txt", 'r')
lines = fr.readlines()
for line in lines:
    if line.startswith("#CAT'03"):
        cat = switch[line.split('/')[1]]
    if textflag == 1:
        if line.startswith("<KW>") or line.startswith("@DOCUMENT"):
            textflag = 0
            t = re.split(r"[<,>,(,),\[,\],\{,\},\",.,-,\s,/,:,,]+", t)
            t.pop()
            t.pop(0)
            t = list(set(t))
            for txt in t:
                text_arr.append(txt + ":-:*" + str(cat))
        else:
            t = t + line

    if line.startswith('#TEXT'):
        textflag = 1
        t = ""
        n = n + 1
    else:
        continue

f = open("textList_train.txt", "w")
for txt in text_arr:
    f.write(txt.split(":-:*")[0] + "\n")
fr.close


# calculate chi-square of each text
doc = [0, 0, 0, 0, 0, 0, 0, 0]
textflag = 0
cat = 0
n = 0

# bring text features
f = open("textList_train.txt", "r")
lines = f.readlines()
for line in lines:
    text_arr[line.split("\n")[0]] = [0, 0, 0, 0, 0, 0, 0, 0]

# count appearance time according to category number
fr = open("HKIB-20000_merge.txt", 'r')
lines = fr.readlines()
for line in lines:
    if line.startswith("#CAT'03"):
        cat = switch[line.split('/')[1]]
        doc[cat] = doc[cat] + 1
    if textflag == 1:
        if line.startswith("<KW>") or line.startswith("@DOCUMENT"):
            n = n + 1
            textflag = 0
            t = re.split(r"[<,>,(,),\[,\],\{,\},\",.,-,\s,/,:,,]+", t)
            t.pop()
            t.pop(0)
            t = list(set(t))
            for txt in t:
                text_arr[txt][cat] = text_arr[txt][cat] + 1
        else:
            t = t + line

    if line.startswith('#TEXT'):
        textflag = 1
        t = ""
fr.close()

# calculate chi-square for training file
for text in text_arr.keys():
    chi_max = 0
    for cat in range(0, 8):
        a = b = c = d = 0
        # if text_arr[text][cat] == 0:
        #   continue
        a = text_arr[text][cat]
        for ct in range(0, 8):
            if ct == cat:
                continue
            else:
                c = c + text_arr[text][ct]
        b = doc[cat] - a
        d = n - doc[cat] - c
        chi = float(n * pow(((a * d) - (b * c)), 2)) / float((a + c) * (b + d) * (a + b) * (c + d))
        if chi_max < chi:
            chi_max = chi
    chi_result[text] = [0, chi_max]
    # print(chi_max)
fr.close()
sort = sorted(chi_result, key=lambda i: float(chi_result[i][1]), reverse=True)
n = 1
min = 10000
max = 0
for i in sort:
    chi_result[i][0] = n
    n = n + 1

# make testfile.txt
textflag = 0

fw = open("trainfile.txt", "w")
fr = open("HKIB-20000_merge.txt", 'r')
lines = fr.readlines()
for line in lines:
    if line.startswith("#CAT'03"):
        cat = switch[line.split('/')[1]]
    if textflag == 1:
        if line.startswith("<KW>") or line.startswith("@DOCUMENT"):
            textflag = 0
            t = re.split(r"[<,>,(,),\[,\],\{,\},\",.,-,\s,/,:,,]+", t)
            t.pop()
            t.pop(0)
            t = list(set(t))
            result = {}
            s = str(cat + 1) + " "
            for word in t:
                if word in chi_result:
                    result[chi_result[word][0]] = chi_result[word][1]
            sort = sorted(result.items(), key=operator.itemgetter(0))
            for r in sort:
                s = s + str(r[0]) + ':' + str(r[1]) + ' '
            fw.write(s[:-1])
            fw.write("\n")
        else:
            t = t + line
    if line.startswith('#TEXT'):
        textflag = 1
        t = ""
fr.close()
fw.close()

##############################################################
# make testfile.txt
textflag = 0

fw = open("testFile.txt", "w")
fr = open("HKIB-20000_005.txt", 'r')
lines = fr.readlines()
for line in lines:
    if line.startswith("#CAT'03"):
        cat = switch[line.split('/')[1]]
    if textflag == 1:
        if line.startswith("<KW>") or line.startswith("@DOCUMENT"):
            textflag = 0
            t = re.split(r"[<,>,(,),\[,\],\{,\},\",.,-,\s,/,:,,]+", t)
            t.pop()
            t.pop(0)
            t = list(set(t))
            result = {}
            s = str(cat + 1) + " "
            for word in t:
                if word in chi_result:
                    result[chi_result[word][0]] = chi_result[word][1]
            sort = sorted(result.items(), key=operator.itemgetter(0))
            for r in sort:
                s = s + str(r[0]) + ':' + str(r[1]) + ' '
            fw.write(s[:-1])
            fw.write("\n")
        else:
            t = t + line
    if line.startswith('#TEXT'):
        textflag = 1
        t = ""
fr.close()
fw.close()
