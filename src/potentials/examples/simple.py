import sys
sys.path.insert(0, '..')
import numpy as np
from potentials.potential import Potential
# ------------- DIABATIC POTENTIALS ------------------
class Simple(Potential):

    def __init__(self, alpha, delta, level=None):
        super().__init__(level)
        
        self.name = 'simple'
        self.alpha = alpha
        self.delta = delta
        self.tau_c = self.get_tau()

    # ----------------- DIABATIC POTENTIAL --------------

    def v1(self, x):

        return self.alpha * np.tanh(x)

    def v2(self, x):
        
        return - self.v1(x)

    def v12(self, x):

        return x - x + self.delta 

# ------------- ADIABATIC POTENTIALS ------------------

    def V1(self, x): 
            
        sign = 1 if self.level == 'up' else -1
        s = np.tanh(x)
            
        return sign * self.alpha**2 * s *(1 - s**2)/self.rho(x)
    
    def V2(self, x): 
        
        a = self.alpha
        s = np.tanh(x)
        sign = 1 if self.level == 'up' else -1
            
        return sign *( (-2) * a**2 * s**2 * (1 - s**2)/self.rho(x) \
                      + a**2 * (1 - s**2)**2/self.rho(x) \
                      - a**4 * s**2 * (1 - s**2)**2/self.rho(x)**3)
    
    def get_tau(self):
        
        a = self.alpha
        d = self.delta
        tau_c = 2 * np.sqrt(a**2 + d**2) * \
                (np.arctan(a/d) +np.arctan(d/a)) - a*np.pi
        
        return tau_c

if __name__ == "__main__":

    pass
