import pytest
from myDes.infra import BitArray

def test_bitarray_init_with_bytes():
    byte_input = bytes([0b10101010])
    bit_array = BitArray(byte_input)
    assert bit_array.bit_list == [1, 0, 1, 0, 1, 0, 1, 0]

def test_bitarray_init_with_list():
    list_input = [1, 0, 1, 0]
    bit_array = BitArray(list_input)
    assert bit_array.bit_list == list_input

def test_bitarray_init_with_invalid_input():
    with pytest.raises(ValueError):
        BitArray("invalid")

def test_bitarray_setitem():
    bit_array = BitArray([0, 0, 0, 0])
    bit_array[2] = 1
    assert bit_array.bit_list == [0, 0, 1, 0]

def test_bitarray_getitem():
    bit_array = BitArray([1, 0, 1, 0])
    assert bit_array[2] == 1

def test_bitarray_len():
    bit_array = BitArray([1, 0, 1, 0])
    assert len(bit_array) == 4

def test_bitarray_xor_with():
    bit_array1 = BitArray([1, 0, 1, 0])
    bit_array2 = BitArray([1, 1, 0, 0])
    result = bit_array1.xor_with(bit_array2)
    assert result.bit_list == [0, 1, 1, 0]

def test_bitarray_slice():
    bit_array = BitArray([1, 0, 1, 0, 1, 0, 1, 0])
    sliced_bit_array = bit_array[2:6]
    assert sliced_bit_array.bit_list == [1, 0, 1, 0]

def test_bitarray_circular_left_shift():
    bit_array = BitArray([1, 0, 1, 0, 1, 0, 1, 0])
    bit_array = bit_array.circular_left_shift(3)
    assert bit_array.bit_list == [0, 1, 0, 1, 0, 1, 0, 1]

def test_bitarray_concatenate():
    bit_array1 = BitArray([1, 0, 1])
    bit_array2 = BitArray([0, 1, 0])
    concatenated_bit_array = bit_array1 + bit_array2
    assert concatenated_bit_array.bit_list == [1, 0, 1, 0, 1, 0]

def test_bitarray_to_bytes():
    bit_array = BitArray([1, 0, 1, 0, 1, 0, 1, 0])
    expected_bytes = bytes([0b10101010])
    assert bit_array.to_bytes() == expected_bytes

def test_bitarray_get_bits():
    bit_array = BitArray([1, 0, 1, 0, 1, 0, 1, 0])
    expected_bits = [1, 0, 1, 0, 1, 0, 1, 0]
    assert bit_array.get_bits() == expected_bits

def test_bitarray_eq():
    bit_array1 = BitArray([1, 0, 1, 0])
    bit_array2 = BitArray([1, 0, 1, 0])
    assert bit_array1 == bit_array2