EVENTUAL_BITS = 48
BITS_TO_TEST = 26

def compute():
    result = 0
    for i in range(2**BITS_TO_TEST):
        result += (i % 10) * 2 - 1
    return result