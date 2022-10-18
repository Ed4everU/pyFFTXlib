from cgitb import small
from termios import N_STRIP
import numpy as np
from .fft_param import fft_param


class sticks_map:

    lgamma:bool = False                # if .true. the map has gamma symmetry
    lpara:bool = False                 # if .true. the map is set for parallel and serial, if .false. only serial 
    mype:int = 0                       # my task id (starting from 0)
    nproc:int = 1                      # number of task (as nproc in fft_type_descriptor)
    nyfft:int = 1                      # number processors in y-direction as nproc2 in fft_type_descriptor)
    nstx:int = 0                       # a safe maximum number of sticks on the map
    lb = np.zeros(3,dtype=np.int64)    # map's lower bounds
    ub = np.zeros(3,dtype=np.int64)    # map's upper bounds
    idx:np.ndarray                     # the index of each stick
    ist:np.ndarray                     # the cartesian coordinates of each stick
    stown:np.ndarray                   # the owner of each stick
    indmap:np.ndarray                  # the index of each stick (represented on the map)
    bg=np.zeros((3,3),dtype=np.int64)  # base vectors, the generators of the mapped space
    iproc:np.ndarray                   # the processor index (as in fft_type_descriptor)
    iproc2:np.ndarray                  # the Y group processor index (as in fft_type_descriptor)

    try:
        from mpi4py import MPI
        comm = MPI.COMM_WORLD
        HAVE_MPI = True
    except:
        HAVE_MPI = False
        comm = None

    def __init__(self, lgamma, lpara, nyfft, iproc, iproc2, nr1, nr2, nr3, bg, comm):
        """
        equivalent to `sticks_map_allocate` part when self.nstx == 0
        """
        ub = np.zeros(3,dtype=np.int64)

        ub[0] = (nr1-1)/2
        ub[1] = (nr2-1)/2
        ub[2] = (nr3-1)/2
        lb = -1*self.ub
        nstx = (self.ub[0]-self.lb[1]+1)*(self.ub[1]-self.lb[1]+1)

        # if self.nstx == 0:
        #     # this map is clean, allocate
        #     #
        self.mype = 0
        self.nproc = 1
        self.comm = comm
        #
        if self.HAVE_MPI:
            self.mype = self.comm.Get_rank()
            self.nproc = self.comm.Get_size()
        #
        self.nstx = nstx
        self.lgamma = lgamma
        self.lpara = lpara
        self.nyfft = nyfft
        self.iproc = iproc
        self.iproc2 = iproc2
        self.ub = ub
        self.lb = lb
        self.bg = bg
        nzfft = self.nproc / nyfft
        # self.iproc = np.zeros((nyfft, nzfft))
        # self.iproc2 = np.zeros((self.nproc))
        self.iproc = iproc
        self.iproc2 = iproc2

        self.indmap = np.zeros((self.ub[0]))

    def update(self):
        self.__init__()