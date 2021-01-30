import numpy as np
from abc import ABC, abstractmethod

class Potential(ABC): # GOOD IDEA: SET UP A BASE CLASS FOR EVERYONE TO EXTEND UPON?
    """
    Raises
    ------
    NotImplementedError
        If no level is set for adiabatic potential
        energy surface.
    """

    def __init__(self, level, formula = 'LZ'):
        """
        level is a string

        Parameters: Class
            Contains parameters for potential
        """
        if  level == 'up' or 'down':
            self.level = level
        else:
            raise NotImplementedError(
                'Please specify upper or lower potential \
                Set up/down in level attribute')

    @abstractmethod
    def v11(self, x):
        pass
    
    @abstractmethod
    def v22(self, x):
        pass
    
    @abstractmethod
    def v12(self, x):
        pass
    
    @abstractmethod
    def v21(self, x):
        pass
    
    @abstractmethod
    def theta(self, x):
        pass
    
    @abstractmethod
    def rho(self, x):
        pass
    
    @abstractmethod
    def d(self, x):
        pass
    
    @abstractmethod
    def get_tau(self):
        pass

    """
    def X(self, x):
        
        return self.v12(x)

    def Z(self, x):
        # half gap between Diabatic surfaces
        return (self.v1(x) - self.v2(x)) / 2

    def d(self, x):
        # average between Diabatic surfaces
        return (self.v1(x) + self.v2(x))/2
    
    def rho(self, x):

        return np.sqrt(self.X(x)**2 + self.Z(x)**2)
    """
    def gap(self, x):
        # gap between Adiabatic surfaces
        return 2 * self.rho(x)

    def V(self, x): # if called multiple times then set up differently
        # adiabatic surfaces
        sign = 1 if self.level == 'up' else -1

        return self.d(x) + sign * self.rho(x)
    
    def u_diab(self, x):

        s = np.ones(shape = (len(x), 2, 2))
        s[:,0,0] = self.rho(x)*self.v11(x) + self.d(x)
        s[:,1,1] = self.rho(x)*self.v22(x) + self.d(x) # sign thing?
        s[:,0,1] = self.rho(x)*self.v12(x) 
        s[:,1,0] = self.rho(x)*self.v21(x)

        return s
    
    #"""
    def get_chrepr(self, x):
        Z = self.v11(x)
        X = self.v12(x)

        theta = np.arctan2(X,Z)
        
        D = np.ones(shape=(len(x), 2, 2), dtype=np.complex128)
        D[:, 0, 0] = np.cos(self.theta(x)/2) #*np.exp(1j*theta/2)
        D[:, 1, 0] = np.sin(self.theta(x)/2) #*np.exp(1j*theta/2)
        D[:, 0, 1] = np.sin(self.theta(x)/2) #*np.exp(1j*theta/2)
        D[:, 1, 1] = -np.cos(self.theta(x)/2) #*np.exp(1j*theta/2)
        # to adiabatic matrix
        A = np.ones(shape=(len(x), 2, 2), dtype=np.complex128)
        A = D
        
        return (A, D)
    
    """
    def get_chrepr(self, x):
        
        Z = self.v11(x)
        X = self.v12(x)
        
        phi1Plus = (Z + np.sqrt(Z**2 + X**2))/X # x is non-zero for the example considered so far...
        phi2Plus = (Z - np.sqrt(Z**2 + X**2))/X
        phi1Minus = np.ones(len(phi1Plus))
        phi2Minus = np.ones(len(phi2Plus))
        k1 = 1/np.sqrt(phi1Plus**2 + phi1Minus**2)
        k2 = 1/np.sqrt(phi2Plus**2 + phi2Minus**2)
        
        D = np.ones(shape=(len(x), 2, 2), dtype=np.complex128)
        D[:, 0, 0] = phi1Plus * k1
        D[:, 1, 0] = phi1Minus * k1
        D[:, 0, 1] = k2 * phi2Plus
        D[:, 1, 1] = k2 * phi2Minus
        # to adiabatic matrix
        A = np.ones(shape=(len(x), 2, 2), dtype=np.complex128)
        A[:, 0, 0] = phi1Plus * k1
        A[:, 0, 1] = phi1Minus * k1
        A[:, 1, 0] = k2 * phi2Plus
        A[:, 1, 1] = k2 * phi2Minus

        return (A, D)
        """
if __name__ == '__main__':

    pass

