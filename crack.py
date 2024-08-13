from myDes import *
import itertools

def inverse_permutation(permutation):
    n = len(permutation)
    inverse_perm = [0] * n
    for i in range(n):
        inverse_perm[permutation[i]] = i
    return inverse_perm

def apply_permutation(block, permutation_table):
    if(len(block) != len(permutation_table)):
        raise ValueError("Block and permutation table must have the same length")
    permuted_block = BitArray([0] * len(block))
    for i in range(len(block)):
        permuted_block[i] = block[permutation_table[i]]
    return permuted_block

F_FUNCTION_P_TABLE = [15, 6, 19, 20, 28, 11, 27, 16, 0, 14, 22, 25, 4, 17, 30, 9, 1, 7, 23, 13, 31, 26, 2, 8, 18, 12, 29, 5, 21, 10, 3, 24]
INVERSE_F_FUNCTION_P_TABLE = inverse_permutation(F_FUNCTION_P_TABLE)

def s_box_transform(input_data : BitArray, s_box_number) -> BitArray:
    if(len(input_data) != 6):
        raise ValueError("Input data must be 6 bits long")
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
    row = (input_data[0] << 1) | input_data[5]
    col = (input_data[1] << 3) | (input_data[2] << 2) | (input_data[3] << 1) | input_data[4]
    # Get the S-box value
    s_box_value = s_boxes[s_box_number][row][col]
    # Convert the S-box value to 4 bits and append to output
    output = BitArray([(s_box_value >> 3) & 1, (s_box_value >> 2) & 1, (s_box_value >> 1) & 1, s_box_value & 1])
    return output


# Generate all the s-box inputs that would produce the given s-box output
# Remember all the s-boxes are used in a single round and not like you would expect a different s-box for each round
def bruteforce_s_box_input(s_box_output: BitArray) -> list[BitArray]:
    all_s_box_results = []
    # Iterate over all s-boxes
    for current_s_box in range(8):
        # Let's focus on a single s-box, put it's value in current_s_box_partial_output
        current_s_box_partial_output = s_box_output[current_s_box * 4: (current_s_box + 1) * 4]
        current_s_box_results = []
        # current_s_box_guess is the possible input of the s-box
        for current_s_box_guess in range(64):
            # 64 values only need 6 bits
            current_guess = BitArray(current_s_box_guess.to_bytes(1, "big"))[2:8]
            # Does the current guess give the correct output?
            if(s_box_transform(current_guess, current_s_box) == current_s_box_partial_output):
                # Save the current guess
                current_s_box_results.append(current_guess)
        # Group all the guesses in lists, one list for each s-box
        all_s_box_results.append(current_s_box_results)
    all_combined_guesses = []
    for current_s_box_1_guess in itertools.product(all_s_box_results[0],
                                               all_s_box_results[1],
                                               all_s_box_results[2],
                                               all_s_box_results[3],
                                               all_s_box_results[4],
                                               all_s_box_results[5],
                                               all_s_box_results[6],
                                               all_s_box_results[7]):
        combined_guess = BitArray(current_s_box_1_guess[0] + current_s_box_1_guess[1] + current_s_box_1_guess[2] + current_s_box_1_guess[3] + current_s_box_1_guess[4] + current_s_box_1_guess[5] + current_s_box_1_guess[6] + current_s_box_1_guess[7])
        all_combined_guesses.append(combined_guess)
    return all_combined_guesses

