from math import lgamma
import numpy as np

from pyFFTXlib.fft_error import HAVE_MPI
from .fft_support import good_fft_dimension, good_fft_order
from .fft_param import fft_param
try:
    from mpi4py import MPI
    HAVE_MPI = True
except:
    HAVE_MPI = False

class fft_type_descriptor:

    nr1 = 0            #
    nr2 = 0            # effective FFT dimensions of the 3D grid (global)
    nr3 = 0            # 
    nr1x = 0           # FFT grids leading dimensions
    nr2x = 0           # dimensions of the arrays for the 3D grid (global)
    nr3x = 0           # may differ from nr1 ,nr2 ,nr3 in order to boost performances

    lpara = False
    lgamma = False
    root = 0
    if HAVE_MPI:
        comm = MPI.COMM_NULL 
        comm2 = MPI.COMM_NULL
        comm3 = MPI.COMM_NULL
    else:
        comm = None    # communicator for the main fft group
        comm2 = None   # communicator for the fft group along the second direction
        comm3 = None   # communicator for the fft group along the third direction
    
    nproc = 1          # number of processor in the main fft group
    nproc2 = 1         # number of processor in the fft group along the second direction
    nproc3 = 1         # number of processor in the fft group along the third direction
    mype = 0           # my processor id (starting from 0) in the fft main communicator
    mype2 = 0          # my processor id (starting from 0) in the fft communicator along the second direction (nproc2)
    mype3 = 0          # my processor id (starting from 0) in the fft communicator along the third direction (nproc3)

    iproc:np.ndarray   # 
    iproc2:np.ndarray  # subcommunicators proc mapping (starting from 1)
    iproc3:np.ndarray  # 
 
    #
    # FFT distributed data dimensions and indices
    #
    my_nr3p = 0        # size of the "Z" section for this processor = nr3p( mype3 + 1 )    ~ nr3/nproc3
    my_nr2p = 0        # size of the "Y" section for this processor = nr2p( mype2 + 1 )    ~ nr2/nproc2
    #
    my_i0r3p = 0
    my_i0r2p = 0 
    #
    nr3p:np.ndarray
    nr3p_offset:np.ndarray
    nr2p:np.ndarray
    nr2p_offset:np.ndarray
    nr1p:np.ndarray
    nr1w:np.ndarray
    nr1w_tg:np.ndarray
