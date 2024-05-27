from pwn import *
from json import loads
from zlib import decompress
from base64 import b64decode

'''
$ nc challenges.404ctf.fr 31777
Zut ! J'ai renversé mon sac à dos et tout est tombé par terre, vous pourriez mettre un peu d'ordre dans tout ça ?
eJw83buybUm....=
'''


host, port = "challenges.404ctf.fr", "31777"

def collect_data():
    p = remote(host, port)
    p.recvline()
    data = p.recvline()
    data = data.decode("utf-8")
    data = b64decode(data)
    data = decompress(data)
    data = data.decode("utf-8")
    p.close()
    return data

with open('collect.data', 'a') as data_file:
    n = 256-170
    pks0 = set()
    for _ in range(n):
        data = collect_data()
        data_file.write(data)
        data_file.write('\n')
        pk0 = loads(data)["public_key"][0]
        pks0.add(pk0)
    
    assert len(pks0) == n