def generate_round_key_0_guesses(plain_block: BitArray, cipher_block: BitArray) -> list[BitArray]:
    # We want to bruteforce the s-box input then we will xor it with the expanded_plain_right_0 to get the round_key_0 guess
    # We need to do 2 things:
    # 1. Get the expanded_plain_right_0
    # 2. Get the s-box input
    # To get the s-box input we need to roll the cipher back up to the point where we have the output of all the s-boxes then brute force the input
    # Once we have the round key guess we cant try to encrypt another block and see if it matches the cipher block

    # Get expanded_plain_right_0 by rolling the cipher forward from plain_0
    plain_block = initial_permutation(plain_block)
    plain_left_0 = plain_block[:32]
    plain_right_0 = plain_block[32:]
    # This happens inside the f_function
    expanded_plain_right_0  = expansion_function(plain_right_0)
    # The next step in the encryption flow is to xor the expanded_plain_right_0 with the round key and feed it to the s-boxes
    # We will stop here and use this part of the xor to calculate the round key guess once we have the result of the xor operation

    # Get the s-box input by rolling the cipher back
    # encrypted_left_2 (before the final swap) which is what we get in the cipher (after the final swap) is actually the result of just encrypting the first right block fully
    # Fully encrypting the right block means feeding the plain to the f_function and xoring the result with the left block

    # Reverse the final permutation
    cipher_block = initial_permutation(cipher_block)
    cipher_left_2 = cipher_block[:32]
    cipher_right_2 = cipher_block[32:]
    # Reverse final swap
    cipher_left_2, cipher_right_2 = cipher_right_2, cipher_left_2
    # Cipher_right_1 is actually just a copy of cipher_left_2
    cipher_right_1 = cipher_left_2
    # cipher_right_1 is the result of a xor of output of the f_function and the left block
    # so the output of the f_function can be calculated by xoring the cipher_right_1 with the left block (plain)
    f_function_result_1  = cipher_right_1.xor_with(plain_left_0)
    # Now lets roll back the inside of the f_function until we get the s-box input
    # First we need to reverse the p_permutation that's at the end of the f_function
    s_box_1_output = apply_permutation(f_function_result_1, INVERSE_F_FUNCTION_P_TABLE)
    # Now we have the output of the s-boxes, we can bruteforce the input
    s_box_1_input_guesses = bruteforce_s_box_input(s_box_1_output)
    # Let's generate the round key guesses by xoring the expanded_plain_right_0 with the s-box input guesses
    all_round_key_guesses = []
    for current_s_box_input_guess in s_box_1_input_guesses:
        round_key_guess = current_s_box_input_guess.xor_with(expanded_plain_right_0)
        all_round_key_guesses.append(round_key_guess)
    return all_round_key_guesses

def generate_round_key_1_guesses(plain_block: BitArray, cipher_block: BitArray) -> list[BitArray]:
    # cipher_right_2 is just the f_function(cipher_left_2) xor plain_right_0
    # Forward
    plain_block = initial_permutation(plain_block)
    plain_left_0 = plain_block[:32]
    plain_right_0 = plain_block[32:]
    plain_left_1 = plain_right_0
    # Backward
    # Reverse the final permutation
    cipher_block = initial_permutation(cipher_block)
    cipher_left_2 = cipher_block[:32]
    cipher_right_2 = cipher_block[32:]
    # Reverse final swap
    cipher_left_2, cipher_right_2 = cipher_right_2, cipher_left_2
    # cipher_right_1 is actually just a copy of cipher_left_2
    # cipher_right_1 is the input of the f_function
    cipher_right_1 = cipher_left_2
    # cipher_right_2 is the xor of the f_function output and plain_left_1
    # so the output of the f_function is the xor of cipher_right_2 and plain_left_1
    f_function_result_2 = cipher_right_2.xor_with(plain_left_1)
    # lets roll back the inside of the f_function
    s_box_2_output = apply_permutation(f_function_result_2, INVERSE_F_FUNCTION_P_TABLE)
    # Now we have the output of the s-boxes, we can bruteforce the input
    s_box_2_input_guesses = bruteforce_s_box_input(s_box_2_output)
    # Since cipher_right_1 is the input of the f_function we can calculate the expanded value
    expanded_cipher_right_1 = expansion_function(cipher_right_1)
    all_round_key_guesses = []
    for current_s_box_input_guess in s_box_2_input_guesses:
        round_key_guess = current_s_box_input_guess.xor_with(expanded_cipher_right_1)
        all_round_key_guesses.append(round_key_guess)
    return all_round_key_guesses

