import time
# from numba import jit

EVENTUAL_BITS = 48
BITS_TO_TEST = 26

def compute():
    result = 0
    for i in range(2**BITS_TO_TEST):
        result += (i % 10) * 2 - 1
    return result

start_time = time.time()
compute()
end_time = time.time()

execution_time = end_time - start_time
print(f"Actual execution time: {execution_time} seconds")
print(f"Expected execution time: {execution_time* (2**(EVENTUAL_BITS-BITS_TO_TEST))/3600} hours")

# @jit(nopython=True)
# def compute_numba():
#     result = 0
#     for i in range(2**BITS_TO_TEST):
#         result += (i % 10) * 2 - 1
#     return result

# start_time = time.time()
# compute_numba()
# end_time = time.time()

# execution_time = end_time - start_time
# print(f"Actual execution time: {execution_time} seconds")
# print(f"Expected execution time: {execution_time* (2**(EVENTUAL_BITS-BITS_TO_TEST))/3600} hours")