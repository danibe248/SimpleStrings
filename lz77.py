def phi_ind(s):
    p = [-1,0]
    k = 0
    for i in range(1,len(s)):
        k = p[i]
        while k >= 0 and s[k] != s[i]:
            k = p[k]
        p.append(k+1)
    return p

def kmp(s,t):
    if len(t) != 0:
        out = []
        p = phi_ind(s)
        m = len(s)
        n = len(t)
        i = 0
        for j in range(0,n):
            while i >= 0 and s[i] != t[j]:
                i = p[i]
            i = i + 1
            if i == m:
                out.append(j-m+1)
                i = p[m]
        return out
    else:
        return []

def lz(s,w,la):
    result = []
    l = len(s)
    back = w - la
    i = 0
    zuzzurellone = 0
    while i < l:
        if i > back:
            zuzzurellone = i - back
        cuBack = ''
        cuAhead = ''
        if i <= back:
            cuBack = s[:i]
        else:
            cuBack = s[i-back:i]
        if l - i < la:
            cuAhead = s[i:]
        else:
            cuAhead = s[i:i + la]
        #print(cuBack + ' | ' + cuAhead)
        out = [0]
        count = 1
        temp = []
        while i+count-1 < l and count <= la and len(out) != 0:
            temp = out
            xs = cuAhead[:count]
            out = kmp(xs,cuBack)
            #print(str(i) + ' - xs: ' + xs + ' ' + str(len(out)))
            count = count + 1
        # if count == 2:
        #     temp = []
        # count = count - 1
        # if len(temp) == 0 and i+count < l:
        #     result.append('<0,0,' + s[i] + '>')
        #     #print(str(i) + ' - <0,0,' + s[i] + '>')
        #     i = i + 1
        # else:
        #     if not(i+count < l):
        #         result.append('<' + str(i-out[-1]-zuzzurellone) + ',' + str(count) + ',>')
        #         #print(str(i) + ' - <' + str(i-out[-1]-zuzzurellone) + ',' + str(count) + ',>')
        #     else:
        #         result.append('<' + str(i-temp[-1]-zuzzurellone) + ',' + str(count-1) + ',' + s[i+count-1] + '>')
        #         #print(str(i) + ' - <' + str(i-temp[-1]-zuzzurellone) + ',' + str(count-1) + ',' + s[i+count-1] + '>')
        #     i = i + count
        if count <= 2:
            count = count - 1
        else:
            count = count - 2
        xs = cuAhead[:count]
        out = kmp(xs,cuBack)
        if len(out) == 0:
            result.append('<0,0,' + s[i] + '>')
            print(str(i) + ' - <0,0,' + s[i] + '>')
            i = i + 1
        else:
            if i + count < l:
                result.append('<' + str(i-out[-1]-zuzzurellone) + ',' + str(count) + ',' + s[i+count] + '>')
                print(str(i) + ' - <' + str(i-out[-1]-zuzzurellone) + ',' + str(count) + ',' + s[i+count] + '>')
            else:
                result.append('<' + str(i-out[-1]-zuzzurellone) + ',' + str(count) + ',>')
                print(str(i) + ' - <' + str(i-out[-1]-zuzzurellone) + ',' + str(count) + ',>')
            i = i + count + 1
    return result

def decode(z):
    out = ''
    for e in z:
        l = e[1:-1].split(',')
        out = out + out[len(out)-int(l[0]):len(out)-int(l[0])+int(l[1])] + l[2]
    return out

s = 'barrayar bar by barrayar bay'
out = lz(s,30,15)
print(decode(out) == s)
print(len(s))
print(str(len(''.join(out))) + ' ==> ' + str(len(''.join(out))-(len(out)*4)))
