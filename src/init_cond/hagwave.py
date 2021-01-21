import numpy as np
from init_cond.wavepacket import Wavepacket

class HagWave(Wavepacket):  # or does it??
    """Complex valued Gaussian (I.C.)"""

    def __init__(self, eps, q0, p0, Q0, P0, c0, neqs): # Space. Code style where you only pass parms
        """
        Parameters:

        --eps-- float
        --q0-- float: average position
        --eps-- float ...
        """
        super().__init__()
        self.name = 'hagedorn' # check it does not override parent class name
        self.q = q0
        self.p = p0
        self.Q = Q0
        self.P = P0
        self.S = 0
        self.c = c0
        self.eps = eps  # standard deviation??
        self.detQ = np.sqrt(Q0) 
        #self.eval_psi(Space)
        #self.eval_psihat(Space)
        print('Hagedorn wavepacket. q0=%.1f, p0=%.1f, Q0=%.1f'
              %(q0, p0, Q0))
        
    def get_psi(self, space): # perhaps it is better as it was done before so that the user does not need to construct its axis...?
        """Evaluate gaussian on a grid"""

        # recall that the parameters and weigths alone may be evolves
        phase = np.exp(1j * self.S/self.eps) 
        y = space.xgrid - self.q

        return phase * self.phi_0(space.xgrid, self.q, self.p, self.Q, self.P) * \
                (self.c[0] + self.c[1]*np.sqrt(2/self.eps)*y \
                 + self.c[2]/np.sqrt(2) * (2/self.eps*y**2 - 1)) 

    def get_psihat(self, space):
        """Evaluate gaussian in fourier space"""
        phase = np.exp(1j * self.S/self.eps - 1j * self.p * self.q / self.eps) 
        y = space.xgrid - self.p

        return phase * self.phi_0(space.xgrid, self.p, - self.q, self.P, -self.Q) * \
                (self.c[0] + self.c[1]*np.sqrt(2/np.eps)*y \
                 + self.c[2]/np.sqrt(2) * (2/self.eps*y**2 - 1)) 

    def phi_0(self, x, q, p, Q, P):
        
        # return gaussian
        return (self.detQ)**(-.5) * (np.pi * self.eps)**(-.25) \
                * np.exp(1j/(2*self.eps) * (x - q)**2 * P*(1/Q) + 1j/self.eps * p * (x - q) )

