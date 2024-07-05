import time
from compute import *

start_time = time.time()
compute()
end_time = time.time()

execution_time = end_time - start_time
print(f"Actual execution time: {execution_time} seconds")
print(f"Expected execution time: {execution_time* (2**(EVENTUAL_BITS-BITS_TO_TEST))/3600} hours")