def main():
    cipher = open("cipher.txt","r").read()
    cipher = bytes.fromhex(cipher)
    if(len(cipher)%8!=0):
        print("Invalid cipher length")
        exit()
    number_of_cipher_blocks = len(cipher)//8
    plain = open("plain.txt","rb").read()
    # Only full blocks are considered
    number_of_plain_blocks = len(plain)//8
    # Generate plain and cipher pairs
    plain_cipher_pairs = []
    for current_block_number in range(number_of_plain_blocks):
        current_plain = BitArray(plain[current_block_number*8:current_block_number*8+8])
        current_cipher = BitArray(cipher[current_block_number*8:current_block_number*8+8])
        plain_cipher_pairs.append((current_plain, current_cipher))
    for current_pair in plain_cipher_pairs:
        print(current_pair[0].to_bytes(), current_pair[1].to_bytes())
    # Generate round key 0 guesses
    round_0_key_guesses = set(generate_round_key_0_guesses(plain_cipher_pairs[0][0], plain_cipher_pairs[0][1]))
    round_1_key_guesses = set(generate_round_key_1_guesses(plain_cipher_pairs[0][0], plain_cipher_pairs[0][1]))

    new_guesses = set(generate_round_key_0_guesses(plain_cipher_pairs[1][0], plain_cipher_pairs[1][1]))
    common_round_key_0_guesses = round_0_key_guesses.intersection(new_guesses)
    print("Number of common round key 0 guesses:", len(common_round_key_0_guesses))
    for current_plain_cipher_pair in plain_cipher_pairs[1:]:
        current_guesses = generate_round_key_0_guesses(current_plain_cipher_pair[0], current_plain_cipher_pair[1])
        common_round_key_0_guesses = common_round_key_0_guesses.intersection(current_guesses)
        print("Number of common round key 0 guesses:", len(common_round_key_0_guesses))

    new_guesses = set(generate_round_key_1_guesses(plain_cipher_pairs[1][0], plain_cipher_pairs[1][1]))
    common_round_key_1_guesses = round_1_key_guesses.intersection(new_guesses)
    print("Number of common round key 1 guesses:", len(common_round_key_1_guesses))
    for current_plain_cipher_pair in plain_cipher_pairs[1:]:
        current_guesses = generate_round_key_1_guesses(current_plain_cipher_pair[0], current_plain_cipher_pair[1])
        common_round_key_1_guesses = common_round_key_1_guesses.intersection(current_guesses)
        print("Number of common round key 1 guesses:", len(common_round_key_1_guesses))

    good_keys = []
    for current_key_pair_guess in itertools.product(common_round_key_0_guesses, common_round_key_1_guesses):
        for current_plain_cipher_pair in plain_cipher_pairs:
            encrypted_block = encrypt_block_two_rounds_only(current_plain_cipher_pair[0], current_key_pair_guess)
            if(encrypted_block != current_plain_cipher_pair[1]):
                break
        # This is ugly but I'm tired
        else:
            # Swap the keys for decryption
            good_keys.append((current_key_pair_guess[1], current_key_pair_guess[0]))
            print("Key pair found:", current_key_pair_guess[0].to_bytes(), current_key_pair_guess[1].to_bytes())

    for current_key_pair_guess in good_keys:
        decrypted_string = b""
        for current_cipher_block_number in range(number_of_cipher_blocks):
            current_cipher_block = BitArray(cipher[current_cipher_block_number*8:current_cipher_block_number*8+8])
            decrypted_block = encrypt_block_two_rounds_only(current_cipher_block, current_key_pair_guess)
            decrypted_string += decrypted_block.to_bytes()
        print(decrypted_string)

if __name__ == "__main__":
    main()