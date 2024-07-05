def bytearray_to_bits(byte_array):
    bit_list = []
    for byte in byte_array:
        for i in range(8):
            bit_list.append((byte >> (7 - i)) & 1)
    return bit_list

def bits_to_bytearray(bit_list):
    byte_array = bytearray()
    for i in range(0, len(bit_list), 8):
        byte = 0
        for bit in bit_list[i:i+8]:
            byte = (byte << 1) | bit
        byte_array.append(byte)
    return bytes(byte_array)

def initial_permutation(block):
    ip_table = [57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3, 61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7, 56, 48, 40, 32, 24, 16, 8, 0, 58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4, 62, 54, 46, 38, 30, 22, 14, 6]
    result = [0] * 64
    for i in range(64):
        result[i] = block[ip_table[i]]
    return result

plain = open('plain.txt', 'rb').read()

all_left = []
all_right = []

for i in range(0, len(plain), 8):
    block = plain[i:i+8]
    if len(block) < 8:
        break
    block_bits = bytearray_to_bits(bytearray(block))
    permuted_block = initial_permutation(block_bits)
    left = permuted_block[:32]
    right = permuted_block[32:]
    left = bits_to_bytearray(left)
    right = bits_to_bytearray(right)
    all_left.append(left)
    all_right.append(right)

print(len(all_left), len(set(all_left)))
print("----")
print(len(all_right), len(set(all_right)))
