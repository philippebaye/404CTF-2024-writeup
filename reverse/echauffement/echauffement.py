secret = b'\x68\x5f\x66\x83\xa4\x87\xf0\xd1\xb6\xc1\xbc\xc5\x5c\xdd\xbe\xbd\x56\xc9\x54\xc9\xd4\xa9\x50\xcf\xd0\xa5\xce\x4b\xc8\xbd\x44\xbd\xaa\xd9'

message = ''.join([chr((secret[i] + i) // 2) for i in range(len(secret))])
print(message)
