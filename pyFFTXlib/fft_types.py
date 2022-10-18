from ctypes import Union
import numpy as np
from pyFFTXlib.fft_error import HAVE_MPI
from pyFFTXlib.fft_support import good_fft_dimension, good_fft_order
from pyFFTXlib.fft_param import fft_param
from pyFFTXlib.stick_base import sticks_map
from pyFFTXlib.fft_error import fftx_error__
try:
    from mpi4py import MPI
    HAVE_MPI = True
except:
    HAVE_MPI = False



fft_dual = 4.0
incremental_grid_identifier = 0


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
    #
    i0r3p:np.ndarray
    ior2p:np.ndarray
    #
    ir1p:np.ndarray
    indp:np.ndarray
    ir1w:np.ndarray
    indw:np.ndarray
    ir1w_tg:np.ndarray
    indw_tg:np.ndarray
    #
    # INTEGER, POINTER DEV_ATTRIBUTES :: ir1p_d(:),   ir1w_d(:),   ir1w_tg_d(:)   ! duplicated version of the arrays declared above
    # INTEGER, POINTER DEV_ATTRIBUTES :: indp_d(:,:), indw_d(:,:), indw_tg_d(:,:) !
    # INTEGER, POINTER DEV_ATTRIBUTES :: nr1p_d(:),   nr1w_d(:),   nr1w_tg_d(:)   !
    #
    nst:np.int64
    nsp:Union[np.ndarray,None] = None
    nsp_offset:np.ndarray
    nsw:np.ndarray
    nss_offset:np.ndarray
    nsw_tg:np.ndarray
    #
    ngl:np.ndarray
    nwl:np.ndarray
    #
    ngm:np.int64
    ngw:np.int64
    #
    iplp:np.ndarray
    iplw:np.ndarray
    #
    nnp = 0
    nnr = 0
    #
    nnr_tg = 0
    #
    iss:np.ndarray
    isind:np.ndarray
    ismap:np.ndarray
    #
    # INTEGER, POINTER DEV_ATTRIBUTES :: ismap_d(:)
    #
    nl:np.ndarray
    nlm:np.ndarray
    #
    # INTEGER, POINTER DEV_ATTRIBUTES :: ismap_d(:)
    # INTEGER, POINTER DEV_ATTRIBUTES :: nlm_d(:)
    #
    tg_snd:np.ndarray
    tg_rcv:np.ndarray
    tg_sdsp:np.ndarray
    tg_rdsp:np.ndarray
    #
    has_task_groups = False
    use_pencil_decomposition = True
    #
    rho_clock_label:str = " "
    wave_clock_label:str = " "
    #
    grid_id:int
    #
    srh : np.ndarray
    aux : np.ndarray
    #
    comm2s:np.ndarray
    comm3s:np.ndarray

    def __init__(self,
        smap:sticks_map,
        pers:str,
        lgamma,
        lpara,
        comm,
        at,
        bg,
        gcut_in,
        nyfft,
        nmany,
        use_pd = None,
        dual_in = None,
        fft_fact = None,
        ):

        dual = fft_dual
        if dual_in != None:
            dual = dual_in

        if pers == "rho":
            gcut = gcut_in
            gkcut = gcut / dual
        elif pers == "wave":
            gkcut = gcut_in
            gcut = gkcut * dual
        else:
            fftx_error__("fft_type_init ", "  unknown FFT personality ", 1)

        # if self.nsp == None:
        #     pass
        # else:
        #     if self.comm != comm:
    
        if use_pd != None:
            self.use_pencil_decomposition = use_pd
        if (not self.use_pencil_decomposition) and (nyfft>1):
            fftx_error__(" fft_type_init ", " Slab decomposition and task groups not implemented. ", 1, self.comm)
            # ----------
            # unfinished
            # ----------
        



