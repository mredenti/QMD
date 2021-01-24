
def angle(z1, z2):
    "angle of the difference would be wrong - consider the case of two \
            vectors with the same phase and of different lenghts"
    diff = abs(np.arctan2(z1.imag, z1.real) - np.arctan2(z2.imag, z2.real))
    #return np.min(diff, 2*np.pi - diff)
    return diff

def run_backward(time, solver, wave):

    for itr in range(1, time.max_itr + 1):
        
        solver.do_step(wave, space, itr, time.max_itr)
        print('%.2f %%' % (itr/(time.max_itr) * 100), end='\r')

def run(time):
   
    snap = [i for i in np.arange(1,time.max_itr, time.max_itr//20)]
    crossed = False
    for itr in range(1, time.max_itr + 1):
        # this should return, amongst else, boa at the crossing
        solver.do_step(wave, space, itr, time.max_itr)
        """
        if itr in snap:
            plt.plot(space.xgrid, abs(wave.psi[0,:]))
            plt.plot(space.xgrid, abs(wave.psi[1,:]), label = 'down')
            plt.legend()
            plt.show()
            plt.close()
        """
        print('%.2f %%' % (itr/(time.max_itr) * 100), end='\r')
        if not crossed:
            solver_boa.do_step(wave_boa, space, itr, time.max_itr)
            com = wave_boa.get_meanx(space)
            if com > 0: # NEED TO CHANGE HOW TO COMPUTE FORMULA
                q_c = potential.get_qc()
                gamma = potential.get_gamma()
                wave_formuladown.psihat = superadiabatic.get_transition(
                                                wave_boa.psihat, space, 
                                                wave_boa.eps, q_c,
                                                DELTA, gamma)
                # need to change this and make 
                wave_formulaup.psihat = wave_boa.psihat + \
                        superadiabatic.get_correction(wave_boa.psihat, space,
                                                      wave_boa.eps, q_c,
                                                      DELTA, gamma, P0) 
                
                wave_formuladown.psi = ifft(wave_formuladown, space) 
                wave_formulaup.psi = ifft(wave_formulaup, space) 
                crossed = True
        
    
    wave_exactup.psi = wave.psi[0,:].copy()
    wave_exactdown.psi = wave.psi[1,:].copy()
    wave_exactup.psihat = wave.psihat[0,:].copy()
    wave_exactdown.psihat = wave.psihat[1,:].copy()
    
    run_backward(time_back, solver_exactup, wave_exactup)
    run_backward(time_back, solver_exactdown, wave_exactdown)
    
    return (wave_boa, wave_formuladown, wave_formulaup, wave_exactdown, wave_exactup)

if __name__ == '__main__':
    import sys 
    sys.path.insert(0, '..')
    from init_cond.gaussian import Gaussian
    from auxiliary.space import Space
    from auxiliary.time import Time
    from auxiliary.efft import ifft
    from auxiliary.data import Data
    from potentials.examples.single import Single
    from solvers.pde.strang import Strang
    from transition_formulae import superadiabatic 
    import matplotlib.pyplot as plt 
    import numpy as np
    # ------------------- PARAMETERS ----------------
    # init wave params - reason behind 2 - see paper initial condition 
    EPS, Q0, P0 = 1/10, 0, 5 # momentums 2 and 5 in the paper 
    DELTA, C, ALPHA = 0.5, -np.pi, np.pi
    # space    
    XL, XR = -30, 30
    N = 2**14
    # time
    T, TSTEP, TDIR= 20/P0, 1/100/P0, 1
    #potential params
    NEQS = 2
    if len(sys.argv) > 1:
        DELTA, ALPHA, EPS, P0 = [float(string) for string in sys.argv[1:]]
    FNAME = './data/single/center/flatdelta%.3fc%.3falpha%.3feps%.3fp%d.txt' %(DELTA, C, ALPHA, EPS, P0)
    # ---------------- INIT -------------------------
    space = Space(N, XL, EPS, XR)
    time_back = Time(T/2, TSTEP, -1)
    wave_boa = Gaussian(EPS, Q0, P0, 'boa', 1, space) # init psi and psi hat
    potential = Single(DELTA, C, ALPHA,  'up')
    solver_boa = Strang(EPS, space, time_back, potential, 1)

    # ---------------- RUN BACKWARD ------------------
    run_backward(time_back, solver_boa, wave_boa)
    
    time = Time(T, TSTEP, TDIR)
    wave = Gaussian(EPS, Q0, P0, 'exact') # init psi and psi hat
    wave.psi = np.stack((wave_boa.psi.copy(), np.zeros(space.n, dtype='complex_')))
    wave_formulaup = Gaussian(EPS, Q0, P0, 'formulaup') # init psi and psi hat
    wave_formuladown = Gaussian(EPS, Q0, P0, 'formuladown') # init psi and psi hat
    wave_exactup = Gaussian(EPS, Q0, P0, 'exactup') # init psi and psi hat
    wave_exactdown = Gaussian(EPS, Q0, P0, 'exactdown') # init psi and psi hat
    potential2 = Single(DELTA, C, ALPHA, 'down')
    solver = Strang(EPS, space, time, potential, 2)
    # need this because now BOA evolving forward
    solver_boa = Strang(EPS, space, time, potential, 1)
    solver_exactup = Strang(EPS, space, time_back, potential, 1)
    solver_exactdown = Strang(EPS, space, time_back, potential2, 1)
    # ----------------- RUN -----------------------
    # returns wavefunctions at the location of the avoided crossing
    wave_boa, wave_formuladown, wave_formulaup, wave_exactdown, wave_exactup = run(time)
    Data.save(FNAME, space, [wave_boa, wave_exactup, wave_exactdown,
                           wave_formulaup, wave_formuladown])
                # it more abstract
                # it more abstract
