import numpy as np
from init_cond.wavepacket import Wavepacket

class Gaussian(Wavepacket):  # or does it??
    """Complex valued Gaussian (I.C.)"""

    def __init__(self, eps, q0, p0, name, neqs = 1, space = None): # Space. Code style where you only pass parms
        """
        Parameters:

        --eps-- float
        --q0-- float: average position
        --eps-- float ...
        """
        super().__init__(name)
        
        self.q0 = q0
        self.p0 = p0
        self.eps = eps  # standard deviation??
        if space:
            self.__eval_psi(space)
            self.__eval_psihat(space)
            if neqs == 2:
                self.psi = np.stack((self.psi, np.zeros(space.n, dtype='complex_')))
                self.psihat = np.stack((self.psihat, np.zeros(space.n, dtype='complex_')))
        print('Initial wavepacket is a Gaussian: q0=%.2f, p0=%.2f, eps=%.3f' \
              %(q0, p0, eps))
        #self.eval_psi(Space)
        #self.eval_psihat(Space)
        
    def __eval_psi(self, space): # perhaps it is better as it was done before so that the user does not need to construct its axis...?
        """Evaluate gaussian on a grid"""

        self.psi = ((np.pi * self.eps)**(-.25) \
                * np.exp(- (space.xgrid - self.q0)**2/(2*self.eps)
               + 1j*self.p0*(space.xgrid - self.q0)/self.eps))
        
    def __eval_psihat(self, space):
        """Evaluate gaussian in fourier space"""

        self.psihat = ((np.pi * self.eps)**(-.25) * \
        np.exp(-1j*self.p0*self.q0/self.eps -
        (space.pgrid - self.p0)**2/(2*self.eps) - \
               1j*self.q0*(space.pgrid - self.p0)/self.eps))


if __name__ == "__main__":

    from mpl_toolkits import mplot3d
    import numpy as np
    import matplotlib.pyplot as plt

    P0 = 5
    Q0 = 0
    EPS = 1/50


    x, step = np.linspace(-10, 0, 10**4, retstep=True)
    wave = Gaussian(EPS, Q0,P0)
    wave.eval_psi(x) # I am not sure if this will work...?
    #print(np.sum(abs(psi)**2*step))

    fig = plt.figure(figsize=(14, 8))
    ax1 = fig.add_subplot(241)
    ax2 = fig.add_subplot(242)
    ax3 = fig.add_subplot(222)
    ax3D = fig.add_subplot(212, projection='3d')

    # plot the potential on the 3d plot
    ax1.plot(x, psi.real, label='real')
    ax1.set_xlim(q0 - 1, q0 + 1)
    ax2.set_xlim(q0 - 1, q0 + 1)
    ax2.plot(x, psi.imag, label='imag')
    ax2.axvline(x=- 5 + eps * np.pi / 2)
    ax3.plot(x, abs(psi), label=r'$|\Psi$|')
    ax3D.plot3D(x, psi.real, psi.imag, color='r')
    ax1.legend()
    ax2.legend()
    plt.show()
    plt.close('all')

    ##########
    eps = 0.001

    p, step = np.linspace(-20, 20, 10**3, retstep=True)
    psi_hat = wave.__eval_psi_hat(p)
    plt.plot(p, abs(psi_hat))
    # print(np.sum(abs(psi)**2)*step)
    plt.show()
    plt.close('all')
