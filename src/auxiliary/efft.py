import numpy as np


def fft(wave, Space):
    """
    @Params
    """

    a = Space.dx * (2*np.pi*wave.eps)**(-.5)
    outer = np.exp(-1j/wave.eps * Space.xgrid[0]*Space.pgrid)
    inner = np.exp(1j * np.pi/Space.dx * (Space.xgrid - Space.xgrid[0]))

    return a * outer * np.fft.fft(inner * wave.psi) # default should be along rows

def ifft(wave, Space):
    """
    Implementation of scaled Fourier Transform
    necessary in order to capture for accurately
    representing the highly oscillatory behaviour 
    of the wave packet.
    """

    A = Space.n * Space.dp * (2*np.pi*wave.eps)**(-.5) 
    shiftOut = np.exp(-1j*np.pi/Space.dx * (Space.xgrid - Space.xgrid[0]))
    shiftIn = np.exp(1j/wave.eps * Space.xgrid[0]*Space.pgrid)

    return A * shiftOut * np.fft.ifft(shiftIn * wave.psihat)


if __name__ == "__main__":

    pass
