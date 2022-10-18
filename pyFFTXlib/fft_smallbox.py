import numpy as np


class fft_smallbox:

    cft_b = None
    cft_b_omp_init = None
    cft_b_omp = None
    # ndims : Number of different FFT tables that the module
    # could keep into memory without reinitialization
    ndims = 3

    cft_b_dims = np.zeros(3,dtype=np.int64)


    

