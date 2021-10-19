"""This is a module for our Wavepacket class.
.. moduleauthor: Michael Redenti <M.Redenti@sms.ed.ac.uk>
"""
import numpy as np


class Wavepacket:
    """Stores the wavepacket in its different representations.
    """
    def __init__(self, name):
        """shdj.

        :param name: first name
        :type name: str
        """
        self.name = name
        #self.eps = eps
        # init dynamics always in adiabatic representation # always needs to
        #have an up to date adiabatic and diabatic representation
        self.repr = 'adia'
        self.psi = None
        self.psihat = None
        # following the mathematical logic/defn of a function acting on a domain
        print('Wavepacket initialised')
    
    def __change_repr(self, change_mat):  # choose a better name
        """Returns diabatic/adiabatic representation of wavepacket.

        :returns: self -- numpy array

        Assuming two states/levels system. 
        """
        assert change_mat.shape[1:] == (
            2, 2), "Dimensions/axis CoR matrix should be (n_points, 2, 2)"

        self.repr = 'dia' if self.repr == 'adia' else 'adia'

        return np.einsum('...jk, k... -> j... ', change_mat, self.psi)

    def get_massx(self, space): 
        # should i not have a sqrt here?
        if len(self.psi.shape) == 1:
            return np.sum(abs(self.psi)**2)*space.dx
        else:   
            return np.sum(abs(self.psi)**2, axis=1)*space.dx

    def get_massp(self, space):

        if len(self.psihat.shape) == 1:
            return np.sum(abs(self.psihat)**2)*space.dp
        else:
            return np.sum(abs(self.psihat)**2, axis=1)*space.dp

    def get_meanx(self, space):

        if len(self.psi.shape) == 1:
            return np.sum(abs(self.psi)**2 * space.xgrid)*space.dx / \
                    (np.sum(abs(self.psi)**2)*space.dx)
        else:   
            return np.sum(abs(self.psi)**2 * space.xgrid, axis=1)*space.dx / \
                    (np.sum(abs(self.psi)**2, axis=1)*space.dx)

    def get_meanp(self, space):

        if len(self.psi.shape) == 1:
            return np.sum(abs(self.psihat)**2 * space.pgrid)*space.dp / \
                    (np.sum(abs(self.psihat)**2)*space.dp)
        else:   
            return np.sum(abs(self.psihat)**2 * space.pgrid, axis=1)*space.dp / \
                    (np.sum(abs(self.psihat)**2, axis=1)*space.dp)
    
    def get_ke(self, space):
        
        if len(self.psi.shape) == 1:
            return 1/2 * np.sum(abs(self.psihat)**2 * space.pgrid**2)*space.dp / \
                    (np.sum(abs(self.psihat)**2)*space.dp)
        else:   
            return 1/2 * np.sum(abs(self.psihat)**2 * space.pgrid**2, axis=1)*space.dp / \
                    (np.sum(abs(self.psihat)**2, axis=1)*space.dp)
    
    def get_e(self, space, potential):
        
        ke = self.get_ke(space)
        if len(self.psi.shape) == 1:
            return np.sum(abs(self.psi)**2 * potential.V(space.xgrid))*space.dx / \
                    (np.sum(abs(self.psi)**2)*space.dx) + ke
        else:   
            return np.sum(abs(self.psi)**2 * potential.u_adiab(space.xgrid), axis=1)*space.dx / \
                    (np.sum(abs(self.psi)**2, axis=1)*space.dx) + ke

if __name__ == "__main__":

    pass
