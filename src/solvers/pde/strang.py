import numpy as np
import scipy.linalg
from auxiliary import efft


class Strang:
    """Strang Splitting with Fourier step.  

    References
    ----------
    * [Shev MacNamara and Gilbert Strang, ****] Operator splitting
        https://www.math.ucla.edu/~wotaoyin/splittingbook/ch3-macnamara-strang.pdf
    To do: change Wave to eps
    """
    name = 'strang' # ideally this is what users would pass in to use this method?? or maybe not??

    def __init__(self, eps, Space, Time, Potential, neqs): # names and staff should be indepedent of the rest of the code/ proper of the method alone...
        """
        Parameters
        ---------
        n_eqs: int
            one level dynamics or two level dynamics
        """
        self.khalf, self.kfull, self.vfull = self.__get_opr(eps, Space,
                                                            Time, Potential,
                                                            neqs)
        # eigen summation subscript string 
        self.subscript = '...k, ...k -> ...k' if neqs == 1 else '...jk, k... -> j... ' # not great
            
        self.neqs = neqs
        print(self.neqs)

    def do_step(self, Wave, Space, itr, max_itr): # perhaps it should not be named psi either...? not proper of the method
        """
        @params:
        psi - half or full step depending on which dynamics we are running first.
        """
        if self.neqs != 1:
            Wave.psi = self.to_diab(Wave.psi)
            Wave.psihat = efft.fft(Wave, Space)
        if itr == 1:
        # evolve half a step
            self.__evolve(self.khalf, self.vfull, Wave, Space)
        # ...
        elif itr == max_itr:
            # last half step
            Wave.psihat = np.einsum(self.subscript, self.khalf, Wave.psihat)
            Wave.psi = efft.ifft(Wave,Space)
        else:
            # evolve half a step
            self.__evolve(self.kfull, self.vfull, Wave, Space)
           
        if self.neqs != 1:
            Wave.psi = self.to_adiab(Wave.psi)
            Wave.psihat = efft.fft(Wave, Space)
    
    def __evolve(self, k, v, Wave, Space):
        
        Wave.psihat = np.einsum(self.subscript, k, Wave.psihat)
        Wave.psi = efft.ifft(Wave,Space)
        Wave.psi = np.einsum(self.subscript, v, Wave.psi)
        Wave.psihat = efft.fft(Wave,Space)

    def __get_opr(self, eps, Space, Time, Potential, neqs):
        
        # half step - kinetic
        khalf_temp = np.exp(-1j*Time.dir *
                               Time.dt*Space.pgrid**2/(eps * 2)/2)
        # full step - kinetic
        kfull_temp = np.exp(-1j*Time.dir *
                               Time.dt*Space.pgrid**2/(eps * 2))
        if neqs == 1:  # one level
            vfull = np.exp(-1j*Time.dir*Time.dt * Potential.V(Space.xgrid)/eps)

            return (khalf_temp, kfull_temp, vfull)

        elif neqs == 2:  # two levels
            khalf, kfull, vfull = np.zeros(shape=(Space.n, 2, 2), dtype='complex_'), np.zeros(
                shape=(Space.n, 2, 2), dtype='complex_'), np.zeros(shape=(Space.n, 2, 2), dtype='complex_')
            khalf[:, 0, 0] = khalf_temp
            khalf[:, 1, 1] = khalf_temp
            kfull[:, 0, 0] = kfull_temp
            kfull[:, 1, 1] = kfull_temp
        
            U = Potential.u_diab(Space.xgrid)

            for i in range(Space.n):
                # potential. dynamics
                vfull[i] = scipy.linalg.expm(-1j*Time.dir*Time.dt *
                                                 U[i]/eps)  # full timestep
            # get to adiabatic transformation matrix
            self.A, self.D = Potential.get_chrepr(Space.xgrid)
            return (khalf, kfull, vfull)

    def to_diab(self, psi):

        return np.einsum(self.subscript, self.D, psi)

    def to_adiab(self, psi):

        return np.einsum(self.subscript, self.A, psi)

