from myDes.infra import BitArray
from myDes.key_schedule import generate_des_round_keys

def initial_permutation(block: BitArray) -> BitArray:
    if(len(block) != 64):
        raise ValueError("Block must be 64 bits long")
    ip_table = [57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3, 61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7, 56, 48, 40, 32, 24, 16, 8, 0, 58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4, 62, 54, 46, 38, 30, 22, 14, 6]
    result = BitArray([0] * 64)
    for i in range(64):
        result[i] = block[ip_table[i]]
    return result

def final_permutation(block: BitArray) -> BitArray:
    if(len(block) != 64):
        raise ValueError("Block must be 64 bits long")
    fp_table = [39, 7, 47, 15, 55, 23, 63, 31, 38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29, 36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27, 34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25, 32, 0, 40, 8, 48, 16, 56, 24]
    result = BitArray([0] * 64)
    for i in range(64):
        result[i] = block[fp_table[i]]
    return result

# Expand 32 bits to 48 bits
def expansion_function(block: BitArray) -> BitArray:
    if(len(block) != 32):
        raise ValueError("Block must be 32 bits long")
    e_table = [31, 0, 1, 2, 3, 4, 3, 4, 5, 6, 7, 8, 7, 8, 9, 10, 11, 12, 11, 12, 13, 14, 15, 16, 15, 16, 17, 18, 19, 20, 19, 20, 21, 22, 23, 24, 23, 24, 25, 26, 27, 28, 27, 28, 29, 30, 31, 0]
    expanded_block = BitArray([0] * 48)
    for i in range(48):
        expanded_block[i] = block[e_table[i]]
    return expanded_block

# Rearrange bits according to the P table
def p_permutation(block: BitArray) -> BitArray:
    if(len(block) != 32):
        raise ValueError("Block must be 32 bits long")
    p_table = [15, 6, 19, 20, 28, 11, 27, 16, 0, 14, 22, 25, 4, 17, 30, 9, 1, 7, 23, 13, 31, 26, 2, 8, 18, 12, 29, 5, 21, 10, 3, 24]
    permuted_block = BitArray([0] * 32)
    for i in range(32):
        permuted_block[i] = block[p_table[i]]
    return permuted_block

def s_box_transform(input_bits: BitArray) -> BitArray:
    if len(input_bits) != 48:
        raise ValueError("Block must be 48 bits long")
    s_boxes = [
        [
            [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
            [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
            [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
            [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
        ],
        [
            [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
            [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
            [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
            [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
        ],
        [
            [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
            [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
            [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
            [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
        ],
        [
            [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
            [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
            [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
            [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
        ],
        [
            [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
            [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
            [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
            [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
        ],
        [
            [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
            [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
            [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
            [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
        ],
        [
            [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
            [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
            [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
            [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
        ],
        [
            [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
            [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
            [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
            [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
        ]
    ]
    output_bits = []
    for i in range(8):
        # Extract 6 bits for this S-box
        six_bits = input_bits[i*6:(i+1)*6]
        # Determine row and column
        row = (six_bits[0] << 1) | six_bits[5]
        col = (six_bits[1] << 3) | (six_bits[2] << 2) | (six_bits[3] << 1) | six_bits[4]
        # Get the S-box value
        s_box_value = s_boxes[i][row][col]
        # Convert the S-box value to 4 bits and append to output
        output_bits.extend([(s_box_value >> 3) & 1, (s_box_value >> 2) & 1, (s_box_value >> 1) & 1, s_box_value & 1])
    if len(output_bits) != 32:
        raise ValueError("Output must be 32 bits long")
    return BitArray(output_bits)


def des_f_function(right_half : BitArray, round_key: BitArray) -> BitArray:
    expanded_right = expansion_function(right_half)
    xor_with_key = expanded_right.xor_with(round_key)
    s_box_output = s_box_transform(xor_with_key)
    p_permuted_output = p_permutation(s_box_output)
    return p_permuted_output

def encrypt_block(block: BitArray, round_keys: list[BitArray], number_of_rounds: int = 16):
    if len(block) != 64:
        raise ValueError("Block must be 64 bits long")
    block = initial_permutation(block)
    left_half = block[:32]
    right_half = block[32:]
    for i in range(number_of_rounds):
        new_left_half = right_half
        new_right_half = left_half.xor_with(des_f_function(right_half, round_keys[i]))
        left_half = new_left_half
        right_half = new_right_half
    block = right_half + left_half
    return final_permutation(block)

def encrypt_block_one_round_only(block: BitArray, round_key: BitArray):
    if len(block) != 64:
        raise ValueError("Block must be 64 bits long")
    block = initial_permutation(block)
    left_0 = block[:32]
    right_0 = block[32:]

    left_1 = right_0
    right_1 = left_0.xor_with(des_f_function(right_0, round_key))

    block = right_1 + left_1
    return final_permutation(block)

def encrypt_block_two_rounds_only(block: BitArray, round_keys: list[BitArray]):
    if len(block) != 64:
        raise ValueError("Block must be 64 bits long")
    block = initial_permutation(block)
    left_0 = block[:32]
    right_0 = block[32:]

    left_1 = right_0
    right_1 = left_0.xor_with(des_f_function(right_0, round_keys[0]))

    # left_2 = right_1
    left_2  = left_0.xor_with(des_f_function(right_0, round_keys[0]))
    right_2 = left_1.xor_with(des_f_function(right_1, round_keys[1]))

    block = right_2 + left_2
    return final_permutation(block)
