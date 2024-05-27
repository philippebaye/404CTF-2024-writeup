# La Seine

<img alt="énoncé du challenge" src="enonce.png" width=500>

----

### 1. Analyse du script

Le script [`LaSeine.py`](./LaSeine.py) fourni génère successivement la signature de 2 messages. La 1ère pour le flag, et la 2ème pour le message témoin `L'eau est vraiment froide par ici (et pas tres propre)`.

La réalisation des signatures s'appuie sur :
- `p`, un nombre premier de 1024 bits
- `a` et `b`, 2 entiers $\in \lbrace 2^{63}, 2^{63}+1, \ldots, 2^{64}-1 \rbrace$

A noter que `p`, `a` et `b` sont identiques pour les 2 signatures.

Pour réaliser cette signature :
- le message est découpé en 2, avec si besoin l'ajout prélable d'un `\x00` si la taille du message est impaire.
- un `k` est généré "aléatoirement" et différent à chaque signature, en choisissant si celui-ci doit être pair (`b=0`) ou impair (`b=1`).
    - pour la signature du message témoin, le `k` utilisé est pair
    - alors que pour celle du flag, il est impair
- ce `k` sert à définir successivement les termes de 2 suites $x_{n}$ et $y_{n}$ qui sont en relation l'une avec l'autre.

Les 1er termes de ces 2 suites sont définis à partir du message à signer :
- $x_{0}$ est défini comme étant la moitié gauche du message à signer
- $y_{0}$ est défini comme étant la moitié droite du message à signer

Les termes suivants sont définis par itérations :
- $x_{n+1} \equiv a \cdot x_{n} + b \cdot y_{n} \pmod{p}$
- $y_{n+1} \equiv b \cdot x_{n} - a \cdot y_{n} \pmod{p}$

La paire $(x_{k}, y_{k})$ constitue la signature du message.

En plus du script on dispose via le contenu du fichier [out.txt](./out.txt) des éléments suivants :
- `p`
- $(x_{k1}, y_{k1})$ correspondant à la signature du flag
- $(x_{k2}, y_{k2})$ correspondant à la signature du message témoin
- `k2`

----

### 2. Détermination de $a^2 + b^2$

On remarque qu'en appliquant 2 itérations successives on obtient les relations suivantes :
- $x_{n+2} \equiv (a^{2} + b^{2}) \cdot x_{n} \pmod{p}$
- $y_{n+2} \equiv (a^{2} + b^{2}) \cdot y_{n} \pmod{p}$

Si on pose $A = a^{2} + b^{2}$, on a alors par récurrence $\forall n \in \mathbb{N}$ :
- $x_{2n} \equiv A^{n} \cdot x_{0} \pmod{p}$
- $y_{2n} \equiv A^{n} \cdot y_{0} \pmod{p}$

Si on note $x_{0}^{-1}$ l'inverse de $x_{0}$ dans $\mathbb(Z/pZ)$ on a alors $A^n \equiv x_{2n} \cdot x_{0}^{-1} \pmod{p}$

NB : $x_{0}^{-1}$ existe puisque `p` est premier

On peut maintenant se servir des principes arithmétiques utilisés dans RSA.

Soit $\phi(p)$ l'indicatrice d'Euler en `p`. Comme `p` est premier : $\phi(p) = p-1$.

