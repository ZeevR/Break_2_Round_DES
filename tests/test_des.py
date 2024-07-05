import struct
import pytest
from myDes.infra import BitArray
from myDes.key_schedule import generate_des_round_keys
from myDes.des import initial_permutation, final_permutation, expansion_function, p_permutation, s_box_transform, des_f_function, encrypt_block, encrypt_block_one_round_only, encrypt_block_two_rounds_only
from pyDes.core import INITIAL_PERMUTATION, INVERSE_PERMUTATION, EXPANSION, PERMUTATION, SUBSTITUTION_BOX,permute, f, encode_block

@pytest.mark.parametrize("block", [b"12345678", b"abcdefgh", b"!@#$%^&*"])
def test_initial_permutation(block):
    myDes_block = BitArray(block)
    pyDes_block = struct.unpack(">Q", block)[0]
    myDes_permuted_block = initial_permutation(myDes_block)
    pyDes_permuted_block = permute(pyDes_block, 64, INITIAL_PERMUTATION)
    assert myDes_permuted_block.to_bytes() == pyDes_permuted_block.to_bytes(8, "big")

@pytest.mark.parametrize("block", [b"12345678", b"abcdefgh", b"!@#$%^&*"])
def test_final_permutation(block):
    myDes_block = BitArray(block)
    pyDes_block = struct.unpack(">Q", block)[0]
    myDes_permuted_block = final_permutation(myDes_block)
    pyDes_permuted_block = permute(pyDes_block, 64, INVERSE_PERMUTATION)
    assert myDes_permuted_block.to_bytes() == pyDes_permuted_block.to_bytes(8, "big")


