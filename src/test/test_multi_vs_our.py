import numpy as np
import time
from multiprocessing import shared_memory
from matplotlib import pyplot as plt
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../extra_compressors')))
from compression_ourDCT_multiprocess import compress_multiproc, decompress_multiproc
from compression_ourDCT import compress_our, decompress_our


if __name__ == "__main__":
    
    block_dim = 8
    threshold = 5
    
    n_procs = [2, 4, 6]
    start = 100
    step = 500
    n_it = 21
    
    ns = [start] + [step*i for i in range(1, n_it)]
    print(ns)
    
    elapsed_times = np.zeros((len(n_procs) + 1, len(ns)))
    i = 0
    for n in ns:
        print(n)
        print("*******************")
        m = n
        
        #single process, centralized
        F = np.random.randint(0, 256, size=(n, m), dtype=np.int16)
        s = time.time()
        res = compress_our(F.copy(), block_dim = block_dim, threshold = threshold)
        dec_res = decompress_our(res.copy(), block_dim)
        e = time.time()
        print("Time single process:", e - s)
        elapsed_times[0][i] = e - s
        for j in range(len(n_procs)):
            n_proc = n_procs[j]
            # multiproc
            shm_f = shared_memory.SharedMemory(name="F", create=True, size=n * m * 2)
            shm_f.buf[:] = F.tobytes()
            n_rows = n // block_dim
            n_cols = m // block_dim
            shm_p = shared_memory.SharedMemory(name = "compressed_pic", create=True, size=n_rows * block_dim * n_cols * block_dim * 2) #int = 16 bit = 2 byte
            compressed_pic = np.ndarray(shape = (n_rows * block_dim, n_cols * block_dim), dtype=np.int16, buffer = shm_p.buf)
            
            shm_d = shared_memory.SharedMemory(name = "decompressed_pic", create=True, size=n_rows * block_dim * n_cols * block_dim * 2) #int = 16 bit = 2 byte
            decompressed_pic = np.ndarray(shape = (n_rows * block_dim, n_cols * block_dim), dtype=np.int16, buffer = shm_d.buf)
            s = time.time()
            compress_multiproc(block_dim = block_dim, threshold = threshold, n_procs = n_proc, n = n, m = m)
            decompress_multiproc(block_dim = block_dim, n_procs = n_proc, n = n, m = m)
            e = time.time()
            print("Time multiproc ", n_proc, " : ", e - s)
            # print(np.all(res == compressed_pic))
            # print(np.all(dec_res == decompressed_pic))
            elapsed_times[j + 1][i] = e - s #j + 1 -> the first row is reserved for centralized version
            
            shm_f.close()
            shm_p.close()
            shm_d.close()
            shm_f.unlink()
            shm_p.unlink()
            shm_d.unlink()
        
        i = i + 1
        
        
    #plot
    labels = ["1 process"] + [str(n_procs[i]) + " processes" for i in range(len(n_procs))]
    colors = plt.cm.tab10.colors[:len(n_procs) + 1]
    print(elapsed_times)
    print(labels)
    for i in range(len(elapsed_times)):
        plt.plot(ns, elapsed_times[i, :], marker='o', linestyle='-', color=colors[i], label=labels[i])

    plt.title('Elapsed Times - Compression & Decompression')
    plt.xlabel('Matrix Dimension (Number of Rows)')
    plt.ylabel('Time (s)')
    plt.legend()
    plt.grid(True)

    plt.show()