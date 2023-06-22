def lcs(a, b):
    lena = len(a)
    lenb = len(b)
    c = [[0 for i in range(lena + 1)] for j in range(lenb + 1)]
    for i in range(lenb):
        for j in range(lena):
            if b[i] == a[j]:
                c[i + 1][j + 1] = c[i][j] + 1
            else:
                c[i + 1][j + 1] = max(c[i + 1][j], c[i][j + 1])
    return c


def find(x, y, z):
    while x > 0 and y > 0:
        if b[x-1] == a[y-1]:
            z += (str(b[x-1]))
            x -= 1
            y -= 1
        else:
            if c[x][y-1] < c[x-1][y]:
                x -= 1
            elif c[x][y-1] > c[x-1][y]:
                y -= 1
            else:
                find(x-1, y, z)
                find(x, y-1, z)
                return
    LCS.append(z[::-1])

a = 'ABCBDAB'
b = 'BDCABA'
LCS = []
c = lcs(a, b)
print('LCS长度为'+str(c[-1][-1]))
print('     ', end='')
print('  '.join(a))
for i in c:
    if c.index(i) != 0:
        print(b[c.index(i)-1], end='')
    else:
        print(' ', end='')
    print(i)
find(len(b), len(a), '')
print(LCS)
