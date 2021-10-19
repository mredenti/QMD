import sys
sys.path.insert(0, '..')
import numpy as np
from potentials.potential import Potential
# ------------- DIABATIC POTENTIALS ------------------
class LZ(Potential):

    def __init__(self, alpha, delta, level=None):
        super().__init__(level)
        
        self.name = 'landau zener'
        self.alpha = alpha
        self.delta = delta
        self.tau_c = self.get_tau()

    # ----------------- DIABATIC POTENTIAL --------------

    def v11(self, x):

        return self.alpha * x

    def v22(self, x):
        
        return - self.v11(x)

    def v12(self, x):

        return x - x + self.delta 

    def v21(self, x):

        return self.v12(x)
    
    def get_tau(self):
        """Check numerically"""
        
        a = self.alpha
        d = self.delta
        tau_c = np.pi * d**2 / 2 / a 
        
        return tau_c
# ------------- ADIABATIC POTENTIALS ------------------

    def V1(self, x): 
        """Check gradient"""    
        return x * 0
    
    def V2(self, x): 
            
        return x * 0

if __name__ == "__main__":

    pass
