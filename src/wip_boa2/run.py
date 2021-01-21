import sys 
sys.path.insert(0, '..')
from init_cond.gaussian import Gaussian
from auxiliary.space import Space
from auxiliary.time import Time
from auxiliary.error import norm2, relerror2
from auxiliary.efft import ifft
from potentials.examples.simple2 import Simple2
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
ALPHA, DELTA = 0.5, 0.05 
LEVEL = 'up'
NEQS = 2
# ---------------- INIT -------------------------
space = Space(N, XL, EPS, XR)
time = Time(T, TSTEP, TDIR)
wave_exact = Gaussian.init(EPS, Q0, P0, NEQS, space) # init psi and psi hat
wave_boa2 = Gaussian.init(EPS, Q0, P0, 1, space) # init psi and psi hat
wave_boa = Gaussian.init(EPS, Q0, P0, 1, space) # init psi and psi hat
potential2 = Simple2(ALPHA, DELTA, LEVEL, EPS)
potential = Simple(ALPHA, DELTA, LEVEL)
solver_exact = Strang(wave_exact, space, time, potential, NEQS)
solver_boa2 = Strang(wave_boa2, space, time, potential2, 1)
solver_boa = Strang(wave_boa, space, time, potential, 1)
# data object with a save function - one for ode and one for pde functioin so 
# that the order is fixed
# -------------- Order e^2 correction to potential --------------
print('Modified potential - Adding O(e^2) diagonal correction for BOA')

# ----------------- RUN -----------------------
snap = [i for i in range(0,time.max_itr,int(time.max_itr/10))]


def run(time):
    
    f = open('./data/order2delta%.3feps%.3fp%d.txt' %(DELTA, EPS, P0), 'w')
    f.write("xgrid \t psiboa2+_real \t psiboa2+_imag \t \
             psiexact+_real \t psiexact+_imag \t \
             pgrid \t psihatboa2+_real \t psihatboa2+_imag \t \
             psihatexact+_real \t psihatexact+_imag \t \
             \t psihatboa_real \t psihatboa_imag \n ")
        
    crossed = False
    for itr in range(1, time.max_itr):
        
        solver_exact.do_step(wave_exact, space, itr, time.max_itr)
        solver_boa2.do_step(wave_boa2, space, itr, time.max_itr)
        solver_boa.do_step(wave_boa, space, itr, time.max_itr)
        # check if wave-packet's CoM has reached crossing
        print('%.2f %%' % (itr/(time.max_itr - 1) * 100), end='\r')
       
    np.savetxt(f, np.c_[space.xgrid,
                        wave_boa2.psi.real,
                        wave_boa2.psi.imag,
                        wave_exact.psi[0,:].real,
                        wave_exact.psi[0,:].imag,
                        space.pgrid, 
                        wave_boa2.psihat.real,
                        wave_boa2.psihat.imag,
                        wave_exact.psihat[0,:].real,
                        wave_exact.psihat[0,:].imag,
                        wave_boa.psihat.real,
                        wave_boa.psihat.imag],
                        delimiter = '\t')
    f.close()

    ######## RUN SCRIPT #########
run(time)
