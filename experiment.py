from myDes import *
from pyDes.core import encode_block

PLAINTEXT = b"testtest"
PASSWORD = b"password"

round_keys = generate_des_round_keys(BitArray(PASSWORD))
block = BitArray(PLAINTEXT)

block = initial_permutation(block)
left_0 = block[:32]
right_0 = block[32:]
left_1 = right_0
right_1 = left_0.xor_with(des_f_function(right_0, round_keys[0]))
left_2  = left_0.xor_with(des_f_function(right_0, round_keys[0]))
right_2 = left_1.xor_with(des_f_function(right_1, round_keys[1]))
block = right_2 + left_2
block_before_final_permutation = block
block = final_permutation(block)

pyDes_block = int.from_bytes(PLAINTEXT, "big")
pyDes_round_keys = []
for round_key in round_keys:
    pyDes_round_keys.append(int.from_bytes(round_key.to_bytes()))
pyDes_encrypted_block = encode_block(pyDes_block, pyDes_round_keys, True, 2)

assert block.to_bytes() == pyDes_encrypted_block.to_bytes(8, "big")

block = initial_permutation(block)
assert block == block_before_final_permutation
right_2_2 = block[:32]
left_2_2 = block[32:]
assert right_2_2 == right_2
assert left_2_2 == left_2