import numpy as np
from .fft_param import fft_param


class sticks_map:


    #
    # if .true. the map has gamma symmetry
    #
    lgamma:bool = False
    #
    # if .true. the map is set for parallel and serial, 
    # if .false. only serial 
    #
    lpara:bool = False  
    #
    # my task id (starting from 0)
    #  
    mype:int = 0
    #
    # number of task (as nproc in fft_type_descriptor)
    #
    nproc:int = 1
    #
    # number processors in y-direction 
    # (as nproc2 in fft_type_descriptor)
    #
    nyfft:int = 1
    #
    # a safe maximum number of sticks on the map
    #
    nstx:int = 0
    #
    # map's lower bounds
    #
    lb = np.zeros(3,dtype=np.int64)
    #
    # map's upper bounds
    # 
    ub = np.zeros(3,dtype=np.int64)

    try:
        from mpi4py import MPI
        comm = MPI.COMM_WORLD
        HAVE_MPI = True
    except:
        HAVE_MPI = False

    @staticmethod
    def hpsort(n, ra, ind):
        # sort an array ra(1:n) into ascending order using heapsort algorithm.
        # n is input, ra is replaced on output by its sorted rearrangement.
        # create an index table (ind) by making an exchange in the index array
        # whenever an exchange is made on the sorted data array (ra).
        # in case of equal values in the data array (ra) the values in the
        # index array (ind) are used to order the entries.
        # if on input ind(1)  = 0 then indices are initialized in the routine,
        # if on input ind(1) #= 0 then indices are assumed to have been
        #                initialized before entering the routine and these
        #                indices are carried around during the sorting process
        #
        # no work space needed #
        # free us from machine-dependent sorting-routines #
        #
        # adapted from Numerical Recipes pg. 329 (new edition)
        #

        pass