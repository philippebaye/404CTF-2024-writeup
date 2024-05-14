import numpy as np

channel_1 = open('channel_1', 'r').read()
channel_2 = open('channel_2', 'r').read()
channel_3 = open('channel_3', 'r').read()
channel_4 = open('channel_4', 'r').read()
channel_5 = open('channel_5', 'r').read()
channel_6 = open('channel_6', 'r').read()
channel_7 = open('channel_7', 'r').read()
channel_8 = open('channel_8', 'r').read()

assert len(channel_1) == len(channel_2) == len(channel_3) == len(channel_4) == len(channel_5) == len(channel_6) == len(channel_7) == len(channel_8)


data = []
for i in range(len(channel_1)):
    d1, d2, d3, d5, d6, d7, d8 = int(channel_1[i]), int(channel_2[i]), int(channel_3[i]), int(channel_5[i]), int(channel_6[i]), int(channel_7[i]), int(channel_8[i])
    if sum([d1, d2, d3, d5, d6, d7]) % 2 == d8:
        d4 = 0
    else:
        d4 = 1
    data += [d1, d2, d3, d4, d5, d6, d7]

with open('flag.png', 'wb') as flag:
    for i in range(0, len(data), 8):
        bits = np.packbits(data[i:i+8])
        flag.write(bits)
