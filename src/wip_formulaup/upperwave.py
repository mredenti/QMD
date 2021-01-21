import sys 
sys.path.insert(0, '..')
from init_cond.gaussian import Gaussian
from auxiliary.space import Space
from auxiliary.time import Time
from auxiliary.error import norm2, relerror2
from auxiliary.efft import ifft
from potentials.examples.simple import Simple
from solvers.pde.strang import Strang
import matplotlib.pyplot as plt 
import numpy as np


# ------------------- PARAMETERS ----------------
# init wave params
EPS, Q0, P0 = 1/10, -10, 5 
# space    
XL, XR = -30, 30
N = 2**14
# time
T, TSTEP, TDIR= 20/P0, 1/100/P0, 1
#potential params
ALPHA, DELTA = 0.5, 0.5 
LEVEL = 'up'
NEQS = 2
# ---------------- INIT -------------------------
space = Space(N, XL, EPS, XR)
time = Time(T, TSTEP, TDIR)
wave_exact = Gaussian.init(EPS, Q0, P0, NEQS, space) # init psi and psi hat
wave_boa = Gaussian.init(EPS, Q0, P0, 1, space) # init psi and psi hat
potential = Simple(ALPHA, DELTA, LEVEL)
solver_exact = Strang(wave_exact, space, time, potential, NEQS)
solver_boa = Strang(wave_boa, space, time, potential, 1)


# ----------------- RUN -----------------------
snap = [i for i in range(0,time.max_itr,int(time.max_itr/10))]


def run(time):
    
    f = open('./data/wavedelta%.3feps%.3fp%d.txt' %(DELTA, EPS, P0), 'w')
    f.write("xgrid \t psiboa+_real \t psiboa+_imag \t \
             psiexact+_real \t psiexact+_imag \t \
             pgrid \t psihatboa+_real \t psiboa+_imag \t \
             psihatexact+_real \t psihatexact+_imag \n")
        
    crossed = False
    for itr in range(1, time.max_itr):
        
        solver_exact.do_step(wave_exact, space, itr, time.max_itr)
        solver_boa.do_step(wave_boa, space, itr, time.max_itr)
        # check if wave-packet's CoM has reached crossing
        """
        if itr in snap:
            plt.plot(space.pgrid, np.arctan2(wave_boa.psihat.imag, wave_boa.psihat.real))
            plt.plot(space.pgrid, np.arctan2(wave_exact.psihat[0,:].imag, wave_exact.psihat[0,:].real))
            plt.xlim(P0 - 0.5, P0 + 0.5)
            plt.show()
            plt.close()
        """ 
        if not crossed:
            if wave_boa.get_meanx(space) > 0:
                delta = potential.delta
                eps = wave_boa.eps
                v = np.zeros(len(space.pgrid), dtype = 'complex_')
                mask = space.pgrid != 0
                tau_c = potential.get_tau()
                v[mask] = np.sign(space.pgrid[mask]) * \
                        np.sqrt(space.pgrid[mask]**2 + 4*delta)
                v[mask] = - (space.pgrid[mask] + v[mask])**2 /(4 * space.pgrid[mask]*v[mask])  * \
                        np.exp(- tau_c/(delta * eps) * \
                               abs(v[mask] - space.pgrid[mask]))
                boa_hat = wave_boa.psihat.copy()
                wave_boa.psihat = wave_boa.psihat + v * wave_boa.psihat
                wave_boa.psi = ifft(wave_boa, space)
                crossed = True
                plt.plot(space.pgrid, abs(wave_boa.psihat))
                plt.plot(space.pgrid, abs(wave_exact.psihat[0,:]))
                plt.plot(space.pgrid, abs(boa_hat))
                plt.xlim(P0-1, P0+1)
                plt.show()
                plt.close('all')
        print('%.2f %%' % (itr/(time.max_itr - 1) * 100), end='\r')
       
    np.savetxt(f, np.c_[space.xgrid,
                        wave_boa.psi.real,
                        wave_boa.psi.imag,
                        wave_exact.psi[0,:].real,
                        wave_exact.psi[0,:].imag,
                        space.pgrid, 
                        wave_boa.psihat.real,
                        wave_boa.psihat.imag,
                        wave_exact.psihat[0,:].real,
                        wave_exact.psihat[0,:].imag],
                        delimiter = '\t')
    f.close()

    ######## RUN SCRIPT #########
run(time)
