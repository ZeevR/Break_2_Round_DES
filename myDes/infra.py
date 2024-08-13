class BitArray:
    def __init__(self, input_data):
        if isinstance(input_data, bytes):
            self.bit_list = []
            for byte in input_data:
                for i in range(8):
                    self.bit_list.append((byte >> (7 - i)) & 1)
        elif isinstance(input_data, list):
            for bit in input_data:
                if bit not in (0, 1):
                    raise ValueError("All elements in the list must be 0 or 1")
            self.bit_list = input_data
        elif isinstance(input_data, BitArray):
            self.bit_list = input_data.bit_list.copy()
        else:
            raise ValueError("Input must be bytes, a list of 0s and 1s, or another BitArray instance")

    def __str__(self):
        return self.to_bytes().hex().upper()

    def __repr__(self):
        byte_representation = self.to_bytes()
        return f"BitArray({self.bit_list}), Bytes({byte_representation})"

    def __getitem__(self, key):
        if isinstance(key, slice):
            if key.step is not None:
                raise ValueError("Step is not supported for slicing BitArray")
            return BitArray(self.bit_list[key.start:key.stop])
        return self.bit_list[key]

    def __setitem__(self, key, value):
        if isinstance(key, slice):
            if not all(v in (0, 1) for v in value):
                raise ValueError("All bit values must be 0 or 1")
            self.bit_list[key] = value
        else:
            if value not in (0, 1):
                raise ValueError("Bit value must be 0 or 1")
            self.bit_list[key] = value

    def __len__(self):
        return len(self.bit_list)

    def __add__(self, other):
        if not isinstance(other, BitArray):
            raise TypeError("Operand must be an instance of BitArray")
        concatenated_list = self.bit_list + other.bit_list
        return BitArray(concatenated_list)

    def __eq__(self, other: 'BitArray') -> bool:
        if not isinstance(other, BitArray):
            return NotImplemented
        return self.bit_list == other.bit_list
    
    def __hash__(self) -> int:
        return hash(tuple(self.bit_list))

    def get_bits(self) -> list[int]:
        return self.bit_list

    def to_bytes(self) -> bytes:
        byte_array = bytearray()
        for i in range(0, len(self.bit_list), 8):
            byte = 0
            for bit in self.bit_list[i:i+8]:
                byte = (byte << 1) | bit
            byte_array.append(byte)
        return bytes(byte_array)

    def xor_with(self, other: 'BitArray') -> 'BitArray':
        if len(self.bit_list) != len(other.bit_list):
            raise ValueError("BitArrays must be of the same length to XOR")
        result = []
        for i in range(len(self.bit_list)):
            result.append(self.bit_list[i] ^ other.bit_list[i])
        return BitArray(result)

    def circular_left_shift(self, shifts: int) -> 'BitArray':
        shifted_list = self.bit_list[shifts:] + self.bit_list[:shifts]
        return BitArray(shifted_list)