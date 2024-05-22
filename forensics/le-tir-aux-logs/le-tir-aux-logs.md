# Le tir aux logs

<img alt="énoncé du challenge" src="enonce.png" width=500>

----

L'analyse des logs montre que les tentavives de connexion correspondent aux appels des URL de la forme :

```http
GET /index.php?username={{username}}&password={{password}}
```

Quand les éléments d'authentification (i.e. `{{username}}` et `{{password}}`) sont corrects, une redirection (i.e. code HTTP `302`) est réalisée vers l'URL qui apparait ensuite (i.e. `/admin.php`).

Quand cela n'est pas le cas, un code HTTP `200` est émis, et une nouvelle tentative d'accès est réalisée.

Pour la plupart des IP, la connexion est établie lors de la première tentative, voire lors de la seconde.

Cependant pour l'IP `146.70.147.101` il y a plusieurs tentatives avec ce qui ressemble à des tentatives d'injection SQL. Parmi toutes les tentatives, celles-ci `/index.php?username=admin%27%23&password=test` est en succès.

Dans les logs, on trouve également ce qui semble être la trace du header `Referer` permet d'avoir le protocole et le nom du site concerné : `http://www.inscription_tir_arc.com`

Le flag est donc `404CTF{http://www.inscription_tir_arc.com/index.php?username=admin%27%23&password=test}`
