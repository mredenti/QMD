import sys
sys.path.insert(0, '..')
import numpy as np
from potentials.potential import Potential
# ------------- DIABATIC POTENTIALS ------------------
class Single(Potential):

    def __init__(self, delta, c, alpha, level):
        """Parameters
            - delta: constant eigenvalue (surface)
            - alpha: coupling parameters
            - c: coupling parameters
        """
        super().__init__(level)
        
        self.name = 'Single - flatevls'
        self.delta = delta 
        self.c = c
        self.alpha = alpha
    
    # ----------------- DIABATIC POTENTIAL --------------
    def d(self, x):

        return x - x
    
    def rho(self, x):

        return x - x + self.delta

    def v11(self, x):

        return np.cos(self.theta(x))
    
    def v22(self, x):

        return -self.v11(x)

    def v12(self, x):

        return np.sin(self.theta(x))
    
    def v21(self, x):

        return self.v12(x)
    # up from here should be inherited...

    def theta(self, x):

        return self.c/self.alpha * np.arctan(np.tanh(self.alpha*x/2))

    def theta_prime(self, x):

        return self.c/2/np.cosh(self.alpha*x)

# ------------- ADIABATIC POTENTIALS ------------------

    def V1(self, x):
        
        sys.exit('Constant eigenvalues potential. Gradient \
                    not yet implemented')
        return None
    
    def V2(self, x): 
        
        sys.exit('Constant eigenvalues potential. Hessian \
                    not yet implemented')
        
        return None 

    def get_gamma(self):
        
        return - self.c/2/self.alpha
    
    def get_qc(self):
        
        return np.pi/2/self.alpha 
    
    def get_tau(self):
        
        print('You have not defined this yet')

    def get_c(self):
        
        return self.c

    def get_alpha(self):

        return self.alpha


if __name__ == "__main__":

    import matplotlib.pyplot as plt

    DELTA = 0.5
    C = -np.pi
    ALPHA = np.pi
    LEVEL = 'up'

    x = np.linspace(-10, 10, 10**2)
    pot = Single(DELTA, C, ALPHA, LEVEL)

    plt.plot(x, pot.theta_prime(x))
    plt.xlabel('x')
    plt.ylabel('coupling (theta prime)')
    plt.show()
    plt.close('all')



