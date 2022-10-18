import numpy as np
from .fft_param import fft_param

try:
    from mpi4py import MPI

    HAVE_MPI = True

    def fftx_error__( 
        calling_routine:str, 
        message:str, 
        ierr:int, 
        comm:MPI.COMM_WORLD 
        ):

        """ name changed from fftx_error_uniform__ to fftx_error_mpi__ """
        
        if ierr <= 0:
            return

        my_rank = comm.Get_rank()

        if my_rank == 0:
            print("{}".format(ierr))
            #-----------
            # unfinished
            #-----------
            print("unfinished")
            print("---- stopping... ----")

except:

    HAVE_MPI = False

    def fftx_error__( calling_routine:str, message:str, ierr:int):
        """
        This is a simple routine which writes an error message to output:
        """
        if ierr <= 0:
            return

        print("{}".format(ierr))
        #-----------
        # unfinished
        #-----------
        print("unfinished")
        print("---- stopping... ----")


