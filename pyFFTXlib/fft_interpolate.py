import numpy as np
from pyFFTXlib.fft_error import fftx_error__
from pyFFTXlib.fft_types import fft_type_descriptor
from pyFFTXlib.fft_interfaces import fwfft, invfft

def fft_interpolate(
    dfft_in:fft_type_descriptor, v_in, 
    dfft_out:fft_type_descriptor, v_out
    ):
    #
    #   This subroutine interpolates an array  v_in   defined on fft grid  dfft_in
    #                           to   an array  v_out  defined on fft grid  dfft_out
    #   v_in and v_out are assumed to be real arrays and may concide
    #
    # v_in = np.zeros(dfft_in.nrr)
    # v_out = np.zeros(dfft_out.nnr)  
    if (dfft_out.grid_id == dfft_in.grid_id):
        v_out = v_in
    else:
        if (dfft_in.lgamma != dfft_out.lgamma):
            fftx_error__("fft_interpolate_real","two grids with inconsistent lgamma values", 1)
        aux_in = v_in
        fwfft("Rho", aux_in, dfft_in)
        aux_out = np.zeros(dfft_out.nnr)  
        ngm = np.min(dfft_in.ngm, dfft_out.ngm)
        aux_out[dfft_out.nl[:ngm]] = aux_in[dfft_in.nl[:ngm]]

        if (dfft_in.lgamma):
            aux_out[dfft_out.nlm[:ngm]] = aux_in[dfft_in.nlm[:ngm]]

        invfft("Rho", aux_out, dfft_out)
        v_out[:dfft_out.nnr] = aux_out[:dfft_out.nnr]
    return v_out

fft_interpolate_complex = fft_interpolate
fft_interpolate_real = fft_interpolate