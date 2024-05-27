from Crypto.Util.number import bytes_to_long, long_to_bytes
from sq2 import sq2
p = 179358513830906148619403250482250880334528756349120678091666297907253922185623290723862265402777434007178297319701286775733620488613530869850160450412929764046707392082705800333548316425165863556480623955587411083384086805686199851628022437853672200835000268893800610064747558825805271528526924659142504913631

def split(f):
    if len(f) & 1:
        f += b"\x00"
    h = len(f) // 2
    return (bytes_to_long(f[:h]), bytes_to_long(f[h:]))

m = b"L'eau est vraiment froide par ici (et pas tres propre)"
x0, y0 = split(m)
k, x_2k, y_2k = (929382, 118454610237220659897316062413105144789761952332893713333891996727204456010112572423850661749643268291339194773488138402728325770671625196790011560475297285424138262812704729573910897903628228179414627406601128765472041473647769084599481166191241495167773352105622894240398746332477947478817552973851804951566, 65891615565820497528921288257089595342791556688007325193257144738940922602117787746412089423500836495505254334866586155889060897532850381510520943387446058037766901712521471259853536310481267471645770625452422081411718151580380288380630522313377397166067417623947500542258985636659962524606869196898543973764)

'''
x(2n) = A^n . x(0)
y(2n) = A^n . y(0)
'''

Ax_k = (pow(x0, -1, p) * x_2k) % p
Ay_k = (pow(y0, -1, p) * y_2k) % p

assert Ax_k == Ay_k
A_k = Ax_k
print(A_k)

'''
n = k_e = k/2
objectifs trouver l'inverse de k_e modulo phi(p)
phi(p) = (p-1)
k_e . k_d = 1 [phi(p)]
=> (A^k_e)^k_d = A
'''
k_e = k // 2
k_d = pow(k_e, -1, p-1)
A = pow(A_k, k_d, p)
assert (A_k == pow(A, k//2, p))
print(A)

'''
A = (a^2 + b^2)
a,b = getRandomNBitInteger(1024//16) = getRandomNBitInteger(64)
=> a,b € [2^63, (2^64)-1]

A = 388070793197506567215490364778692980485
A = 3^2 · 5 · 17 · 73 · 853 · 1193 · 6828686706854717038620990997

'''

# Traitement des facteurs / facteur % 4 = 1
x_y = []
for factor in [5, 17, 73, 853, 1193, 6828686706854717038620990997]:
    x, y = sq2(factor)
    x, y = abs(x), abs(y)
    assert x**2 + y**2 == factor
    x_y.append((x, y))
    print(f"{factor} = {x}^2 + {y}^2")

'''
(a^2 + b^2).(c^2 + d^2) = (a.c - b.d)^2 + (a.d + b.c)^2
'''

combinaisons = [x_y[0]]
combinaisons = [(3*a, 3*b) for a, b in combinaisons]
for c, d in x_y[1:]:
    new_combinaisons = []
    for (a0, b0) in combinaisons:
        a1 = a0 * c - b0 * d
        b1 = a0 * d + b0 * c
        a, b = abs(a1), abs(b1)
        new_combinaisons.append((a,b))
        a0, b0 = b0, a0
        a1 = a0 * c - b0 * d
        b1 = a0 * d + b0 * c
        a, b = abs(a1), abs(b1)
        new_combinaisons.append((a,b))
        combinaisons = new_combinaisons[:]

for a, b in combinaisons:
    assert A == a**2 + b**2

'''
a et b joue le même role => A = a^2 + b^2 = b^2 + a^2
=> ajout des combinaisons (b, a) à celles (a, b) trouvées
'''
combinaisons = [(a, b) for a, b in combinaisons if 2**63<=a<2**64]
new_combinaisons = []
for (a, b) in combinaisons:
    new_combinaisons.append((a,b))
    new_combinaisons.append((b,a))
combinaisons = new_combinaisons

print(combinaisons)
print(len(combinaisons))

x_2n1, y_2n1 = (151683403543233106224623577311980037274441590153911847119566701699367001537936290730922138442040542620222943385810242081949211326676472369180020899628646165132503185978510932501521730827126356422842852151275382840062708701174847422687809816503983740455064453231285796998931373590630224653066573035583863902921, 76688287388975729010764722746414768266232185597001389966088556498895611351239273625106383329192109917896575986761053032041287081527278426860237114874927478625771306887851752909713110684616229318569024945188998933167888234990912716799093707141023542980852524005127986940863843004517549295449194995101172400759)

'''
x(2n+1) = a.x(2n) + b.y(2n)
y(2n+1) = b.x(2n) - a.y(2n)

=> 

x(2n+1) = A^n . (a.x(0) + b.y(0))
y(2n+1) = A^n . (b.x(0) - a.y(0))

=> 

a.x(2n+1) + b.y(2n+1) = A^n . (a^2 . x(0) + a.b.y(0) + b^2 . x(0) - a.b.y(0)) = A^n . (a^2 + b^2) . x(0)
b.x(2n+1) - a.y(2n+1) = A^n . (a.b.x(0) + b^2 . y(0) - a.b.x(0) + a^2 . y(0)) = A^n . (a^2 + b^2) . y(0)

=>

a.x(2n+1) + b.y(2n+1) = A^n . A . x(0)
b.x(2n+1) - a.y(2n+1) = A^n . A . y(0)

=> 

x(0) = (a.x(2n+1) + b.y(2n+1)). inv(A) . inv(A^n)
x(0) commence par 404CTF{
'''

n_min = 2**18
inv_A = pow(A, -1, p)
print(inv_A)
def find_flag():
    global flag_start, a, b
    for a, b in combinaisons:
        print(a, b)
        x_0 = ((a * x_2n1 + b * y_2n1) * inv_A * pow(pow(A, n_min, p), -1, p)) % p
        for n in range(2**18):
            x_0 = (x_0 * inv_A) % p
            flag_start = long_to_bytes(x_0)
            try:
                flag_start.decode('ascii')
                print(flag_start)
                return n
            except:
                pass
    else:
        print("bad algo ...")
        quit()

'''
y_0 = (b.x(2n+1) - a.y(2n+1)) . inv(A) . inv(A^n)
'''
n = find_flag()

print(n)
A_n = pow(A, 2**18+n+1, p)
y_0 = ((b * x_2n1 - a * y_2n1) * inv_A * pow(A_n, -1, p)) % p
flag_end = long_to_bytes(y_0)
if flag_end[-1] == b"\x00":
    flag_end = flag_end[:-1]

flag = flag_start + flag_end
print(f"{flag=}")
