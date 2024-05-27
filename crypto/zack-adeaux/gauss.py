from Crypto.Util.number import getRandomNBitInteger


def echange_ligne(A,i,j):
    """Applique l’opération élémentaire Li <-> Lj à la matrice A"""
    n = len(A[0]) # nbre de colonnes de A
    for k in range(n):
        temp = A[i][k]
        A[i][k] = A[j][k]
        A[j][k] = temp

def echange_ligne_bis(A,i,j):
    """Applique l’opération élémentaire Li <-> Lj à la matrice A"""
    temp = A[i]
    A[i] = A[j]
    A[j] = temp

def transvection(A,i,j,mu):
    """Applique l’opération élémentaire Li <-Li + mu*Lj à la matrice A"""
    # cas où A est une matrice colonne
    if type(A[0]) != list:
        A[i] = A[i] + mu*A[j]
    else:
        n = len(A[0]) # nbre de colonnes de A
        for k in range(n):
            A[i][k] = A[i][k] + mu*A[j][k]

def pivot_partiel(A, j0):
    n = len(A) # nbre de lignes de A
    imax = j0 # indice de ligne avec pivot max
    for i in range(j0+1, n):
        if abs(A[i][j0]) > abs(A[imax][j0]):
            imax = i
    return imax

def solution_triangle(A,b):
    """ Renvoie la solution du système Ax =b
    lorsque A est tringulaire supérieure inversible"""
    n =len(b)
    x = [0 for i in range(n)]
    x[n-1] = b[n-1]/A[n-1][n-1]
    for i in range(n-2,-1,-1):
        s = 0
        for j in range(i+1,n):
            s = s + A[i][j]*x[j]
        x[i] = (b[i] - s)/ A[i][i]
    return x

import copy
def solution_systeme(A0,b0):
    """ Renvoie la solution X du système de Cramer A0 X= b0"""
    A,b = copy.deepcopy(A0), copy.deepcopy(b0) # on ne détruit pas les données initiales
    n = len(A)
    # Mise sous forme triangulaire
    for j in range(n-1): # on itère n-1 fois
        i0 = pivot_partiel(A,j)
        echange_ligne_bis(A,j,i0)
        echange_ligne_bis(b,j,i0)
        for i in range(j+1,n):
            x = A[i][j]/A[j][j]
            transvection(A,i,j,-x)
            transvection(b,i,j,-x) # attention b matrice colonne
    # phase de remontée
    return solution_triangle(A,b)

if __name__ == "__main__":
    a,b,c,d,e,f,g,h,i = [getRandomNBitInteger(2048) for _ in range(9)]
    B = [a+c, d+f, g+i]
    a,b,c = a/B[0], b/B[0], c/B[0]
    d,e,f = d/B[1], e/B[1], f/B[1]
    g,h,i = g/B[2], h/B[2], i/B[2]
    B = [1, 1, 1]
    A = [[a,b,c], [d,e,f], [g,h,i]]
    X = solution_systeme(A,B)
    print(X)
