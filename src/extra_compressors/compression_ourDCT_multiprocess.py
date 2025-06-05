from multiprocessing import Process, shared_memory
import os
import numpy as np
from DCT2D import DCT2D, compute_D, IDCT2D
from utils import cut, clip_and_round

def compress_block(F, compressed_pic, D, cur_row, cur_col, block_dim, threshold):
    B = F[cur_row:cur_row + block_dim, cur_col: cur_col + block_dim]
    B -= 128
    
    # execute DCT2 on block B
    C = DCT2D(B, D)
    C = C.round(decimals=0)
    C_cut = cut(C, threshold)
    compressed_pic[cur_row:cur_row + block_dim,
                           cur_col: cur_col + block_dim] = C_cut
    
    
def main_proc_compression(block_dim, threshold, n, m, row_first_index, row_last_index):    
    n_rows = n // block_dim 
    n_cols = m // block_dim
    
    #read shared memory
    shm_f = shared_memory.SharedMemory(name = "F")
    F = np.ndarray((n, m), dtype=np.int16, buffer=shm_f.buf)
    
    shm_D = shared_memory.SharedMemory(name = "D")
    D = np.ndarray((block_dim, block_dim), dtype=np.float64, buffer=shm_D.buf)
    
    shm_p = shared_memory.SharedMemory(name = "compressed_pic") 
    compressed_pic = np.ndarray(shape = (n_rows * block_dim, n_cols * block_dim), dtype=np.int16, buffer = shm_p.buf)
    
    while row_first_index < row_last_index:
        cur_row = row_first_index * block_dim
        cur_col = 0
        #iterate through columns and compress the blocks
        for _ in range(n_cols):
            compress_block(F, compressed_pic, D, cur_row, cur_col, block_dim, threshold)
            cur_col = cur_col + block_dim
        row_first_index = row_first_index + 1
        
    shm_f.close()
    shm_p.close()
    shm_D.close()

def compress_multiproc(block_dim, threshold, n_procs, n, m):
    procs = []
    
    shm_D = shared_memory.SharedMemory(name = "D", create=True, size = block_dim*block_dim*8)
    D = np.ndarray((block_dim, block_dim), dtype = np.float64, buffer = shm_D.buf)
    D_computed = compute_D(block_dim)
    D[:] = D_computed #copy data onto shared memory

    # divide pic into blocks
    n_rows = n // block_dim 
    if n_rows < n_procs:
        n_procs = n_rows
    
    rows_per_proc = np.array([n_rows // n_procs for _ in range(n_procs)])
    remaining_rows = n_rows % n_procs # the first remaining_rows processes will have one more row
    
    # every process works on the rows from row_first_index (included) to row_last_index (excluded);
    row_first_index, row_last_index = 0, 0   
    for i in range(n_procs):
        if i < remaining_rows:
            rows_per_proc[i] = rows_per_proc[i] + 1

        row_last_index = row_first_index + rows_per_proc[i]

        procs.append(Process(target = main_proc_compression, args = (block_dim, threshold, n, m, row_first_index, row_last_index)))
        procs[i].start()
        
        #update the indexes
        row_first_index = row_last_index
        
    for i in range(len(procs)):
        procs[i].join()
        
    shm_D.close()
    shm_D.unlink()


###############################################################################################


def decompress_block(C, decompressed_pic, D, cur_row, cur_col, block_dim):
    
    B = C[cur_row:cur_row + block_dim, cur_col: cur_col + block_dim].astype(np.float64)
    
    # execute IDCT2 on block B
    L = IDCT2D(B, D)
    L += 128
    L = clip_and_round(L)
    
    decompressed_pic[cur_row:cur_row + block_dim,
                           cur_col: cur_col + block_dim] = L
    
    
def main_proc_decompression(block_dim, n, m, row_first_index, row_last_index):
    n_rows = n // block_dim 
    n_cols = m // block_dim
       
    #read shared memory 
    shm_c = shared_memory.SharedMemory(name = "compressed_pic")
    C = np.ndarray((n_rows*block_dim, n_cols*block_dim), dtype=np.int16, buffer=shm_c.buf)
    
    shm_D = shared_memory.SharedMemory(name = "D")
    D = np.ndarray((block_dim, block_dim), dtype=np.float64, buffer=shm_D.buf)
    
    shm_p = shared_memory.SharedMemory(name = "decompressed_pic") 
    decompressed_pic = np.ndarray(shape = (n_rows * block_dim, n_cols * block_dim), dtype=np.int16, buffer = shm_p.buf)
    
    while row_first_index < row_last_index:
        cur_row = row_first_index * block_dim
        cur_col = 0
        #iterate through columns and decompress the blocks
        for _ in range(n_cols):
            decompress_block(C, decompressed_pic, D, cur_row, cur_col, block_dim)
            cur_col = cur_col + block_dim
        row_first_index = row_first_index + 1

    shm_c.close()
    shm_p.close()
    shm_D.close()
    
    
    
def decompress_multiproc(block_dim, n_procs, n, m):
    procs = []
    
    shm_D = shared_memory.SharedMemory(name = "D", create=True, size = block_dim*block_dim*8)
    D = np.ndarray((block_dim, block_dim), dtype = np.float64, buffer = shm_D.buf)
    D_computed = compute_D(block_dim)
    D[:] = D_computed 
    
    n_rows = n // block_dim 
    if n_rows < n_procs:
        n_procs = n_rows
    
    rows_per_proc = np.array([n_rows // n_procs for _ in range(n_procs)])
    remaining_rows = n_rows % n_procs
    
    row_first_index, row_last_index = 0, 0
    
    for i in range(n_procs):
        if i < remaining_rows:
            rows_per_proc[i] = rows_per_proc[i] + 1

        row_last_index = row_first_index + rows_per_proc[i]
        
        #proc[i] works on F[row_first_index:row_last_index]
        procs.append(Process(target = main_proc_decompression, args = (block_dim, n, m, row_first_index, row_last_index)))
        procs[i].start()
        
        #update the indexes
        row_first_index = row_last_index
        
    for i in range(len(procs)):
        procs[i].join()
        
    shm_D.close()
    shm_D.unlink()