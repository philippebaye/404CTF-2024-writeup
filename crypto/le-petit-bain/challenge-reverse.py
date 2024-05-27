FLAG_beginning = "404CTF{tHe_c"

charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}_-!"
n = len(charset)

ENCRYPTED_FLAG = "C_ef8K8rT83JC8I0fOPiN6P!liE03W2NXFh1viJCROAqXb6o"


class Paire:
    def __init__(self, clear_char:str, encrypted_char:str) -> None:
        self.clear_char = charset.index(clear_char)
        self.encrypted_char = charset.index(encrypted_char)

def reverse_A_and_B(pair1:Paire, pair2:Paire):
    A = (pair1.encrypted_char - pair2.encrypted_char) * pow(pair1.clear_char - pair2.clear_char, -1, n)
    A %= n

    B = pair1.encrypted_char - A * pair1.clear_char
    B %= n
    return A, B


all_A, all_B = [], []
for i in range(len(FLAG_beginning) // 2):
    paire1 = Paire(FLAG_beginning[i], ENCRYPTED_FLAG[i])
    paire2 = Paire(FLAG_beginning[i+6], ENCRYPTED_FLAG[i+6])
    A, B = reverse_A_and_B(paire1, paire2)
    all_A.append(A)
    all_B.append(B)


def inv_f(a, b, n, x):
	return ((x-b)*pow(a, -1, n)) % n


def decrypt(encrypted_message, n):
    message = ""
    for i, char in enumerate(encrypted_message):
        x = charset.index(char)
        a, b = all_A[i%6], all_B[i%6]
        x = inv_f(a, b, n, x)
        message += charset[x]
    return message

MESSAGE = decrypt(ENCRYPTED_FLAG, n)
print(f"{MESSAGE=}")
