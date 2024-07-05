import numpy as np
import time

# Size of the matrix
N = 1024

# Create two random matrices
A = np.random.rand(N, N).astype(np.float32)
B = np.random.rand(N, N).astype(np.float32)

# Measure the time taken for matrix multiplication using NumPy
start = time.time()
C = np.dot(A, B)
end = time.time()

print("Time taken for CPU computation with NumPy (PyPy):", end - start, "seconds")
