"""
Variation of simple potential. Testing constant phase effect.
"""
import sys
sys.path.insert(0, '..')
import numpy as np
from potentials.examples.simple import Simple


class Simple2(Simple):
    """
    Intruduce eps^2 term in adiabatic potential"
    """
    def __init__(self, alpha, delta, level, eps):
        super().__init__(alpha, delta, level)

        self.name = 'Simple with O(eps^2) correction'
        self.eps = eps
    def V(self, x):
        
        print('Using modified potential')
        sign = 1 if self.level == 'up' else -1

        return self.d(x) + sign * self.rho(x) + \
                self.eps**2 * (-self.delta * self.alpha * \
                               (1 - np.tanh(x)**2) /self.rho(x)**2)**2/8
