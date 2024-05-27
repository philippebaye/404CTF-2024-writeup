from challenge2 import Bob
from Crypto.Util.number import long_to_bytes


# ================================================
# Find cycles in perm
# ================================================
def find_cycles_in_perm():
    perm = [65, 107, 53, 90, 67, 35, 17, 100, 37, 103, 41, 92, 23, 120, 70, 11, 34, 73, 16, 29, 7, 91, 127, 69, 81, 26, 0, 98, 71, 51, 9, 112, 64, 121, 101, 47, 114, 30, 104, 113, 3, 27, 6, 32, 42, 93, 48, 21, 118, 99, 89, 84, 36, 110, 25, 102, 61, 39, 86, 50, 14, 10, 56, 28, 38, 62, 22, 46, 66, 19, 108, 18, 13, 125, 49, 2, 74, 95, 8, 122, 58, 5, 75, 97, 15, 63, 117, 123, 96, 24, 94, 43, 4, 33, 115, 45, 76, 80, 126, 109, 52, 12, 79, 72, 54, 77, 31, 57, 1, 87, 88, 60, 20, 55, 40, 111, 116, 44, 82, 85, 68, 105, 106, 83, 78, 124, 59, 119]

    cycles = []

    def is_already_in_cycle(i):
        for cycle in cycles:
            if i in cycle:
                return True
        return False

    for i in range(len(perm)):
        if is_already_in_cycle(i):
            continue

        j = i
        new_cycle = [i]
        while (j := perm[j]) != i:
            new_cycle.append(j)
        cycles.append(new_cycle)
    
    return cycles

cycles = find_cycles_in_perm()
[print(cycle) for cycle in cycles]


# ================================================
# Bob's friend
# ================================================
class Patrick(Bob):
    def __init__(self, data):
        Bob.__init__(self, data)
        self.sav_data = self.data

    def _inverse_f(self, state):
        perm = [65, 107, 53, 90, 67, 35, 17, 100, 37, 103, 41, 92, 23, 120, 70, 11, 34, 73, 16, 29, 7, 91, 127, 69, 81, 26, 0, 98, 71, 51, 9, 112, 64, 121, 101, 47, 114, 30, 104, 113, 3, 27, 6, 32, 42, 93, 48, 21, 118, 99, 89, 84, 36, 110, 25, 102, 61, 39, 86, 50, 14, 10, 56, 28, 38, 62, 22, 46, 66, 19, 108, 18, 13, 125, 49, 2, 74, 95, 8, 122, 58, 5, 75, 97, 15, 63, 117, 123, 96, 24, 94, 43, 4, 33, 115, 45, 76, 80, 126, 109, 52, 12, 79, 72, 54, 77, 31, 57, 1, 87, 88, 60, 20, 55, 40, 111, 116, 44, 82, 85, 68, 105, 106, 83, 78, 124, 59, 119]
        #print('bob state', state)
        input_perm = state[0].copy()+state[1].copy()
        output_perm = [input_perm[perm.index(perm.index(i))] for i in perm]
        #output_perm = [output_perm[:self.R_size],output_perm[self.R_size:]]
        return output_perm
    
    def state_before_last_absorb(self):
        self._absorb()
        return self._inverse_f(self.state)

# ====================================
# Input data
# ====================================
data = long_to_bytes(0x749bfdedfb96f03b650a7b96f38c6fc2)
bob_hash = Bob(data).hexdigest()
print(data)

# ====================================
# Anayse
# ====================================
patrick = Patrick(data)
state_before_last_absorb = patrick.state_before_last_absorb()
print(f'{state_before_last_absorb=}')

# ====================================
# Find other Bob
# ====================================
fake_data = data + b'\x00'
fake_patrick = Patrick(fake_data)
fake_state_before_last_absorb = fake_patrick.state_before_last_absorb()
print(f'{fake_state_before_last_absorb=}')


# ====================================
# Adjust fake_data
# ====================================
def find_index_data_to_change(i):
    def find_cycle(i):
        for cycle in cycles:
            if i in cycle:
                return cycle

    if i < 16:
        return 4*32+i
    
    cycle = find_cycle(i)
    i_index_in_cyle = cycle.index(i)
    next_i = cycle[i_index_in_cyle+1]
    if next_i < 32:
        return 3*32+next_i
    next_i = cycle[i_index_in_cyle+2]
    if next_i < 32:
        return 2*32+next_i
    next_i = cycle[i_index_in_cyle+3]
    if next_i < 32:
        return 1*32+next_i
    next_i = cycle[i_index_in_cyle+4]
    if next_i > 31:
        print("aie")
    return next_i


new_data = fake_patrick.sav_data.copy()
for i, (b1, b2) in enumerate(zip(state_before_last_absorb, fake_state_before_last_absorb)):
    if b1 != b2:
        f_index = find_index_data_to_change(i)
        print(i, state_before_last_absorb[i], fake_state_before_last_absorb[i], f_index, fake_patrick.sav_data[f_index])
        new_data[f_index] ^= 1

# ====================================
# Display good fake_data
# ====================================
d4 = fake_patrick.binArray2bytes(new_data)
print(d4[-1])
print(d4[:-1])
while d4[-1] == 0:
    d4 = d4[:-1]

d4 = d4[1:-1]
print(d4)
print(f'fake_data : {d4.hex()}')
