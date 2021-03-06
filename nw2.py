import copy
import math
from Bio import pairwise2
from datetime import datetime

def nw(s,t,mt,mmt,indel):
    snew = '$'+s
    tnew = '$'+t
    a = range(0,len(tnew))
    b = range(0,len(snew))
    df = []
    for i in b:
        df.append([0]*len(a))
    v = copy.deepcopy(df)
    for j in a[1:]:
        df[0][j] = indel*j
        v[0][j] = '→'
    for i in b[1:]:
        df[i][0] = indel*i
        v[i][0] = '↓'
    for i in b[1:]:
        for j in a[1:]:
            d1 = 0
            if snew[i] == tnew[j]:
                d1 = df[i-1][j-1]+mt
            else:
                d1 = df[i-1][j-1]+mmt
            d2 = df[i][j-1] + indel
            d3 = df[i-1][j] + indel
            l = [d1,d2,d3]
            if mt <= mmt or mt <= indel:
                df[i][j] = min(l)
                if df[i][j] == d1:
                    v[i][j] = '↘'
                elif df[i][j] == d2:
                    v[i][j] = '→'
                else:
                    v[i][j] = '↓'
            else:
                df[i][j] = max(l)
                if df[i][j] == d1:
                    v[i][j] = '↘'
                elif df[i][j] == d2:
                    v[i][j] = '→'
                else:
                    v[i][j] = '↓'
    o1, o2 = rec_nw(v,snew,tnew)
    return o1, o2, df[i][j]

def rec_nw(v,snew,tnew):
    out1 = ''
    out2 = ''
    i = len(v) - 1
    j = len(v[0]) -1
    while i != 0 and j != 0:
        if v[i][j] == '→':
            out2 = tnew[j] + out2
            out1 = '-' + out1
            j = j - 1
        elif v[i][j] == '↓':
            out1 = snew[i] + out1
            out2 = '-' + out2
            i = i - 1
        else:
            out1 = snew[i] + out1
            out2 = tnew[j] + out2
            j = j - 1
            i = i - 1
    return out1, out2

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
ATCCCAGCTGCTCCCAAATAAACTCCAGAAG'
t = 'CCACTGCACTCACCGCACCCGGCCAATTTTTGTGTTTTTAGTAGAGACTAAATACCATATAGTGAACACCTAAGA\
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
start = datetime.now()
o1, o2, score = nw(s,t,1,0,0)
time = (datetime.now() - start).total_seconds()
# print(o2)
# print(o1)
print(score)
print(time)
start = datetime.now()
alignments = pairwise2.align.globalxx('bocca','boccca')
time = (datetime.now() - start).total_seconds()
print(time)
# print(alignments[0][0])
# print(alignments[0][1])
print(alignments[0][2])
print(alignments[0][0])
print(alignments[0][1])
