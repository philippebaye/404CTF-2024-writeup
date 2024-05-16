from Crypto.Util.number import bytes_to_long

with open('chall.bin', 'rb') as file_bin:
    raw_data = file_bin.read()
    bin_data = ''
    for d in raw_data:
        bin_data += "{:08b}".format(d)
    print(bin_data)
    open('decode.bin', 'w').write(bin_data)

    started = False
    num = 0
    data = ''
    bloc = ''
    for i, b in enumerate(bin_data):
        if not started:
            if b == '0':
                started = True
                bloc = ''
                num = 0
        else:
            num += 1
            if num <= 7:
                bloc += b
            elif num == 8:
                parity = 0
                for b_elt in bloc:
                    parity ^= int(b_elt)
                if (int(b) != parity):
                    print("parity", i, b, parity)
                    print(bloc)
                    quit()
            elif num == 9:
                if b != '1':
                    print("bug", b)
                    quit()
                else:
                    started = False
                    data += bloc
    print(len(data))
    print(data)

        
for i in range(0, len(data), 7):
    by = int(data[i:i+7][::-1], 2)
    print(chr(by), end='')
print()