@pytest.mark.parametrize("block", [b"1234", b"abcd", b"!@#$"])
def test_expansion(block):
    myDes_block = BitArray(block)
    pyDes_block, = struct.unpack(">L", block)
    myDes_permuted_block = expansion_function(myDes_block)
    pyDes_permuted_block = permute(pyDes_block, 32, EXPANSION)
    assert myDes_permuted_block.to_bytes() == pyDes_permuted_block.to_bytes(48//8, "big")

@pytest.mark.parametrize("block", [b"1234", b"abcd", b"!@#$"])
def test_ppermuation(block):
    myDes_block = BitArray(block)
    pyDes_block, = struct.unpack(">L", block)
    myDes_permuted_block = p_permutation(myDes_block)
    pyDes_permuted_block = permute(pyDes_block, 32, PERMUTATION)
    assert myDes_permuted_block.to_bytes() == pyDes_permuted_block.to_bytes(32//8, "big")

@pytest.mark.parametrize("block", [b"123456", b"abcdef", b"!@#$%^"])
def test_s_box_transform(block):
    myDes_block = BitArray(block)
    pyDes_block = int.from_bytes(block, "big")
    myDes_transformed_block = s_box_transform(myDes_block)
    pyDes_transformed_block = 0
    for i, box in enumerate(SUBSTITUTION_BOX):
        i6 = pyDes_block >> 42 - i * 6 & 0x3f
        pyDes_transformed_block = pyDes_transformed_block << 4 | box[i6 & 0x20 | (i6 & 0x01) << 4 | (i6 & 0x1e) >> 1]
    print(myDes_transformed_block.to_bytes(), pyDes_transformed_block)
    assert myDes_transformed_block.to_bytes() == pyDes_transformed_block.to_bytes(4, "big")

@pytest.mark.parametrize("block", [b"123456", b"abcdef", b"!@#$%^"])
def test_s_box_and_p_permutation(block):
    myDes_block = BitArray(block)
    pyDes_block = int.from_bytes(block, "big")
    myDes_transformed_block = s_box_transform(myDes_block)
    myDes_transformed_and_permuted_block = p_permutation(myDes_transformed_block)
    pyDes_transformed_block = 0
    for i, box in enumerate(SUBSTITUTION_BOX):
        i6 = pyDes_block >> 42 - i * 6 & 0x3f
        pyDes_transformed_block = pyDes_transformed_block << 4 | box[i6 & 0x20 | (i6 & 0x01) << 4 | (i6 & 0x1e) >> 1]
    pyDes_transformed_and_permuted_block = permute(pyDes_transformed_block, 32, PERMUTATION)
    assert myDes_transformed_and_permuted_block.to_bytes() == pyDes_transformed_and_permuted_block.to_bytes(4, "big")

@pytest.mark.parametrize("block, key", [(b"1234", b"abcdef"), (b"!@#$", b"123456"), (b"abcd", b"!@#$%^")])
def test_des_f_function(block, key):
    myDes_block = BitArray(block)
    myDes_key = BitArray(key)
    pyDes_block = int.from_bytes(block, "big")
    pyDes_key = int.from_bytes(key, "big")
    myDes_result = des_f_function(myDes_block, myDes_key)
    pyDes_result = f(pyDes_block, pyDes_key)
    assert myDes_result.to_bytes() == pyDes_result.to_bytes(32//8, "big")

@pytest.mark.parametrize("block, round_keys, number_of_rounds", [
    (b"12345678", [b"key1__"], 1),
    (b"abcdefgh", [b"key2__", b"key3__", b"key4__"], 3),
    (b"secret12", [b"k1____", b"k2____", b"k3____", b"k4____", b"k5____", b"k6____", b"k7____", b"k8____", b"k9____", b"k10___", b"k11___", b"k12___", b"k13___", b"k14___", b"k15___", b"k16___"], 16),
])
def test_encrypt_block(block, round_keys, number_of_rounds):
    myDes_block = BitArray(block)
    myDes_round_keys = [BitArray(key) for key in round_keys]
    encrypted_block = encrypt_block(myDes_block, myDes_round_keys, number_of_rounds)
    pyDes_block = int.from_bytes(block, "big")
    pyDes_round_keys = [int.from_bytes(key, "big") for key in round_keys]
    pyDes_encrypted_block = encode_block(pyDes_block, pyDes_round_keys, True, number_of_rounds)
    assert encrypted_block.to_bytes() == pyDes_encrypted_block.to_bytes(8, "big")


@pytest.mark.parametrize("block, round_key", [
    (b"12345678", b"key1__"),
    (b"abcdefgh", b"key2__"),
    (b"secret12", b"k1____"),
])
def test_encrypt_block_only_1_round(block, round_key):
    myDes_block = BitArray(block)
    myDes_round_keys = BitArray(round_key)
    myDes_encrypted_block = encrypt_block_one_round_only(myDes_block, myDes_round_keys)
    pyDes_block = int.from_bytes(block, "big")
    pyDes_round_keys = [int.from_bytes(round_key, "big")]
    pyDes_encrypted_block = encode_block(pyDes_block, pyDes_round_keys, True, 1)
    assert myDes_encrypted_block.to_bytes() == pyDes_encrypted_block.to_bytes(8, "big")

@pytest.mark.parametrize("block, round_key1, round_key2", [
    (b"12345678", b"key1__", b"key2__"),
    (b"abcdefgh", b"key3__", b"key4__"),
    (b"secret12", b"k1____", b"k2____"),
])
def test_encrypt_block_only_2_rounds(block, round_key1, round_key2):
    myDes_block = BitArray(block)
    myDes_round_keys = [BitArray(round_key1), BitArray(round_key2)]
    myDes_encrypted_block = encrypt_block_two_rounds_only(myDes_block, myDes_round_keys)
    pyDes_block = int.from_bytes(block, "big")
    pyDes_round_keys = [int.from_bytes(round_key1, "big"), int.from_bytes(round_key2, "big")]
    pyDes_encrypted_block = encode_block(pyDes_block, pyDes_round_keys, True, 2)
    assert myDes_encrypted_block.to_bytes() == pyDes_encrypted_block.to_bytes(8, "big")


from Crypto.Cipher import DES
from pyDes import DesKey
@pytest.mark.parametrize("block, password", [
    (b"12345678", b"password"),
    (b"abcdefgh", b"Passw0rd"),
    (b"secret12", b"12345678"),
])
def test_encrypt_block(block, password):
    myDes_block = BitArray(block)
    myDes_round_keys = generate_des_round_keys(BitArray(password))
    myDes_encrypted_block = encrypt_block(myDes_block, myDes_round_keys, number_of_rounds=16)

    pyDes_cipher = DesKey(password)
    pyDes_encrypted_block = pyDes_cipher.encrypt(block)

    crypto_cipher = DES.new(password, DES.MODE_ECB)
    crypto_encrypted_block = crypto_cipher.encrypt(block)

    assert myDes_encrypted_block.to_bytes() == pyDes_encrypted_block
    assert myDes_encrypted_block.to_bytes() == crypto_encrypted_block