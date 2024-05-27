from gauss import solution_systeme
from json import loads

M = []
B = []

with open('collect.data', 'r') as datas_file:
    for data in datas_file:
        data = loads(data)
        pks = data["public_key"]
        enc = data["encrypted"]
        pks = [d/enc for d in pks]
        M.append(pks)
        B.append(1)

X = solution_systeme(M, B)
X = [round(x) for x in X]
print(X)

X = [0, 0] + X[:-2]
print(X)

flag = []
for i in range(0, len(X), 8):
    c = sum([X[i+j]*(2**(7-j)) for j in range(8)])
    c = chr(c)
    flag.append(c)

flag = ''.join(flag)
print(f'{flag=}')
