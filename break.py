from myDes import des_f_function, BitArray, initial_permutation, final_permutation
import time

cipher = open("cipher.txt", "rb").read()
plain = open("plain.txt", "rb").read()
plain_0 = BitArray(plain[:8])
cipher_0 = BitArray(cipher[:8])

cipher_0_before_final_permutation = initial_permutation(cipher_0)
cipher_right_2 = cipher_0_before_final_permutation[:32]
cipher_left_2 = cipher_0_before_final_permutation[32:]
plain_0 = initial_permutation(plain_0)
left_0 = plain_0[:32]
right_0 = plain_0[32:]

possible_round_keys = []

start_time = time.time()

for current_round_key in range(2**48):
    if(current_round_key % 2**22 == 0 and current_round_key != 0):
        print(f"Current round key: {current_round_key}, Time elapsed: {time.time() - start_time} seconds")
        rate = current_round_key / (time.time() - start_time)  # keys per second
        total_work = 2**48  # Total keys to try
        work_done = current_round_key  # Keys tried so far
        remaining_work = total_work - work_done  # Keys left to try
        remaining_time_seconds = remaining_work / rate  # Time left in seconds
        remaining_hours = remaining_time_seconds / 3600  # Time left in hours
        print(f"Expected time remaining: {remaining_hours} hours")
        print(f"Found {len(possible_round_keys)} possible round keys")
        print(f"Percentage: {current_round_key / 2**48 * 100}%")
    round_key = current_round_key.to_bytes(6, 'big')
    round_key = BitArray(round_key)
    left_2  = left_0.xor_with(des_f_function(right_0, round_key))
    if(left_2 == cipher_left_2):
        possible_round_keys.append(round_key)

print(possible_round_keys, len(possible_round_keys))