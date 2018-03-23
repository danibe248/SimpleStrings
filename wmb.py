import pandas as pd

def edit(s1,s2):
    m = len(s1) + 1
    n = len(s2) + 1
    v = pd.DataFrame([[0] * n] * m,columns=','.join(list(str(i) for i in range(0,n))).split(','))
    for i in range(0,m):
        v.loc[i,str(0)] = i
    for j in range(0,n):
        v.loc[0,str(j)] = j
    for i in range(1,m):
        for j in range(1,n):
            if s1[i-1] == s2[j-1]:
                v.loc[i,str(j)] = v.loc[i-1,str(j-1)]
            else:
                v.loc[i,str(j)] = 1 + min(min(v.loc[i,str(j-1)],v.loc[i-1,str(j)]),v.loc[i-1,str(j-1)])
    return v.loc[m-1,str(n-1)]

def bm(s,a):
    out = {}
    m = pow(2,len(s)-1)
    for c in a:
        out[c] = 0
    for i in s:
        out[i] = out[i] | m
        m = (m >> 1)
    return out

def wmb(t,s,a,tau):
    out = []
    m = pow(2,len(s)-1)
    mm = 1
    b = bm(s,a)
    dt = []
    d = [0] * (len(t)+1)
    j = 1
    for c in t:
        d[j] = ((d[j-1] >> 1) | m) & b[c]
        j = j + 1
    dt.append(d)
    for k in range(1,tau+1):
        d = [0] * (len(t)+1)
        w = len(s) - 1
        count = 1
        while count <= k:
            d[0] = d[0] + pow(2,w)
            w = w - 1
            count = count + 1
        j = 1
        for c in t:
            d[j] = (((d[j-1] >> 1) | m) & b[c]) | ((dt[k-1][j-1] >> 1) | m) | dt[k-1][j-1] | ((dt[k-1][j] >> 1) | m)
            #if d[j] == pow(2,len(s))-1 and k == tau:
            if d[j] % 2 != 0 and k == tau:
                out.append(j-1)
            j = j + 1
        dt.append(d)
    return out

t = 'babcabcadc'
s = 'abca'
a = ['a','b','c','d']
tau = 2
r = wmb(t,s,a,tau)
print(r)
for q in r:
    i = len(s) - tau
    flag = False
    while i <= len(s) + tau and not(flag):
        sx = q+1 - i
        if sx <= 0:
            sx = 0
            flag = True
        current = t[sx:q+1]
        e = edit(s,current)
        if e <= tau:
            print(str(q+1) + ' ' + current + ' ' + str(e))
        i = i + 1
