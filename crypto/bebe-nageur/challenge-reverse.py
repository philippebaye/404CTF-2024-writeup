from collections import Counter

charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}_-!"

def f(a,b,n,x):
	return (a*x+b)%n

def encrypt(message,a,b,n):
	encrypted = ""
	for char in message:
		x = charset.index(char)
		x = f(a,b,n,x)
		encrypted += charset[x]

	return encrypted

n = len(charset)
#a = rd.randint(2,n-1)
#b = rd.randint(1,n-1)

#print(encrypt(FLAG,a,b,n))

ENCRYPTED_FLAG = "-4-c57T5fUq9UdO0lOqiMqS4Hy0lqM4ekq-0vqwiNoqzUq5O9tyYoUq2_"

index_4 = charset.index('4')
index_0 = charset.index('0')
index_tiret = charset.index('-')
print(index_4, index_0, index_tiret)

'''
n = 67

(1) a*56 + b = 65 % n
(2) a*52 + b = 56 % n

(1) - (2)
=> a*(56-52) = (65-56) %n
=> a*4 = 9 % n

pow(4, -1, 67) = 17
=> 17*4 = 1 %n
=> 9*(17*4) = 1 %n
=> a = 9*17 % n
=> a = 19

en remplacant a par sa valeur dans (1) :
=> 19*56 + b = 65 % n
=> b = 65 - 19*56 %n
=> b = 6
'''

def inv_f(a,b,n,x):
	return ((x-b)*pow(a, -1, n)) % n

def decrypt(encrypted_message,a,b,n):
	message = ""
	for char in encrypted_message:
		x = charset.index(char)
		x = inv_f(a,b,n,x)
		message += charset[x]

	return message

MESSAGE = decrypt(ENCRYPTED_FLAG, 19, 6, n)
print(f"{MESSAGE=}")
