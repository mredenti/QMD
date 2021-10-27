
def angle(z1, z2):
    "angle of the difference would be wrong - consider the case of two \
            vectors with the same phase and of different lenghts"
    diff = (np.arctan2(z1.imag, z1.real) - np.arctan2(z2.imag, z2.real)) % 2*np.pi
    #return np.qin(diff, 2*np.pi - diff)
    return diff

def run_backward2(time, solver, wave, space):

    for itr in range(1, time.max_itr + 1):
       
        if wave.get_meanx(space) > 0:
            solver.do_step(wave, space, itr, time.max_itr)
            print('%.2f %%' % (itr/(time.max_itr) * 100), end='\r')

    return wave

def run_backward(time, solver, wave):

    for itr in range(1, time.max_itr + 1):
        
        solver.do_step(wave, space, itr, time.max_itr)
        print('%.2f %%' % (itr/(time.max_itr) * 100), end='\r')

    return wave

def run(time):
   
    snap = [i for i in np.arange(1,time.max_itr, time.max_itr//6)]
    crossed = False
    for itr in range(1, time.max_itr + 1):
        # this should return, amongst else, boa at the crossing
        solver.do_step(wave, space, itr, time.max_itr)
        solver_boa.do_step(wave_boa, space, itr, time.max_itr)
        """
        if itr in snap:
            #plt.plot(space.xgrid, abs(wave.psi[0,:]), label = 'exact up')
            plt.plot(space.xgrid, abs(wave.psi[1,:]), label = 'exact down')
            plt.plot(space.xgrid, abs(wave_boa.psi), label = 'BOA')
            plt.legend()
            plt.show()
            plt.close()
        """
        print('%.2f %%' % (itr/(time.max_itr) * 100), end='\r')
        if not crossed:
            #solver_boa.do_step(wave_boa, space, itr, time.max_itr)
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
                # upper level naive 1
                mass_lower = wave_formuladown.get_massp(space)
                wave_upper_mass.psihat = superadiabatic.get_upper_mass(
                    wave_boa.psihat, mass_lower) 
                
                # upper level naive 2
                wave_upper_minus.psihat = superadiabatic.get_upper_minus(
                                                wave_boa.psihat, space, 
                                                wave_boa.eps, q_c,
                                                DELTA, gamma) 
                
                wave_formuladown.psi = ifft(wave_formuladown, space) 
                wave_formulaup.psi = ifft(wave_formulaup, space) 
                wave_upper_mass.psi = ifft(wave_upper_mass, space) 
                wave_upper_minus.psi = ifft(wave_upper_minus, space) 
                crossed = True
        else:
            solver_exactup.do_step(wave_formulaup, space, itr, time.max_itr)
            solver_exactup.do_step(wave_upper_mass, space, itr, time.max_itr)
            solver_exactup.do_step(wave_upper_minus, space, itr, time.max_itr)
            solver_exactdown.do_step(wave_formuladown, space, itr, time.max_itr)
            """
            if itr in snap:
                #plt.plot(space.xgrid, abs(wave.psi[0,:]), label = 'exact up')
                plt.plot(space.xgrid, abs(wave_formulaup.psi), label = 'form+')
                plt.plot(space.xgrid, abs(wave_formuladown.psi), label = 'form-')
                plt.legend()
                plt.show()
                plt.close()
             """
    
    wave_exactup.psi = wave.psi[0,:].copy()
    wave_exactdown.psi = wave.psi[1,:].copy()
    wave_exactup.psihat = wave.psihat[0,:].copy()
    wave_exactdown.psihat = wave.psihat[1,:].copy()
    
    #run_backward2(time_back, solver_exactup, wave_exactup, space)
    #run_backward2(time_back, solver_exactdown, wave_exactdown, space)
    
    return (wave_boa, wave_formuladown, wave_formulaup, wave_exactdown, wave_exactup, wave_upper_mass, wave_upper_minus)

if __name__ == '__main__':
    import sys 
    sys.path.insert(0, '..')
    from init_cond.gaussian6 import Gaussian6
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
        DELTA, C, ALPHA, EPS, P0 = [float(string) for string in sys.argv[1:]]
    FNAME = './data/delta%.3fc%.3falpha%.3feps%.3fp%d.txt' %(DELTA, C, ALPHA, EPS, P0)
    print(ALPHA)
    # ---------------- INIT -------------------------
    space = Space(N, XL, EPS, XR)
    time_back = Time(T/2, TSTEP, -1)
    wave_boa = Gaussian6(EPS, Q0, P0, 'boa', 1, space) # init psi and psi hat
    potential = Single(DELTA, C, ALPHA, 'up')
    solver_boa = Strang(EPS, space, time_back, potential, 1)

    # ---------------- RUN BACKWARD ------------------
    wave_boa = run_backward(time_back, solver_boa, wave_boa)
    
    time = Time(T, TSTEP, TDIR)
    wave = Gaussian6(EPS, Q0, P0, 'exact') # init psi and psi hat
    wave.psi = np.stack((wave_boa.psi.copy(), np.zeros(space.n, dtype='complex_')))
    wave_formulaup = Gaussian6(EPS, Q0, P0, 'formulaup') # init psi and psi hat
    wave_formuladown = Gaussian6(EPS, Q0, P0, 'formuladown') # init psi and psi hat
    wave_upper_mass = Gaussian6(EPS, Q0, P0, 'upper mass') # init psi and psi hat
    wave_upper_minus = Gaussian6(EPS, Q0, P0, 'upper minus') # init psi and psi hat
    wave_exactup = Gaussian6(EPS, Q0, P0, 'exactup') # init psi and psi hat
    wave_exactdown = Gaussian6(EPS, Q0, P0, 'exactdown') # init psi and psi hat
    potential2 = Single(DELTA, C, ALPHA, 'down')
    solver = Strang(EPS, space, time, potential, 2)
    # need this because now BOA evolving forward
    solver_boa = Strang(EPS, space, time, potential, 1)
    solver_exactup = Strang(EPS, space, time, potential, 1)
    solver_exactdown = Strang(EPS, space, time, potential2, 1)
    # ----------------- RUN -----------------------
    # returns wavefunctions at the location of the avoided crossing
    wave_boa, wave_formuladown, wave_formulaup, wave_exactdown, wave_exactup, wave_upper_mass, wave_upper_minus = run(time)
    Data.save(FNAME, space, [wave_boa, wave_exactup, wave_exactdown,
                           wave_formulaup, wave_formuladown, wave_upper_mass, wave_upper_minus])
                # it more abstract
                # it more abstract
