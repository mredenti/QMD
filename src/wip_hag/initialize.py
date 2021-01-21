import sys 
sys.path.insert(0, '..')
import setup
from init_cond.hagwave import HagWave
from auxiliary.space import Space
from auxiliary.time import Time
from potentials.potential import Potential
from solvers.ode.strang import Strang
import matplotlib.pyplot as plt 
import numpy as np

# ---------------- INIT -------------------------
class PARAM:
    alpha = setup.ALPHA
    delta = setup.DELTA
    level = setup.LEVEL
space = Space(setup.N, setup.XL, setup.EPS, setup.XR)
time = Time(setup.T, setup.TSTEP, setup.TDIR)
wave = HagWave(setup.EPS, setup.q0, setup.p0, setup.Q0, setup.P0, setup.c0, setup.NEQS) # init psi and psi hat
potential = Potential(setup.POTENTIAL_NAME, PARAM, PARAM.level)
solver = Strang()

