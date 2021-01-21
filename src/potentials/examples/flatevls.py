import sys
sys.path.insert(0, '..')
import numpy as np
from potentials.potential import Potential
# ------------- DIABATIC POTENTIALS ------------------
class FlatEvls(Potential):

    def __init__(self, delta, q_c, level):
        """Parameters
            - delta: constant eigenvalue (surface)
        """
        super().__init__(level)
        
        self.name = 'flatevls'
        self.delta = delta
        self.q_c = q_c
    # ----------------- DIABATIC POTENTIAL --------------

    def v1(self, x):

        return self.delta * np.cos(self.theta(x))
    
    def v2(self, x):

        return - self.v1(x)

    def v12(self, x):

        return self.delta * np.sin(self.theta(x))
    
    # up from here should be inherited...

    def theta(self, x):

        return np.arctan(x/self.q_c) # arctan2...?
    
    def rho(self, x):

        return x - x + self.delta

    def V(self, x): # if called multiple times then set up differently
        # adiabatic surfaces
        print('Flat eigenvalues')
        sign = 1 if self.level == 'up' else -1
        
        return x - x + sign * self.delta

    def gap(self,x):

        return 2*self.delta
# ------------- ADIABATIC POTENTIALS ------------------

    def V1(self, x):
        
        sys.exit('Constant eigenvalues potential. Gradient \
                    not yet implemented')
        return None
    
    def V2(self, x): 
        
        sys.exit('Constant eigenvalues potential. Hessian \
                    not yet implemented')
        
        return None 

    def get_tau(self):
        
        return 2*self.delta*self.q_c 
    
    def get_qc(self):
        
        return self.q_c 

    def get_gamma(self):
        
        return - self.q_c/2

if __name__ == "__main__":

    import matplotlib.pyplot as plt

    DELTA = 0.2
    Q_C = 0.1
    LEVEL = 'up'

    x = np.linspace(-10, 10, 10**2)
    pot = FlatEvls(DELTA, Q_C, LEVEL)
    
    plt.plot(x, pot.V(x))
    plt.show()
    plt.close('all')