Si $n$ et $\phi(p)$ sont premiers entre eux, alors (d'après le théorême de Bachet-Bezout) :

$$
\exists m, n \cdot m \equiv 1 \pmod{\phi(p)}
\Rightarrow
\exists u, n \cdot m = 1 + u \cdot \phi(p)
$$

$m$ permet alors de trouver $A$, grâce au petit théorême de Fermat :

$$
A^{p-1} \equiv 1 \pmod{p}
$$

donc :

$$
(A^{n})^{m} \equiv A^{n \cdot m} \equiv A^{1 + u \cdot \phi(p)} \equiv A \cdot (A^{\phi(p)})^{u}\equiv A \pmod{p}
$$

Or on dispose justement de `k2` (utilisé lors de la génération de la signature du message témoin) qui est pair. Il suffit de poser $n$ tel que $k2 = 2 \cdot n$ et ensuite vérifier que $n$ et $p-1$ soient bien premiers entre eux.

Ca tombe bien car c'est le cas :smile:

Après calcul, on obtient $A = 388070793197506567215490364778692980485$

A ce stade on connait donc $A = a^2 + b^2$.

Si on sait que le `k` utilisé pour la signature est pair, en posant $k = 2 \cdot n$, on est capable de retrouver le message à partir de sa signature, en testant toutes les valeurs possibles de `n` :
- $x_{0} \equiv (A^{n})^{-1} \cdot x_{2n} \pmod{p}$
- $y_{0} \equiv (A^{n})^{-1} \cdot y_{2n} \pmod{p}$

Le bon `n` devant donner un message intelligible.

----

### 3. Résolution pour `k` impair

Malheureusement la signature du flag a été réalisée avec un `k` impair que l'on peut noter $2 \cdot n + 1$.

En utilisant les différentes relations de récurrence, on obtient :
- $x_{2n+1} \equiv A^{n} \cdot (a \cdot x_{0} + b \cdot y_{0}) \pmod{p}$
- $y_{2n+1} \equiv A^{n} \cdot (b \cdot x_{0} - a \cdot y_{0}) \pmod{p}$

En résolvant le système pour les inconnues $x_{0}$ et $y_{0}$ ont obtient alors :
- $x_{0} \equiv A^{-1} \cdot (A^{n})^{-1} \cdot (a \cdot x_{2n+1} + b \cdot y_{2n+1}) \pmod{p}$
- $y_{0} \equiv A^{-1} \cdot (A^{n})^{-1} \cdot (b \cdot x_{2n+1} - a \cdot y_{2n+1}) \pmod{p}$

La connaissance de $A$ n'est donc pas suffisante, et il est nécessaire de retrouver $a$ et $b$.

----

### 4. Détermination de $a$ et $b$

Le [Théorême des 2 carrés de Fermat](https://fr.wikipedia.org/wiki/Th%C3%A9or%C3%A8me_des_deux_carr%C3%A9s_de_Fermat) nous apprend qu'il est possible de décomposer un nombre premier $p$ en somme de 2 carrés, et de façon unique, si celui-ci est de la forme $p=4\cdot n +1$ :

$$
p \equiv 1 \pmod{4}
\Rightarrow
\exists (u,v), u^2 + v^2 = p
$$

L'[identité de Diophante / Brahmagupta](https://fr.wikipedia.org/wiki/Identit%C3%A9_de_Brahmagupta) permet de transformer le produit de 2 sommes de 2 carrés, en 1 somme de 2 carrés :

$$
\forall a,b,c,d \in \mathbb{N}, (a^2 + b^2) \cdot (c^2 + d^2) = (ac - bd)^2 + (ad + bc)^2
$$


Si on applique cette identité au produit de 2 nombres premiers $p$ et $q$ décomposables chacun en somme de 2 carrés, on est capable d'en exprimer le produit en somme de 2 carrés :

$$
\begin{array}{ll}
p = u^2 + v^2
\\
q = x^2 + y^2
\\
\Rightarrow
p \cdot q = (u^2 + v^2) \cdot (x^2 + y^2) = (ux - vy)^2 + (uy + vx)^2
\end{array}
$$


Si on décompose $A$ en facteurs premiers (par exemple sur [factordb](http://factordb.com/)) on obtient :

$$
A = 3^2 \cdot 5 \cdot 17 \cdot 73 \cdot 853 \cdot 1193 \cdot 6828686706854717038620990997
$$

Tous les facteurs, hormis $3$, peuvent s'exprimer sous la forme $4 \cdot n +1$.

Si on pose $B$ tel que $A = 3^2 \cdot B$, on peut alors en appliquant successivement l'identité de Diophante / Brahmagupta, trouver $i$ et $j$ tel que : $B = i^2 + j^2$

Donc :

$$
A = 3^2 \cdot (i^2 + j^2) = (3i)^2 + (3j)^2
\Rightarrow
\left\lbrace
    \begin{array}{ll}
        a = 3 \cdot i
        \\
        b = 3 \cdot j
    \end{array}
\right.
$$

----

### 5. Considérations finales

Dans l'identité de Diophante / Brahmagupta, dans les 2 couples $(a,b)$ et $(c,d)$, chaque élément peut être interverti.

Ainsi, en prenant les différentes combinaisons, on obtient plusieurs couples $(a,b)$ possibles permettant d'avoir $A = a^2 + b^2$

De plus, ne connaissant pas le `k` utilisé pour la signature du flag, il suffit de tester tous les cas possibles. Donc avec $k = 2 \cdot n + 1$, il suffit de tester pour $\forall n \in \lbrace 2^{18}, 2^{18}+1, \ldots, 2^{19}-1 \rbrace$.

Parmi toutes les possibilités, le bon triplet $(a, b, n)$ doit permettre l'obtention d'un $x_{0}$ intelligible. Il suffit esnuite de les utiliser pour obtenir la 2ème partie $y_{0}$ du flag.

Le script [`LaSeine-reverse.py`](./LaSeine-reverse.py) implémente cette logique et permet ainsi de retrouver le flag `404CTF{F4u7_p4S_80iR3_l4_t4ss3...}`

Il s'appuie sur [`sq2.py`](./sq2.py) pour déterminer les 2 éléments constituant la somme des carrés d'un nombre premier.
