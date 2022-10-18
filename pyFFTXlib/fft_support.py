import numpy as np
from .fft_error import fftx_error__
from .fft_param import fft_param

def good_fft_dimension(n:np.int64):
    nx = n
    # # __LINUX_ESSL only
    # log2n = np.log(n)/np.log(2)
    # if (np.abs(int(log2n)-log2n) < 1.0e-8):
    #     nx = n+1
    if np.mod(n,2)==0:
        nx = n+1
    return nx

def allowed(nr:np.int64):
    pwr = np.zeros(5,dtype=np.int64)
    factors = (2,3,5,7,11)

    mr = nr
    flag = False
    for i in range(5):
        if not flag:
            fac = factors[i]
            maxpwr = int(np.log(mr)/np.log(fac))+1
            for p in range(maxpwr):
                if not flag:
                    if mr==1:
                        flag = True
                    if np.mod(mr,fac) == 0:
                        mr /= fac
                        pwr[i] += 1

    if nr != mr*2**pwr[0]*3**pwr[1]*5**pwr[2]*7**pwr[3]*11**pwr[4]:
        fftx_error__("allowed ", " what ?#?", 1)
    if mr!=1:
        allowed = False
    else:
        allowed = (pwr[3]==0 and pwr[4]==0)
    return allowed

def good_fft_order(nr, np=None):
    #
    #    This function find a "good" fft order value greater or equal to "nr"
    #
    #    nr  (input) tentative order n of a fft
    #
    #    np  (optional input) if present restrict the search of the order
    #        in the ensemble of multiples of np
    #
    #    Output: the same if n is a good number
    #         the closest higher number that is good
    #         an fft order is not good if not implemented (as on IBM with ESSL)
    #         or implemented but with awful performances (most other cases)

    new = nr
    if np != None:
        if np <= 0 or np > nr:
            fftx_error__("good_fft_order"," invalid np ", 1)
            while (not allowed(new)) or (np.mod(new,np)!=0) and (new<=fft_param.nfftx):
                new += 1
        else:
            while (not allowed(new)) and (new<=fft_param.nfftx):
                new+=1

    if new>fft_param.nfftx:
        fftx_error__( " good_fft_order ", " fft order too large ", new )

    return new