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
    def get_tau(self, x):
        pass

    def d(self, x):
        """Average diagonal surfaces"""
        return (self.v11(x) + self.v22(x))/2

    def Z(self, x):
        """Half gap diagonal terms"""
        return (self.v11(x) - self.v22(x))/2
    
    def Zd(self, x):
        """Half gap diagonal terms"""
        return (self.v11d(x) - self.v22d(x))/2
    
    def Zdd(self, x):
        """Half gap diagonal terms"""
        return (self.v11dd(x) - self.v22dd(x))/2
    
    def rho(self, x):
        """Eigenvalue
        """
        return np.sqrt(self.Z(x)**2 + self.v12(x)**2)

    def rho_complex_arg(self, x):
        """Eigenvalue"""
        return [np.sqrt(self.Z(x[0] + 1j*x[1])**2 + self.v12(x[0] + 1j*x[1])**2).real,
                np.sqrt(self.Z(x[0] + 1j*x[1])**2 + self.v12(x[0] + 1j*x[1])**2).imag]
    
    def rho_complex_arg2(self, x, y):
        """Eigenvalue"""
        return np.sqrt(self.Z(x + 1j*y)**2 + self.v12(x + 1j*y)**2).real + \
                1j * np.sqrt(self.Z(x + 1j*y)**2 + self.v12(x + 1j*y)**2).imag
    
    def theta(self, x):

        return np.arctan2(self.v12(x),  self.Z(x))
    
    def V(self, x): # if called multiple times then set up differently
        # adiabatic surfaces
        sign = 1 if self.level == 'up' else -1

        return self.d(x) + sign * self.rho(x)
    
    def u_diab(self, x): # do i need to change this if i have zero trace? what is this?

        s = np.ones(shape = (len(x), 2, 2))
        s[:,0,0] = self.v11(x) 
        s[:,1,1] = self.v22(x) 
        s[:,0,1] = self.v12(x)  
        s[:,1,0] = self.v21(x) 

        return s
    
    def u_adiab(self, x):

        s = np.ones(shape = (2, len(x)))
        s[0,:] = self.rho(x) + self.d(x)
        s[1,:] = - self.rho(x) + self.d(x) # sign thing?

        return s
    
    def u_adiab(self, x):

        s = np.ones(shape = (2, len(x)))
        s[0,:] = self.rho(x) #self.rho(x)*self.v11(x) + self.d(x)
        s[1,:] = - self.rho(x) #self.rho(x)*self.v22(x) + self.d(x) # sign thing?

        return s
    """
    def get_chrepr(self, x):
        
        #Z = self.v11(x)
        #X = self.v12(x)
        #theta = np.arctan2(X,Z)
        
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
        
        Z = (self.v11(x) - self.v22(x)) / 2 # this may need to be changed
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

if __name__ == '__main__':

    pass

