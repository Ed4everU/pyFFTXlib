import numpy as np


class fft_param:

    try:
        import mpi4py
    except:
        HAVE_MPI = False

    # Number of different FFT tables that the module
    #could keep into memory without reinitialization
    ndims:np.int = 20

    # Max allowed fft dimension
    nfftx:np.int = 16385

    eps8:np.float64 = 1.0E-8

