
def angle(z1, z2):
    "angle of the difference would be wrong - consider the case of two \
            vectors with the same phase and of different lenghts"
    diff = abs(np.arctan2(z1.imag, z1.real) - np.arctan2(z2.imag, z2.real))
    #return np.min(diff, 2*np.pi - diff)
    return diff

if __name__ == '__main__':
    import sys 
    sys.path.insert(0, '..')
    from init_cond.gaussian import Gaussian
    from auxiliary.space import Space
    from auxiliary.time import Time
    from auxiliary.efft import ifft
    from auxiliary.data import Data
    from potentials.examples.tully import Tully
    from solvers.pde.strang import Strang
    import numpy as np
    import matplotlib.pyplot as plt
    # ------------------- PARAMETERS ----------------
    # init wave params - reason behind 2 - see paper initial condition 
    EPS, Q0, P0 = 1/10, -10, 4 # momentums 2 and 5 in the paper 
    A, B, C, D = 1, 1, 0.005, 1
    # space    
    XL, XR = -30, 30
    N = 2**14
    # time
    T, TSTEP, TDIR= 20/P0, 1/100/P0, 1
    #potential params
    FNAME = './tullya%.3fb%.3fc%.3fd%.3feps%.3fp%d.txt' %(A, B, C, D, EPS, P0)
    # ---------------- INIT -------------------------
    space = Space(N, XL, EPS, XR)
    time = Time(T, TSTEP, TDIR)
    potential = Tully(A, B, C, D,  'up')
    wave = Gaussian(EPS, Q0, P0, 'exact') # init psi and psi hat
    wave_boa = Gaussian(EPS, Q0, P0, 'boa', 1, space) # init psi and psi hat
    solver = Strang(EPS, space, time, potential, 2)
    solver_boa = Strang(EPS, space, time, potential, 1)

    # ---------------- RUN BACKWARD ------------------
    wave.psi = np.stack((wave_boa.psi.copy(), np.zeros(space.n, dtype='complex_')))
    # ----------------- RUN -----------------------
    for itr in range(1, time.max_itr + 1):
        # this should return, amongst else, boa at the crossing
        solver.do_step(wave, space, itr, time.max_itr)
        solver_boa.do_step(wave_boa, space, itr, time.max_itr)
        print('%.2f %%' % (itr/(time.max_itr) * 100), end='\r')

    plt.plot(space.xgrid, abs(wave_boa.psi))
    plt.plot(space.xgrid, abs(wave.psi[0,:]))
    plt.plot(space.xgrid, abs(wave.psi[1,:]))
    np.savetxt('wave', wave.psi[0,:])
    plt.show()
    plt.close()
    plt.plot(space.xgrid, angle(wave_boa.psi, wave.psi[0,:]))
    plt.xlim(5,20)
    plt.show()
    plt.close()

    # I would say to simply compute the phase difference without too much hassle
