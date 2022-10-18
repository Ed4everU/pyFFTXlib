import numpy as np
from pyFFTXlib.fft_types import fft_type_descriptor
from pyFFTXlib.fft_error import fftx_error__


def fft_set_nl(dfft:fft_type_descriptor, at, g, mill=None):
    """
    Input:  FFT descriptor dfft, lattice vectors at, list of G-vectors g
    Output: indices nl such that G_fft(nl(i)) = G(i)
            indices nlm such that G_fft(nlm(i)) = -G(i) only if lgamma=.true.
            optionally, Miller indices: if bg = reciprocal lattice vectors,
    G(:,i) = mill(1,i)*bg(:,1) + mill(2,i)*bg(:,2) + mill(3,i)*bg(:,3)
    """
    dfft.nl = np.zeros(dfft.ngm, dtype=np.int64)
    if dfft.lgamma:
        dfft.nlm = np.zeros(dfft.ngm,dtype=np.int64)

    for ng in range(dfft.ngm):
        #
        n1 = int(np.sum(g[:,ng]*at[:,0]))
        if mill != None:
            mill[0,ng] = n1
        if n1<0:
            n1 += dfft.nr1
        #
        n2 = int(sum(g[:,ng]*at[:,1]))
        if mill != None:
            mill[1,ng] = n2
        if n2<0:
            n2 += dfft.nr2
        #
        n3 = int(sum(g[:,ng]*at[:,2]))
        if mill != None:
            mill[2,ng] = n3
        if n3<0:
            n2 += dfft.nr3

        if (n1>=dfft.nr1 or n2>=dfft.nr2 or n3>=dfft.nr3):
            fftx_error__("ggen","Mesh too small?", ng)

        if dfft.lpara:
            dfft.nl[ng] = 1+n3+(dfft.isind[n1+n2*dfft.nr1x]-1)
        else:
            dfft.nl[ng] = 1+n1+n2*dfft.nr1x+n3*dfft.nr1x*dfft.nr2x

        if dfft.lgamma:
            #
            n1 = -n1
            if n1<0:
                n1 += dfft.nr1
            #
            n2 = -n2
            if n2<0:
                n2 += dfft.nr2
            #
            n3 = -n3
            if n3<0:
                n3 += dfft.nr3
            #
            if dfft.lpara:
                dfft.nlm[ng] = 1+n3+(dfft.isind[n1+n2*dfft.nr1x]-1)*dfft.nr3x
            else:
                dfft.nlm[ng] = 1+n1+n2*dfft.nr1x+n3*dfft.nr1x*dfft.nr2x