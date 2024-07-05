import pytest
from myDes.infra import BitArray
from myDes.key_schedule import generate_des_round_keys
from pyDes import DesKey

def test_generate_des_round_keys():
    password = b"Password"
    round_keys = generate_des_round_keys(BitArray(password))
    # Add assertions to verify the correctness of round_keys
    # This is an example assertion, you'll need to replace it with actual checks
    assert len(round_keys) == 16, "There should be 16 round keys generated"

def test_deskey_round_keys_as_int():
    password = b"Password"
    example_round_keys = DesKey(password).round_keys_as_int
    # Add assertions to verify the correctness of example_round_keys
    # This is an example assertion, you'll need to replace it with actual checks
    assert len(example_round_keys[0]) == 16, "There should be 16 round keys"

@pytest.mark.parametrize("password", [
    b"Passw0rd",
    b"An0ther1",
    b"12345678",
    b"Secur3!1",
    b"LastOne!"
])
def test_round_keys_equivalence(password):
    # Generate round keys using myDes
    my_des_round_keys = generate_des_round_keys(BitArray(password))

    # Generate round keys using pyDes
    py_des_round_keys = DesKey(password).round_keys_as_int[0]

    # Convert PyDes round keys to bytes
    py_des_round_keys_bytes = []
    for key in py_des_round_keys:
        py_des_round_keys_bytes.append(key.to_bytes(48//8,byteorder='big'))

    # Convert myDes round keys to bytes
    my_des_round_keys_bytes = []
    for key in my_des_round_keys:
        my_des_round_keys_bytes.append(key.to_bytes())

    # Assert that both sets of round keys are equal
    assert my_des_round_keys_bytes == py_des_round_keys_bytes, "Round keys should be equal"