import sys 
sys.path.insert(0, '../src/')
from init_cond.gaussian import Gaussian
from auxiliary.space import Space
from auxiliary.time import Time
from auxiliary.efft import ifft
from potentials.examples.single import Single
from solvers.pde.strang import Strang
import matplotlib.pyplot as plt 
import numpy as np
# ------------------- PARAMETERS ----------------
# init wave params  
EPS, Q0, P0 = 1/10, -5, 3   
# potential parameters
DELTA, C, ALPHA = 0.5, -np.pi, np.pi
# space    
XL, XR = -20, 20
N = 2**14
# time
T, TSTEP, TDIR= 10/P0, 1/100/P0, 1
NEQS = 1

# ---------------- INIT -------------------------
space = Space(N, XL, EPS, XR)
time = Time(T, TSTEP, TDIR)
wave_boa = Gaussian.init(EPS, Q0, P0, NEQS, space) # init psi and psi hat
potential = Single(DELTA, C, ALPHA,  'up')
solver = Strang(wave_boa, space, time, potential, NEQS)
wave_boa_two = Gaussian.init(EPS, Q0, P0, 2, space) # init psi and psi hat
solver_two = Strang(wave_boa, space, time, potential, 2) 
