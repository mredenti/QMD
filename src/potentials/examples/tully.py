import sys
sys.path.insert(0, '..')
import numpy as np
from potentials.potential import Potential
# ------------- DIABATIC POTENTIALS ------------------
class Tully(Potential):

    def __init__(self, a, b, c, d, level):
        """Parameters
            - a: coupling parameter?
            - b: coupling parameters
            - c: coupling parameters
            - d: coupling parameters
        """
        super().__init__(level)
        
        self.name = 'Tully potential (1d)'
        self.a = a 
        self.b = b
        self.c = c
        self.d_ = d
    
    # ----------------- DIABATIC POTENTIAL --------------
    def d(self, x):

        return x - x
    
    def rho(self, x):

        return np.sqrt(self.Z(x)**2 + self.X(x)**2)

    def v11(self, x):

        return self.Z(x) / self.rho(x)
    
    def v22(self, x):

        return - self.v11(x)

    def v12(self, x):

        return self.X(x) / self.rho(x)
    
    def v21(self, x):

        return self.v12(x)
    # up from here should be inherited...

    def Z(self, x):

        return self.a * np.sign(x) * (1 - np.exp(-self.b*np.abs(x)))

    def X(self, x):

        return self.c * np.exp(-self.d_ * x**2)

# ------------- ADIABATIC POTENTIALS ------------------

    def V1(self, x):
        
        sys.exit('Tully potential. Gradient \
                    not yet implemented')
        return None
    
    def V2(self, x): 
        
        sys.exit('Tully potential. Hessian \
                    not yet implemented')
        
        return None 

    def get_gamma(self):
        
        sys.exit('Tully potential. No gamma given')
    
    def get_qc(self):
        
        sys.exit('Tully potential. No qc given')
    
    def get_tau(self):
        
        sys.exit('Tully potential. No tau given')

    def get_a(self):
        
        return self.a

    def get_b(self):
        
        return self.b

    def get_c(self):
        
        return self.c
    
    def get_d(self):
        
        return self.d_

if __name__ == '__main__':

    import matplotlib.pyplot as plt

    x = np.arange(5,20,0.1)
    tully = Tully(1, 1, 0.005, 1, 'up')
    plt.plot(x, (1 - tully.v11(x))/tully.v12(x))
    #plt.plot(x, tully.v12(x))
    print(tully.X(x))
    plt.show()
    plt.close('all')
