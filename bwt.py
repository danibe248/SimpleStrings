import time
import math
import sys
import pandas as pd

def mergesort(s):
    if len(s) == 1:
        return s
    else:
        m = math.floor(len(s)/2)
        sx = mergesort(s[:m])
        dx = mergesort(s[m:])
    return merge(sx,dx)

def merge(sx,dx):
    out = sx
    for e in dx:
        i = 0
        while i < len(sx) and sx[i][1] < e[1]:
            i = i + 1
        out.insert(i,e)
    return out

def suffixa2(s):
    if type(s) == str:
        t = s
        if t[-1] != '$':
            t = t + '$'
        m = []
        for i in range(0,len(t)):
            m.append([i,t[i:]+t[:i]])
        return m
    elif type(s) == list:
        t = s
        si = 0
        m = []
        for string in t:
            if string[-1] != '$':
                string = string + '$'
            for ci in range(0,len(string)):
                m.append([[si,ci],string[ci:]+string[:ci]])
            si = si + 1
        return m
    else:
        print('Please provide string or list of strings')
        return '0'

def bwt2(bwt):
    out = ''
    for i in bwt:
        #print(i)
        out = out + i[1][-1]
    f = ''.join(sorted(list(i for i in out)))
    sa = []
    for j in bwt:
        sa.append(j[0])
    return out, f, sa

def decode(f,b,om):
    out = '$'
    p = 0
    for i in range(0,len(f)-1):
        j = 0
        while f[j] != out[0] or p > 0:
            if f[j] == out[0]:
                p = p-1
            j = j + 1
        out = b[j] + out
        if b[j] == '$':
            j = j + 1
            while b[j] != '$':
                j = j + 1
        p = om.loc[j,b[j]] ##
        # print(str(j) + ' ' + b[j] + ' ' + str(occ(b,j)) + ' ' + str(om.loc[j,b[j]]))
    return out

# def occ(b,j):
#     if j >= len(b):
#         j = len(b) - 1
#     sigma = b[j]
#     count = 0  ##
#     while j > 0:
#         j = j-1
#         if b[j] == sigma:
#             count = count +1
#     return count

def occmatrix(b):
    a = sorted(list(set(b)))
    #df = pd.DataFrame(columns=list(''.join(sorted(list(i for i in a)))))
    df = pd.DataFrame(columns=','.join(sorted(list(i for i in a))).split(','))
    df = df.append(pd.DataFrame([[0]*len(a)],columns=list(''.join(sorted(list(i for i in a))))), ignore_index=True)
    for i in range(1,len(b)+1):
        j = 0
        r = [0] * len(a)
        for c in a:
            if c == b[i-1]:
                r[j] = int(df.loc[i-1,c] + 1)
            else:
                r[j] = int(df.loc[i-1,c])
            j = j + 1
        df = df.append(pd.DataFrame([r],columns=list(''.join(sorted(list(i for i in a))))), ignore_index=True)
    return df.astype(int)

def c(f):
    cs = {}
    a = sorted(list(set(f)))
    for c in a:
        i = 0
        cs[c] = 0
        while i < len(f) and f[i] != c:
            i = i + 1
            cs[c] = cs[c] + 1
    return cs

def strmatch(s,f,cs,om,bwt,sortm):
    out = []
    b = 0
    e = len(bwt)
    i = len(s) - 1
    while i >= 0:
        sigma = s[i]
        oldb = b
        b = cs[sigma] + om.loc[b,sigma]
        e = b + om.loc[e,sigma] - om.loc[oldb,sigma]
        i = i - 1
    for index in range(b,e):
        out.append(sortm[index][0])
    return sorted(out)

