import sys
sys.path.insert(0, '..')
import numpy as np
from init_cond.wavepacket import Wavepacket

class Hagedorn(Wavepacket):
    """Could make it so that at index zero it generates the Gaussian"""
    def __init__(self, eps, q, p, Q, P, index, neqs = 1, space = None):

        self.q = q
        self.p = p
        self.Q = Q
        self.P = P
        self.index = index
        self.eps = eps

        if space:
            self.__eval_psi(space)
            self.__eval_psihat(space) # this should be straightforward
            if neqs == 2:
                self.psi = np.stack((self.psi, np.zeros(space.n, dtype='complex_')))
                self.psihat = np.stack((self.psihat, np.zeros(space.n, dtype='complex_')))
                print('Initial wavepacket is a Gaussian: q0=%.2f, p0=%.2f, eps=%.3f' \
                    %(q0, p0, eps))

    def __eval_psi(self, space): # perhaps it is better as it was done before so that the user does not need to construct its axis...?
        """Build Hagedorn wavepacket by multiplying Gaussian and polynomial"""
        #self.__eval__gaussian(space)
        self.__eval_gaussian(space)
        if self.index != 0:
            y = np.ones(len(self.psi), dtype = 'complex_')
            z = np.ones(len(self.psi), dtype = 'complex_')
            for i in range(self.index):
                temp = (np.sqrt(2/self.eps)/self.Q*(space.xgrid - self.q)*y - \
                        np.conj(self.Q)/self.Q * np.sqrt(i)*z)/np.sqrt(i+1)
                z = y
                y = temp
            self.psi *= y

    def __eval_psihat(self, space):
        """Build Hagedorn wavepacket by multiplying Gaussian and polynomial"""
        #self.__eval__gaussian(space)
        self.__eval_gaussian_hat(space)
        if self.index != 0:
            y = np.ones(len(self.psi), dtype = 'complex_')
            z = np.ones(len(self.psi), dtype = 'complex_')
            for i in range(self.index):
                temp = (np.sqrt(2/self.eps)/self.P*(space.pgrid - self.p)*y - \
                        np.conj(self.P)/self.P * np.sqrt(i)*z)/np.sqrt(i+1)
                z = y
                y = temp
            self.psihat *= (y * (-1j)**self.index)

    def __eval_gaussian(self, space):
        # need to check prefactor Q0
        self.psi = (np.pi * self.eps)**(-.25) * self.Q**(-0.5)\
                * np.exp( 1j/(2*self.eps)*self.P/self.Q*(space.xgrid - self.q)**2
               + 1j/self.eps*self.p*(space.xgrid - self.q))
    def __eval_gaussian_hat(self, space):
        # need to check prefactor Q0
        self.psihat = np.exp(-1j*self.p*self.q/self.eps) * (np.pi * self.eps)**(-.25) \
                * self.P**(-0.5) * np.exp(- 1j/(2*self.eps)*self.Q/self.P*(space.pgrid - self.p)**2 \
                - 1j/self.eps*self.q*(space.pgrid - self.p))


if __name__ == "__main__":
    import sys
    sys.path.insert(0, '..')
    from auxiliary.space import Space
   # import matplotlib.pyplot as plt
    #from mpl_toolkits import mplot3d
    import numpy as np

    eps = 1/50
    q = 4
    p = 0
    P = 1j
    Q = 1
    index = 20

    space = Space(2**10, 2, eps, 8)
    wave = Hagedorn(eps, q, p, Q, P, index, 1, space)


    #ax3.plot(x, abs(psi), label=r'$|\Psi$|')
    #ax3D.plot3D(x, psi.real, psi.imag, color='r')
    plt.plot(space.xgrid, wave.psi.real) 
    plt.show()
    plt.close('all')
