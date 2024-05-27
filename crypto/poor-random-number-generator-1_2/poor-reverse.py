from encrypt import xor, get_blocks
from my_random import Generator


class MyGenerator(Generator):
	def __init__(self, flag_start, flag_start_enc):
		self.feed = [a ^ b for a, b in zip(flag_start, flag_start_enc)]


def decrypt(generator, data,block_size):
	decrypted = b''

	data_blocks = get_blocks(data,block_size)
	for block in data_blocks:
		rd = generator.get_random_bytes(block_size)
		xored = xor(block,rd)
		decrypted+= xored

	return decrypted


if __name__ == "__main__":
    BLOCK_SIZE = 4

    flag_part = open("flag.png.part",'rb').read()
    flag_start = flag_part[:2000]
    flag_enc = open("flag.png.enc",'rb').read()

    generator = MyGenerator(flag_start, flag_enc[:2000])
    flag_end = decrypt(generator, flag_enc[2000:], BLOCK_SIZE)

    with open('flag.png', 'wb') as flag_file:
        flag_file.write(flag_start)
        flag_file.write(flag_end)
