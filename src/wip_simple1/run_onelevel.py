#import terminalplot as tp

def run_simple(time, space, solver, wave, potential, fname):

    f = open(fname, 'w')
    header = 'itr \t mean_x \t mean_p \t ke \t e \t mass \n'
    f.write(header)
    
    for itr in range(time.max_itr):

        
        solver.do_step(wave, space, itr, time.max_itr)
        
       
        if itr in time.snap:
            mean_x = wave.get_meanx(space)
            mean_p = wave.get_meanp(space)
            ke = wave.get_ke(space)
            e = wave.get_e(space, potential)
            
            data = np.array([itr, 
                    mean_x, mean_p,
                    ke, e,
                    wave.get_massx(space)])
            
            np.savetxt(f, data.reshape(1,-1))
            
            #tp.plot(list(space.xgrid), list(abs(wave.psi[0,:])**2))
            
        
    f.close()

    return wave

def run_stop(time, space, solver, wave, potential, fname):
    
    itr = range(1, time.max_itr + 100)
    count = 0
    while wave.get_meanx(space) > 0: 
        solver.do_step(wave, space, itr[count], time.max_itr)
        if itr[count] in time.snap:
            print('%.2f %%' % (itr[count]/(time.max_itr) * 100), end='\r')
            print("------------ Observables -------------") # do not repeat
            print("      Mass x={:.12f}  ".format(wave.get_massx(space)))
            print("      Mean x={:.12f}  ".format(wave.get_meanx(space)))
            print("      Mass p={:.12f}  ".format(wave.get_massp(space)))
            print("      Mean p={:.12f}  ".format(wave.get_meanp(space)))
            
            #tp.plot(list(space.xgrid), list(abs(wave.psi)**2))
        count += 1
    return wave

def run_coupled(time, space, solver, wave, potential, fname):
    
    f = open(fname, 'w')
    header = 'itr \t mean_x_up \t mean_x_down \t mean_p_up \t mean_p_down \
            \t ke_up \t ke_down \t e_up \t e_down \t mass_up \t mass_down \n'
    f.write(header)

    for itr in range(time.max_itr):
        
        solver.do_step(wave, space, itr, time.max_itr)
        
       
        if itr in time.snap:
            mean_x_up = wave.get_meanx(space)[0]
            mean_x_down = wave.get_meanx(space)[1]
            mean_p_up = wave.get_meanp(space)[0]
            mean_p_down = wave.get_meanp(space)[1]
            ke_up = wave.get_ke(space)[0]
            ke_down = wave.get_ke(space)[1]
            e_up = wave.get_e(space, potential)[0]
            e_down = wave.get_e(space, potential)[1]
            
            data = np.array([itr, 
                    mean_x_up, mean_x_down,
                    mean_p_up, mean_p_down,
                    ke_up, ke_down, 
                    e_up, e_down,
                    wave.get_massx(space)[0], 
                    wave.get_massx(space)[1]])
            
            np.savetxt(f, data.reshape(1,-1))
            print('%.2f %%' % (itr/(time.max_itr) * 100), end='\r')
            print("------------ Observables -------------") # do not repeat
            print("      Mass x={:.12f}  ".format(wave.get_massx(space)[0]))
            print("      Mean x={:.12f}  ".format(wave.get_meanx(space)[0]))
            print("      Mass p={:.12f}  ".format(wave.get_massp(space)[0]))
            print("      Mean p={:.12f}  ".format(wave.get_meanp(space)[0]))
            
            #tp.plot(list(space.xgrid), list(abs(wave.psi[0,:])**2))
            
    f.close()
    
    return wave


if __name__ == '__main__':
    """ Sample Wigner distribution --> evolve particles --> detect crossing --> jump """
    import sys 
    sys.path.insert(0, '..')
    from init_cond.gaussian import Gaussian
    from auxiliary.space import Space
    from auxiliary.time import Time
    from auxiliary.efft import ifft, fft
    from auxiliary.data import Data
    from potentials.examples.simple1 import Simple1
    from solvers.pde.strang import Strang
    from transition_formulae import superadiabatic 
    import matplotlib.pyplot as plt 
    import numpy as np
    #import logging 

    # ----------------- PRINT OUPUT TO A FILE
    sys.stdout = open("info_run.txt", "w")
    
    #  ---------------- PARAMETERS FOR INITIAL WIGNER DISTRIBUTION 
    EPS, q, p = 1/10, -10, 4 
    #  ---------------- PARAMETERS FOR UNIFORM GRID
    XL, XR, N = -20, 20,  2**16
    #  ---------------- PARAMETERS FOR TIME
    T, TSTEP, TDIR= 20/p, 1/100/p, 1 
    #  ---------------- PARAMETERS FOR POTENTIAL 
    DELTA, ALPHA = 0.5, 0.5 # delta 0.1# CHANGE PARAMETERS
    NEQS = 2
    #  ---------------- CHECK FOR COMMAND LINE ARGUMENTS
    if len(sys.argv) > 1:
        DELTA, ALPHA, EPS, p = [float(string) for string in sys.argv[1:]] # change parameters
        # add a check for the parameters fed 
    # ----------------- SAVE DATA TO FOLLOWING FILE 
    FNAME = './data/onelevelwavepacketdelta%.4falpha%.4feps%.4fp%d.txt' \
            %(DELTA, ALPHA, EPS, p) # TO CHANGE
    FNAME_OBS = './data/onelevelobservablesdelta%.4falpha%.4feps%.4fp%d.txt' \
            %(DELTA, ALPHA, EPS, p) # TO CHANGE
    
    print("############ Simulation parameters ##############")
    print("-----> Potential is Simple1") 
    # makes sense to have this potential class
    print("-----> delta={:.4f}, alpha={:.4f}".format(DELTA, ALPHA))
    print("------------ Simulation parameters ---------------")
    print("------------ Simulation parameters ---------------")

    # --------------- INITIALISE SPACE-TIME-POTENTIAL BACKWARD
    space = Space(N, XL, EPS, XR)
    time_back = Time(T/2, TSTEP, -1)
    potential = Simple1(ALPHA, DELTA, 'up')
    solver_boa_back = Strang(EPS, space, time_back, potential, 1)
   
    """
    # --------------- INITIALISE GAUSSIAN WAVEPACKET WITH DEFINED PARAMETERS 
    wave_boa = Gaussian(EPS, q, p, 'boa', 1, space) # init psi and psi hat
    
    # --------------- EVOLVE BACKWARD FROM CROSSING --------------
    #run_simple(time_back, space, solver_boa_back, wave_boa, FNAME_OBS)
    # --------------- EVOLVE FORWARD --------------
    """
    wave = Gaussian(EPS, q, p, 'exact', 1, space) # init psi and psi hat
    #wave = Gaussian(EPS, q, p, 'exact') # init psi and psi hat
    #wave.psi = np.stack((wave_boa.psi.copy(), np.zeros(space.n, dtype='complex_')))
    time_forward = Time(T, TSTEP, 1)
    solver_single = Strang(EPS, space, time_forward, potential, 1)
    run_simple(time_forward, space, solver_single, wave, potential, FNAME_OBS)
    
    # --------------- SAVE DATA --------------
    Data.save(FNAME, space, [wave]) # this will not work

    

    # ----------------- SAVE DATA
    print("GOOD LUCK -------------------------------------------")
    
    sys.stdout.close()


