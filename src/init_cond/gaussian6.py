import sys 
sys.path.insert(0, '..')
import numpy as np
from init_cond.wavepacket import Wavepacket
from auxiliary.efft import ifft

class Gaussian6(Wavepacket):  # or does it??
    """Modified complex gaussian"""

    def __init__(self, eps, q0, p0, name, neqs = 1, space = None): # Space. Code style where you only pass parms
        """
        Parameters:

        --eps-- float
        --q0-- float: average position
        --eps-- float ...
        """
        super().__init__(name)
        
        self.q0 = q0
        self.p0 = p0
        self.eps = eps  # standard deviation??
        if space:
            #order matters
            self.__eval_psihat(space)
            self.__eval_psi(space)
            if neqs == 2:
                self.psi = np.stack((self.psi, np.zeros(space.n, dtype='complex_')))
                self.psihat = np.stack((self.psihat, np.zeros(space.n, dtype='complex_')))
        print('Initial wavepacket is a Gaussian: q0=%.2f, p0=%.2f, eps=%.3f' \
              %(q0, p0, eps))
        #self.eval_psi(Space)
        #self.eval_psihat(Space)
        
    def __eval_psi(self, space): # perhaps it is better as it was done before so that the user does not need to construct its axis...?
        """Evaluate gaussian on a grid"""

        self.psi = ifft(self, space)
        
    def __eval_psihat(self, space):
        """Evaluate gaussian in fourier space"""

        temp = np.exp(- (space.pgrid - self.p0)**6/4/self.eps)
        self.psihat = 1/np.sqrt(np.sum(temp**2)*space.dp) * temp

if __name__ == "__main__":

    import sys 
    sys.path.insert(0, '..')
    import numpy as np
    import matplotlib.pyplot as plt
    from auxiliary.space import Space

    P0 = 5
    Q0 = 0
    EPS = 1/30


    space = Space(2**14, -10, EPS, 10)
    wave = Gaussian6(EPS, Q0,P0,'gauss6', 1, space)
    
    print(np.sum(np.abs(wave.psi)**2)*space.dx )
    print(np.sum(np.abs(wave.psihat)**2)*space.dp)

    #plt.plot(space.xgrid, np.abs(wave.psi)**2)
    plt.plot(space.pgrid, (wave.psihat)**2)
    plt.xlim(P0 -2,P0 + 2)
    plt.ylabel('abs^2')
    #plt.xlabel('x')
    plt.xlabel('p')
    plt.show()
    plt.close('all')

