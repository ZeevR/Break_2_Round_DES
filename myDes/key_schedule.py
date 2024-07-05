from myDes.infra import *

def generate_des_round_keys(password_bits: BitArray) -> list[BitArray]:
    if len(password_bits) != 64:
        raise ValueError("Key must be 64 bits long")
    # PC-1 Permutation Table
    PC1 = [
        56, 48, 40, 32, 24, 16, 8,
        0, 57, 49, 41, 33, 25, 17,
        9, 1, 58, 50, 42, 34, 26,
        18, 10, 2, 59, 51, 43, 35,
        62, 54, 46, 38, 30, 22, 14,
        6, 61, 53, 45, 37, 29, 21,
        13, 5, 60, 52, 44, 36, 28,
        20, 12, 4, 27, 19, 11, 3,
    ]
    # PC-2 Permutation Table
    PC2 = [
        13, 16, 10, 23, 0, 4, 2, 27, 14, 5, 20, 9,
        22, 18, 11, 3, 25, 7, 15, 6, 26, 19, 12, 1,
        40, 51, 30, 36, 46, 54, 29, 39, 50, 44, 32, 47,
        43, 48, 38, 55, 33, 52, 45, 41, 49, 35, 28, 31
    ]
    # Shifts for each round
    shifts = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

    pc1_key = BitArray([0] * 56)
    for i in range(len(PC1)):
        pc1_key[i] = password_bits[PC1[i]]

    left = BitArray(pc1_key[:28])
    right = BitArray(pc1_key[28:])

    round_keys = []

    for round_shift in shifts:
        left = left.circular_left_shift(round_shift)
        right = right.circular_left_shift(round_shift)
        combined_key = left + right
        round_key = BitArray([0] * 48)
        for i in range(len(PC2)):
            round_key[i] = combined_key[PC2[i]]
        round_keys.append(round_key)

    return round_keys