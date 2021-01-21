import numpy as np
# ------------------- PARAMETERS ----------------
# init wave params
EPS, q0, p0 = 1/10, -10, 5 
Q0 , P0 = 1, 1j
w = 1/np.sqrt(3)
c0 = np.array([1, 0, 0])
# space    
XL, XR = -30, 30
N = 2**14
# time
T, TSTEP, TDIR= 20/p0, 1/100/p0, 1
#potential params
ALPHA, DELTA = 0.5, 0.5 
LEVEL = 'up'
NEQS = 1
POTENTIAL_NAME = 'simple'