s = 'GGCAGATTCCCCCTAGACCCGCCCGCACCATGGTCAGGCATGCCCCTCCTCATCGCTGGGCACAGCCCAGAGGGT\
ATAAACAGTGCTGGAGGCTGGCGGGGCAGGCCAGCTGAGTCCTGAGCAGCAGCCCAGCGCAGCCACCGAGACACC\
ATGAGAGCCCTCACACTCCTCGCCCTATTGGCCCTGGCCGCACTTTGCATCGCTGGCCAGGCAGGTGAGTGCCCC\
CACCTCCCCTCAGGCCGCATTGCAGTGGGGGCTGAGAGGAGGAAGCACCATGGCCCACCTCTTCTCACCCCTTTG\
GCTGGCAGTCCCTTTGCAGTCTAACCACCTTGTTGCAGGCTCAATCCATTTGCCCCAGCTCTGCCCTTGCAGAGG\
GAGAGGAGGGAAGAGCAAGCTGCCCGAGACGCAGGGGAAGGAGGATGAGGGCCCTGGGGATGAGCTGGGGTGAAC\
CAGGCTCCCTTTCCTTTGCAGGTGCGAAGCCCAGCGGTGCAGAGTCCAGCAAAGGTGCAGGTATGAGGATGGACC\
TGATGGGTTCCTGGACCCTCCCCTCTCACCCTGGTCCCTCAGTCTCATTCCCCCACTCCTGCCACCTCCTGTCTG\
GCCATCAGGAAGGCCAGCCTGCTCCCCACCTGATCCTCCCAAACCCAGAGCCACCTGATGCCTGCCCCTCTGCTC\
CACAGCCTTTGTGTCCAAGCAGGAGGGCAGCGAGGTAGTGAAGAGACCCAGGCGCTACCTGTATCAATGGCTGGG\
GTGAGAGAAAAGGCAGAGCTGGGCCAAGGCCCTGCCTCTCCGGGATGGTCTGTGGGGGAGCTGCAGCAGGGAGTG\
GCCTCTCTGGGTTGTGGTGGGGGTACAGGCAGCCTGCCCTGGTGGGCACCCTGGAGCCCCATGTGTAGGGAGAGG\
AGGGATGGGCATTTTGCACGGGGGCTGATGCCACCACGTCGGGTGTCTCAGAGCCCCAGTCCCCTACCCGGATCC\
CCTGGAGCCCAGGAGGGAGGTGTGTGAGCTCAATCCGGACTGTGACGAGTTGGCTGACCACATCGGCTTTCAGGA\
GGCCTATCGGCGCTTCTACGGCCCGGTCTAGGGTGTCGCTCTGCTGGCCTGGCCGGCAACCCCAGTTCTGCTCCT\
CTCCAGGCACCCTTCTTTCCTCTTCCCCTTGCCCTTGCCCTGACCTCCCAGCCCTATGGATGTGGGGTCCCCATC\
ATCCCAGCTGCTCCCAAATAAACTCCAGAAG\
CCACTGCACTCACCGCACCCGGCCAATTTTTGTGTTTTTAGTAGAGACTAAATACCATATAGTGAACACCTAAGA\
CGGGGGGCCTTGGATCCAGGGCGATTCAGAGGGCCCCGGTCGGAGCTGTCGGAGATTGAGCGCGCGCGGTCCCGG\
GATCTCCGACGAGGCCCTGGACCCCCGGGCGGCGAAGCTGCGGCGCGGCGCCCCCTGGAGGCCGCGGGACCCCTG\
GCCGGTCCGCGCAGGCGCAGCGGGGTCGCAGGGCGCGGCGGGTTCCAGCGCGGGGATGGCGCTGTCCGCGGAGGA\
CCGGGCGCTGGTGCGCGCCCTGTGGAAGAAGCTGGGCAGCAACGTCGGCGTCTACACGACAGAGGCCCTGGAAAG\
GTGCGGCAGGCTGGGCGCCCCCGCCCCCAGGGGCCCTCCCTCCCCAAGCCCCCCGGACGCGCCTCACCCACGTTC\
CTCTCGCAGGACCTTCCTGGCTTTCCCCGCCACGAAGACCTACTTCTCCCACCTGGACCTGAGCCCCGGCTCCTC\
ACAAGTCAGAGCCCACGGCCAGAAGGTGGCGGACGCGCTGAGCCTCGCCGTGGAGCGCCTGGACGACCTACCCCA\
CGCGCTGTCCGCGCTGAGCCACCTGCACGCGTGCCAGCTGCGAGTGGACCCGGCCAGCTTCCAGGTGAGCGGCTG\
CCGTGCTGGGCCCCTGTCCCCGGGAGGGCCCCGGCGGGGTGGGTGCGGGGGGCGTGCGGGGCGGGTGCAGGCGAG\
TGAGCCTTGAGCGCTCGCCGCAGCTCCTGGGCCACTGCCTGCTGGTAACCCTCGCCCGGCACTACCCCGGAGACT\
TCAGCCCCGCGCTGCAGGCGTCGCTGGACAAGTTCCTGAGCCACGTTATCTCGGCGCTGGTTTCCGAGTACCGCT\
GAACTGTGGGTGGGTGGCCGCGGGATCCCCAGGCGACCTTCCCCGTGTTTGAGTAAAGCCTCTCCCAGGAGCAGC\
CTTCTTGCCGTGCTCTCTCGAGGTCAGGACGCGAGAGGAAGGCGC'
t = 'AAA'
sb = suffixa2(s)
ssort = mergesort(sb)
sbwt, f, sa = bwt2(ssort)
cs = c(f)
om = occmatrix(sbwt)
# s2 = decode(f,sbwt,om)
# print('S: ' + s + ' = ' + s2[:-1] + ' ==> ' + str(s == s2[:-1]) + '\nF: ' + f + '\nBWT: ' + sbwt)
# print(cs)
# sys.stdout.write(t + ': ')
start = time.time()
out = strmatch(t,f,cs,om,sbwt,ssort)
end = time.time()
print(out)
print(end-start)

# p = ['dot','acc','ecr','bbc','cat','qpo']
# r = 'c'
# sb = suffixa2(p)
# ssort = mergesort(sb)
# sbwt, f, sa = bwt2(ssort)
# cs = c(f)
# om = occmatrix(sbwt)
# s2 = decode(f,sbwt,om)
# print('S: ' + ', '.join(sorted(p)) + ' = ' + ', '.join(sorted(s2.split('$')[:-1])) + ' ==> ' + str(sorted(p) == sorted(s2.split('$')[:-1])) + '\nF: ' + f + '\nBWT: ' + sbwt)
# print(cs)
# sys.stdout.write(r + ': ')
# print(strmatch(r,f,cs,om,sbwt,ssort))
