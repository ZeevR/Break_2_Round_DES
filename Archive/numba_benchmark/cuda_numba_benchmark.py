import numpy as np
from numba import cuda
import time

# Size of the matrix
N = 1024

# Create two random matrices
A = np.random.rand(N, N).astype(np.float32)
B = np.random.rand(N, N).astype(np.float32)
C = np.zeros((N, N), dtype=np.float32)

# Define the GPU kernel for matrix multiplication
@cuda.jit
def matmul_gpu(A, B, C):
    row, col = cuda.grid(2)
    if row < C.shape[0] and col < C.shape[1]:
        temp = 0.
        for k in range(A.shape[1]):
            temp += A[row, k] * B[k, col]
        C[row, col] = temp

# Define the block and grid size
threads_per_block = (16, 16)
blocks_per_grid_x = int(np.ceil(A.shape[0] / threads_per_block[0]))
blocks_per_grid_y = int(np.ceil(A.shape[1] / threads_per_block[1]))
blocks_per_grid = (blocks_per_grid_x, blocks_per_grid_y)

# Copy the matrices to the device
A_device = cuda.to_device(A)
B_device = cuda.to_device(B)
C_device = cuda.to_device(C)

# Measure the time taken for the GPU computation
start = time.time()
matmul_gpu[blocks_per_grid, threads_per_block](A_device, B_device, C_device)
cuda.synchronize()
end = time.time()

# Copy the result back to the host
C = C_device.copy_to_host()

print("Time taken for GPU computation:", end - start, "seconds")
